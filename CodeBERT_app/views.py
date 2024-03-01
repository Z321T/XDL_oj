import torch
import json
from transformers import AutoTokenizer, AutoModel
from scipy.spatial.distance import cosine

from CodeBERT_app.models import CodeFeature, ProgrammingCodeFeature
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


# 计算程序设计报告的相似度
def calculate_cosine_similarity(feature_json1, feature_json2):
    # 加载特征值
    feature1 = torch.Tensor(json.loads(feature_json1))
    feature2 = torch.Tensor(json.loads(feature_json2))

    # 计算余弦相似度
    similarity_score = 1 - cosine(feature1, feature2)

    return similarity_score

    # # 假设你有两个代码的特征值
    # feature_as_json1 = analyze_programming_code(student1, code1, question_id1)
    # feature_as_json2 = analyze_programming_code(student2, code2, question_id2)
    #
    # # 计算相似度
    # similarity_score = calculate_cosine_similarity(feature_as_json1, feature_as_json2)
    # print(f"Similarity score: {similarity_score}")
