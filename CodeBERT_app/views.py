import torch
import json
from transformers import AutoTokenizer, AutoModel

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
    ProgrammingCodeFeature.objects.create(student=student, exercise_question=question, feature=feature_as_json)