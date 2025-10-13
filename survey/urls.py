from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey_page, name='survey_page'),
    path('autosave/', views.autosave_form, name='autosave_form'),
    path('button-click/', views.button_click, name='button_click'),
    path('pdf-button-click/', views.pdf_button_click, name='pdf_button_click'),  # Новый URL
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('success/', views.success_page, name='success_page'),
]