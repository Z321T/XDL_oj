import torch
import json
from transformers import AutoTokenizer, AutoModel
from torch.nn.functional import cosine_similarity

from CodeBERT_app.models import CodeFeature, ProgrammingCodeFeature, ProgrammingReportFeature
from administrator_app.models import ProgrammingExercise
from teacher_app.models import ExerciseQuestion, ExamQuestion

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
def analyze_programming_report(student, code, question_id):
    # 分词
    tokenized_report = tokenizer.tokenize(code)
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
