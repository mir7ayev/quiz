from django.contrib import admin
from .models import Subject, Question, Answer, QuizResult


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject')
    list_display_links = ('id', 'subject')
    list_filter = ('id', 'subject')
    search_fields = ('id', 'subject')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'is_correct')
    list_display_links = ('id', 'question')
    list_filter = ('id', 'question', 'is_correct')
    search_fields = ('id', 'question')


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'is_correct')
    list_display_links = ('user', 'question')
    list_filter = ('user', 'question', 'answer', 'is_correct')
    search_fields = ('user', 'question', 'answer')
