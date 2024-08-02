from rest_framework.serializers import ModelSerializer
from .models import (
    Subject, Question, Answer
)


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = ('name',)


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ('question', 'text', 'is_correct')


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ('subject', 'text', 'image')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['answers'] = AnswerSerializer(instance.answers.all(), many=True).data
        return representation
