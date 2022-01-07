from django.urls import path

from .views import (QuestionnaireCreateView,
                    QuestionnaireUpdateView,
                    QuestionnaireRetrieveView,
                    QuestionnaireListView,
                    SectionOneAPIView,
                    SectionTwoAPIView)

urlpatterns = [
    path('questionnaire', QuestionnaireListView.as_view()),     # Get all user plans
    path('questionnaire/', QuestionnaireCreateView.as_view()),     # Post new plan
    path('questionnaire/<uuid>', QuestionnaireRetrieveView.as_view()),      # Get plan information before submit
    path('questionnaire/<uuid>/', QuestionnaireUpdateView.as_view()),       # Submit plan
    path('section/one/<uuid:uuid>/', SectionOneAPIView.as_view()),      # Get, Post, Submit section one
    path('section/two/<uuid:uuid>/', SectionTwoAPIView.as_view()),      # Get, Post, Submit section two
]
