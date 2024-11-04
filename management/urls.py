from django.urls import path
from management import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('load-brgy/', views.load_barangay_json, name='load-brgy'),
    path('survey/<int:respondent_id>/', views.survey_page, name='survey'),
    path('add-option-question/<int:question_id>/', views.question_add_option, name='add-option'),
    path('survey-quali/<int:respondent_id>/', views.qualitative_survey_view, name='survey-quali'),
    path('dashboard/', views.analytics, name='analytics'),
    path('analysis-results/', views.analysis_results_pdf, name='analytics-pdf')
]
