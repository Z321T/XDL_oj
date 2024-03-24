import torch
import json
import subprocess
from sklearn.decomposition import PCA
from django.shortcuts import get_object_or_404
from transformers import AutoTokenizer, AutoModel
from torch.nn.functional import cosine_similarity
from cpplint import liplnt
# cpplint
from django.db.models.signals import post_save
from django.dispatch import receiver

from CodeBERT_app.models import (ProgrammingCodeFeature, ProgrammingReportFeature,
                                 ReportStandardScore, CodeStandardScore)
from administrator_app.models import ProgrammingExercise
from teacher_app.models import ExerciseQuestion, ExamQuestion, ReportScore, Teacher, Class

# 加载 CodeBERT 模型和分词器
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")


# 分析练习与考试代码
# def analyze_code(student, code, types, question_id=None):
#     # 分词
#     tokenized_code = tokenizer.tokenize(code)
#     features = []
#     for i in range(0, len(tokenized_code), 512):
#         inputs = tokenizer(tokenized_code[i:i+512], return_tensors="pt", padding=True, truncation=True, max_length=512)
#         # 获取特征值
#         with torch.no_grad():
#             feature = model(**inputs).last_hidden_state.mean(dim=1)
#             features.append(feature)
#     # 连接所有特征值
#     concatenated_features = torch.cat(features, dim=0)
#     feature_as_json = json.dumps(concatenated_features.tolist())
#
#     if types == 'exercise':
#         question = ExerciseQuestion.objects.get(id=question_id)
#         CodeFeature.objects.create(student=student, exercise_question=question, feature=feature_as_json)
#     elif types == 'exam':
#         question = ExamQuestion.objects.get(id=question_id)
#         CodeFeature.objects.create(student=student, exam_question=question, feature=feature_as_json)


# 分析程序设计题代码
def analyze_programming_code(student, code, question_id):
    # 代码分词
    tokenized_code = tokenizer.tokenize(code)
    features = []
    for i in range(0, len(tokenized_code), 512):
        inputs = tokenizer(tokenized_code[i:i+512], return_tensors="pt", padding=True, truncation=True, max_length=512)
        # 获取特征值
        with torch.no_grad():
            feature = model(**inputs).last_hidden_state.mean(dim=1)
            features.append(feature)
    # 连接所有特征值
    concatenated_features = torch.cat(features, dim=0)
    # 使用 PCA 进行维度减少，n_components可以根据需要改变
    pca = PCA(n_components=2)
    # 注意：PCA需要在CPU上的NumPy数组上运行
    reduced_features = pca.fit_transform(concatenated_features.cpu().numpy())
    # 将降维后的特征转换为JSON格式
    feature_as_json = json.dumps(reduced_features.tolist())

    question = ProgrammingExercise.objects.get(id=question_id)
    ProgrammingCodeFeature.objects.update_or_create(
        student=student,
        programming_question=question,
        defaults={'feature': feature_as_json}
    )


# 分析程序设计题报告
def analyze_programming_report(student, report, question_id):
    # 报告分词
    tokenized_report = tokenizer.tokenize(report)
    features = []
    for i in range(0, len(tokenized_report), 512):
        inputs = tokenizer(tokenized_report[i:i+512], return_tensors="pt", padding=True, truncation=True, max_length=512)
        # 获取特征值
        with torch.no_grad():
            feature = model(**inputs).last_hidden_state.mean(dim=1)
            features.append(feature)
    # 连接所有特征值
    concatenated_features = torch.cat(features, dim=0)
    # 使用 PCA 进行维度减少，n_components可以根据需要改变
    pca = PCA(n_components=2)
    # 注意：PCA需要在CPU上的NumPy数组上运行
    reduced_features = pca.fit_transform(concatenated_features.cpu().numpy())
    # 将降维后的特征转换为JSON格式
    feature_as_json = json.dumps(reduced_features.tolist())

    question = ProgrammingExercise.objects.get(id=question_id)
    ProgrammingReportFeature.objects.update_or_create(
        student=student,
        programming_question=question,
        defaults={'feature': feature_as_json}
    )


# 计算程序设计报告&代码的相似度
def compute_cosine_similarity(feature_json1, feature_json2):
    feature1 = torch.tensor(json.loads(feature_json1)).float()
    feature2 = torch.tensor(json.loads(feature_json2)).float()

    # 填充较小的张量以匹配较大的张量的维度
    if feature1.numel() < feature2.numel():
        # 在第二个维度填充零
        padding = feature2.numel() - feature1.numel()
        feature1 = torch.cat([feature1, torch.zeros(padding)], dim=0)
    elif feature1.numel() > feature2.numel():
        padding = feature1.numel() - feature2.numel()
        feature2 = torch.cat([feature2, torch.zeros(padding)], dim=0)

    feature1 = feature1.view(1, -1)
    feature2 = feature2.view(1, -1)

    similarity_tensor = cosine_similarity(feature1, feature2)

    similarity_score = similarity_tensor.item()

    return similarity_score


