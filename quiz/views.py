from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Subject, Question, Answer, QuizResult
from .serilizers import SubjectSerializer, QuestionSerializer


class QuizViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Get all subjects",
        responses={200: SubjectSerializer(many=True)},
        tags=["Quiz"]
    )
    @action(methods=['get'], detail=False)
    def subjects(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Retrieve questions for a subject",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'subject': openapi.Schema(type=openapi.TYPE_STRING)},
            required=['subject']
        ),
        responses={200: QuestionSerializer(many=True)},
        tags=["Quiz"]
    )
    @action(methods=['post'], detail=False)
    def questions(self, request):
        subject_name = request.data.get('subject')
        if subject_name is None:
            return Response("No subject provided", status=status.HTTP_404_NOT_FOUND)

        subject = get_object_or_404(Subject, name=subject_name)
        questions = Question.objects.filter(subject=subject).order_by('?')[:10]

        for question in questions:
            question.answers = Answer.objects.filter(question=question)

        serializer = QuestionSerializer(questions, many=True)

        request.session['quiz_start_time'] = str(timezone.now())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Submit answers and receive results",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'question_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'answer': openapi.Schema(type=openapi.TYPE_INTEGER)
            },
            required=['question_id', 'answer']
        ),
        responses={
            200: "Answer recorded",
            400: "Bad request",
            404: "Question or answer not found"
        },
        tags=["Quiz"]
    )
    @action(methods=['post'], detail=False)
    def answers(self, request):
        user = request.user

        start_time = request.session.get('quiz_start_time')
        if start_time is None:
            return Response("No start time provided", status=status.HTTP_404_NOT_FOUND)
        start_time = timezone.datetime.fromisoformat(start_time)

        question_id = request.data.get('question_id')
        if question_id is None:
            return Response("No question_id provided", status=status.HTTP_404_NOT_FOUND)

        answer_id = request.data.get('answer')
        if answer_id is None:
            return Response("No answer provided", status=status.HTTP_404_NOT_FOUND)

        question = Question.objects.filter(id=question_id).first()
        if question is None:
            return Response("No question found", status=status.HTTP_400_BAD_REQUEST)

        answer = Answer.objects.filter(id=answer_id, question_id=question_id).first()
        if answer is None:
            return Response("No answer found", status=status.HTTP_400_BAD_REQUEST)

        is_correct = answer.is_correct

        if (timezone.now() - start_time).total_seconds() > 180:
            is_correct = False

        quiz_result = QuizResult.objects.create(
            user=user,
            question_id=question_id,
            answer_id=answer_id,
            is_correct=is_correct
        )
        quiz_result.save()

        results = request.session.get('quiz_results', [])

        results.append({
            'question': question.text,
            'selected_answer': answer.text,
            'is_correct': is_correct
        })

        request.session['quiz_results'] = results

        if len(results) == 10:
            total_correct = sum(result['is_correct'] for result in results)

            del request.session['quiz_start_time']
            del request.session['quiz_results']

            subject = 'Quiz Results'
            message = f'You answered {total_correct} out of 10 questions correctly.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            return Response({"message": "Quiz completed. Results have been sent to your email."},
                            status=status.HTTP_200_OK)

        return Response({"message": "Answer recorded"}, status=status.HTTP_200_OK)
