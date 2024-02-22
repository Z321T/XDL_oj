import torch
import json
from transformers import AutoTokenizer, AutoModel
from .models import CodeFeature, Student, ExerciseQuestion, ExamQuestion

# 加载 CodeBERT 模型和分词器
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")


def analyze_code(student, code, types, question_id=None):
    # 分词
    inputs = tokenizer(code, return_tensors="pt", padding=True, truncation=True, max_length=512)
    # 获取特征值
    with torch.no_grad():
        # 保存特征值
        feature = model(**inputs).last_hidden_state.mean(dim=1).tolist()
        feature_as_json = json.dumps(feature)

    if types == 'exercise':
        question = ExerciseQuestion.objects.get(id=question_id)
        CodeFeature.objects.create(student=student, exercise_question=question, feature=feature_as_json)
    elif types == 'exam':
        question = ExamQuestion.objects.get(id=question_id)
        CodeFeature.objects.create(student=student, exam_question=question, feature=feature_as_json)

