import torch
import json
from docx import Document
from transformers import AutoTokenizer, AutoModel
from torch.nn.functional import cosine_similarity

from CodeBERT_app.models import CodeFeature, ProgrammingCodeFeature, ProgrammingReportFeature
from administrator_app.models import ProgrammingExercise
from teacher_app.models import ExerciseQuestion, ExamQuestion, ReportScore

# 加载 CodeBERT 模型和分词器
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")


# 分析练习与考试代码
def analyze_code(student, code, types, question_id=None):
    # 分词
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
    feature_as_json = json.dumps(concatenated_features.tolist())

    if types == 'exercise':
        question = ExerciseQuestion.objects.get(id=question_id)
        CodeFeature.objects.create(student=student, exercise_question=question, feature=feature_as_json)
    elif types == 'exam':
        question = ExamQuestion.objects.get(id=question_id)
        CodeFeature.objects.create(student=student, exam_question=question, feature=feature_as_json)


# 分析程序设计题代码
def analyze_programming_code(student, code, question_id):
    # 分词
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
    feature_as_json = json.dumps(concatenated_features.tolist())

    question = ProgrammingExercise.objects.get(id=question_id)
    ProgrammingCodeFeature.objects.create(student=student, programming_question=question, feature=feature_as_json)


# 分析程序设计题报告
def analyze_programming_report(student, report, question_id):
    # 分词
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
    feature_as_json = json.dumps(concatenated_features.tolist())

    question = ProgrammingExercise.objects.get(id=question_id)
    ProgrammingReportFeature.objects.create(student=student, programming_question=question, feature=feature_as_json)


# 计算程序设计报告&代码的相似度
def compute_cosine_similarity(feature_json1, feature_json2):
    feature1 = torch.tensor(json.loads(feature_json1)).float()
    feature2 = torch.tensor(json.loads(feature_json2)).float()

    feature1 = feature1.view(1, -1)
    feature2 = feature2.view(1, -1)

    similarity_tensor = cosine_similarity(feature1, feature2)

    similarity_score = similarity_tensor.item()

    return similarity_score


# 报告规范性评分
def score_report(file):

    doc = Document(file)  # 1. 检查文档是否含有目录
    has_table_of_contents = False
    for para in doc.paragraphs:
        if "目录" in para.text:
            has_table_of_contents = True
            break
    score_table_of_contents = 10 if has_table_of_contents else 0  # 2. 检查每个段落的首行缩进
    score_indentation = 10
    for para in doc.paragraphs:
        if not para.paragraph_format.first_line_indent or para.paragraph_format.first_line_indent.pt != 36:
            score_indentation -= 0.5
    score_indentation = max(0, score_indentation)  # 3. 检查段落中的文字字体大小是否为12
    score_font_size = 10
    for para in doc.paragraphs:
        for run in para.runs:
            if run.font.size and abs(run.font.size.pt - 12) > 1:
                score_font_size -= 1
    score_font_size = max(0, score_font_size)  # 4. 检查文档中的图像是否居中对齐
    score_image_alignment = 10
    for shape in doc.inline_shapes:
        if shape.type == 3:
            if shape.text_frame.paragraph.alignment != 1:
                score_image_alignment -= 1
    score_image_alignment = max(0, score_image_alignment)  # 5. 计算有页码的页面占比

    def score_page_numbers(doc):
        total_pages = len(doc.sections)
        pages_with_page_numbers = 0
        for section in doc.sections:
            for para in section.footer.paragraphs:
                if any(char.isdigit() for char in para.text):
                    pages_with_page_numbers += 1
                    break
        if total_pages == 0:
            return 0
        return min(10, (pages_with_page_numbers / total_pages) * 10)

    score_page_numbers = score_page_numbers(doc)  # 6. 检查段落的样式
    score_paragraph_style = 10
    for para in doc.paragraphs:
        if para.style.name.startswith('Heading'):
            level = int(para.style.name.split()[1])
            if para.style.name == f'Heading {level}':
                score_paragraph_style -= 5
    score_paragraph_style = max(0, score_paragraph_style)  # 计算平均分数
    total_score = (
            score_table_of_contents +
            score_indentation +
            score_font_size +
            score_image_alignment +
            score_page_numbers +
            score_paragraph_style
    )
    average_score = total_score / 6
