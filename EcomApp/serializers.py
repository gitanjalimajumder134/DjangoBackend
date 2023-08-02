from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizzes
        fields = ['title']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_right']


class RandomQuesionsSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['title', 'answer',]


class QuizQuesionsSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True, read_only=True)
    quiz = QuizSerializer(read_only=True)
    class Meta:
        model = Question
        fields = ['quiz', 'title', 'answer',]