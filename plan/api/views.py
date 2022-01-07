from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.api.authentication import SafeJWTAuthentication
from plan.models import Questionnaire, SectionOne, SectionTwo

from .serializers import QuestionnaireSerializer, SectionOneSerializer, SectionTwoSerializer


class QuestionnaireRetrieveView(generics.RetrieveAPIView):
    lookup_field = 'uuid'
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SafeJWTAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 'success',
            'message': serializer.data
        }, status=status.HTTP_200_OK)


class QuestionnaireListView(generics.ListAPIView):
    serializer_class = QuestionnaireSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SafeJWTAuthentication,)
    model = Questionnaire

    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'code': 'success',
            'message': serializer.data
        }, status=status.HTTP_200_OK)


class QuestionnaireCreateView(generics.CreateAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SafeJWTAuthentication,)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'code': 'success',
            'message': response.data,
        }, status=status.HTTP_201_CREATED)


class QuestionnaireUpdateView(generics.UpdateAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    lookup_field = 'uuid'
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SafeJWTAuthentication,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == 4:
            return Response({
                'code': 'success',
                'message': 'Object already submitted'
            })
        # request.data['status] should be received equal 4
        if request.data['status'] != 4:
            return Response({
                'code': 'fail',
                'message': '%s not a valid choice' % request.data['status']
            })
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 'success',
                'message': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'code': 'fail',
                'message': serializer.errors
            })


class SectionOneAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SafeJWTAuthentication,)
    MODEL_CLASS = SectionOne
    SERIALIZER_CLASS = SectionOneSerializer

    def post(self, request, uuid):
        try:
            questionnaire = Questionnaire.objects.get(uuid=uuid, user=request.user)
        except ObjectDoesNotExist:
            return Response({
                'code': 'fail',
                'message': 'Object does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data['questionnaire'] = questionnaire.pk
        serializer = self.SERIALIZER_CLASS(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Set questionnaire status section one submitted
        questionnaire.status = 2
        questionnaire.save()
        return Response({
            'code': 'success',
            'message': serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request, uuid):
        try:
            questionnaire = Questionnaire.objects.get(uuid=uuid, user=request.user)
        except ObjectDoesNotExist:
            return Response({
                'code': 'fail',
                'message': 'Object does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        try:
            section = self.MODEL_CLASS.objects.get(questionnaire=questionnaire)
        except ObjectDoesNotExist:
            return Response({
                'code': 'fail',
                'message': 'Object does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = self.SERIALIZER_CLASS(section)
        return Response({
            'code': 'success',
            'message': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, uuid):
        try:
            questionnaire = Questionnaire.objects.get(uuid=uuid, user=request.user)
        except ObjectDoesNotExist:
            return Response({
                'code': 'fail',
                'message': 'Object does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        if questionnaire.status == 4:
            return Response({
                'code': 'success',
                'message': 'Object already submitted'
            })
        try:
            section = self.MODEL_CLASS.objects.get(questionnaire=questionnaire)
        except ObjectDoesNotExist:
            return Response({
                'code': 'fail',
                'message': 'Object does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data['questionnaire'] = questionnaire.pk
        serializer = self.SERIALIZER_CLASS(data=request.data, instance=section)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'code': 'success',
            'message': serializer.data
        })


class SectionTwoAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SafeJWTAuthentication,)
    MODEL_CLASS = SectionTwo
    SERIALIZER_CLASS = SectionTwoSerializer

    def post(self, request, uuid):
        try:
            questionnaire = Questionnaire.objects.get(uuid=uuid, user=request.user)
        except ObjectDoesNotExist:
            return Response({
                'code': 'fail',
                'message': 'Object does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data['questionnaire'] = questionnaire.pk
        serializer = self.SERIALIZER_CLASS(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Set questionnaire status section two submitted
        questionnaire.status = 3
        questionnaire.save()
        return Response({
            'code': 'success',
            'message': serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request, uuid):
        try:
            questionnaire = Questionnaire.objects.get(uuid=uuid, user=request.user)
        except ObjectDoesNotExist:
            return Response({
                'code': 'fail',
                'message': 'Object does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        try:
            section = self.MODEL_CLASS.objects.get(questionnaire=questionnaire)
        except ObjectDoesNotExist:
            return Response({
                'code': 'fail',
                'message': 'Object does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = self.SERIALIZER_CLASS(section)
        return Response({
            'code': 'success',
            'message': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, uuid):
        try:
            questionnaire = Questionnaire.objects.get(uuid=uuid, user=request.user)
        except ObjectDoesNotExist:
            return Response({
                'code': 'fail',
                'message': 'Object does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        if questionnaire.status == 4:
            return Response({
                'code': 'success',
                'message': 'Object already submitted'
            })
        try:
            section = self.MODEL_CLASS.objects.get(questionnaire=questionnaire)
        except ObjectDoesNotExist:
            return Response({
                'code': 'fail',
                'message': 'Object does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data['questionnaire'] = questionnaire.pk
        serializer = self.SERIALIZER_CLASS(data=request.data, instance=section)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'code': 'success',
            'message': serializer.data
        })