# 报告规范性评分
def score_report(student, document, programmingexercise_id):
    class_assigned = student.class_assigned
    teacher = get_object_or_404(Class, id=class_assigned.id).teacher
    report_score = ReportScore.objects.get(teacher=teacher)

    total_score = report_score.totalscore
    content_score = report_score.contents
    firstrow_score = report_score.firstrow
    fontsize_score = report_score.fontsize
    image_score = report_score.image
    pagenum_score = report_score.pagenum

    # 1. 检查文档是否含有目录
    for para in document.paragraphs:
        if "目录" in para.text:
            break
        else:
            total_score += content_score

    # 2. 检查每个段落的首行缩进
    first_line = False
    for para in document.paragraphs:
        if not para.paragraph_format.first_line_indent or para.paragraph_format.first_line_indent.pt != 36:
            first_line = True
            break
    if first_line:
        total_score += firstrow_score

    # 3. 检查段落中的文字字体大小是否为12
    font_size = False
    for para in document.paragraphs:
        if font_size:
            break
        for run in para.runs:
            if run.font.size and abs(run.font.size.pt - 12) > 1:
                font_size = True
                break
    if font_size:
        total_score += fontsize_score

    # 4. 检查文档中的图像是否居中对齐
    image_alignment = False
    for shape in document.inline_shapes:
        if shape.type == 3:
            if shape.text_frame.paragraph.alignment != 1:
                image_alignment = True
                break
    if image_alignment:
        total_score += image_score

    # 5. 计算有页码的页面占比
    def score_page_numbers(doc):
        total_pages = len(doc.sections)
        for section in doc.sections:
            page_number_found = False
            for para in section.footer.paragraphs:
                if any(char.isdigit() for char in para.text):
                    page_number_found = True
                    break
            if not page_number_found:
                return True
        if total_pages == 0:
            return True
        return False
    if score_page_numbers(document):
        total_score += pagenum_score

    # 保存分数
    ReportStandardScore.objects.update_or_create(
        student=student,
        programming_question_id=programmingexercise_id,
        defaults={'standard_score': total_score}
    )


# cppcheck的使用
#  @receiver(post_save, sender=CodeStandardScore)
# # def run_cppcheck(sender, instance, code_file, **kwargs):
# def run_cppcheck(student, code_file, programmingexercise_id):
#     cppcheck_output = subprocess.check_output(['cppcheck', code_file])
#     score = code_score(cppcheck_output)
#     CodeStandardScore.objects.update_or_create(
#         student=student,
#         programming_question_id=programmingexercise_id,
#         defaults={'standard_score': score}
#     )
#     # instance.score = score
#     # instance.save()
#
#
# # 代码规范性打分
# def code_score(cppcheck_output):
#     error_scores = {
#         'error': 10,
#         'warning': 5,
#         'performance': 3,
#         'style': 1,
#     }
#
#     total_score = 0
#     for line in cppcheck_output.splitlines():
#         for error_type, score in error_scores.items():
#             if error_type in line:
#                 total_score += score
#
#     return total_score

# cpplint

# @receiver(post_save, sender=CodeStandardScore)
# def run_cpplint(sender, instance, **kwargs):
def run_cpplint(student, file_path, programmingexercise_id):
    student = student
    code_file = file_path  # 假设 file_path 是 CodeStandardScore 模型中代表代码文件路径的字段
    programmingexercise_id = programmingexercise_id

    cpplint_output = subprocess.check_output(['cpplint', code_file], stderr=subprocess.STDOUT)
    score = code_style_score(cpplint_output)
    CodeStandardScore.objects.update_or_create(
        student=student,
        programming_question_id=programmingexercise_id,
        defaults={'standard_score': score}


    # # 更新 instance 的 style_score 而不是创建新的实例
    # instance.style_score = score
    # instance.save()


#def code_style_score(cpplint_output):
#    total_errors = 0
#   for line in cpplint_output.decode('utf-8').split('\n'):
#        if 'Total errors found' in line:
#           total_errors = int(line.split()[-1])
#            break
#    score = max(100 - total_errors, 0)
#    return score

# 注意：确保你已经为你的CodeStandardScore模型创建了file_path 和 programming_question_id 字段。


#def count_style_score(file_path):
 #   cpplint_output = subprocess.check_output(['cpplint', file_path])
  #  error_lines = cpplint_output.decode('utf-8').split('\n')
 #   error_count = len([line for line in error_lines if line.startswith('Total errors found:')])
 #   return error_count

import subprocess


def count_cpplint_errors(file_paths):
    """
    计算指定文件列表中cpplint的错误数量。
    :param file_paths: 文件路径列表。
    :return: cpplint错误数量。
    """
    cpplint_command = "cpplint"  # 假设cpplint在系统PATH中
    cpplint_errors_count = 0

    for file_path in file_paths:
        try:
            # 使用subprocess运行cpplint命令
            cpplint_output = subprocess.check_output([cpplint_command, file_path])
        except subprocess.CalledProcessError as e:
            # cpplint返回非零退出状态，表示发现错误
            cpplint_errors_count += e.output.count(b'\n')
        else:
            # 没有错误
            continue

    return cpplint_errors_count