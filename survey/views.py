from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import timedelta
import os
from .models import SurveyResponse, PageVisit
from .forms import SurveyForm
import json

def survey_page(request):
    # Считаем посещение страницы
    if not request.session.get('visited'):
        PageVisit.objects.create(
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        request.session['visited'] = True
    
    # Получаем или создаем идентификатор сессии для этого пользователя
    if not request.session.get('user_session_id'):
        import uuid
        request.session['user_session_id'] = str(uuid.uuid4())
    
    user_session_id = request.session['user_session_id']
    
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # УДАЛЯЕМ ВСЕ СТАРЫЕ ЗАПИСИ ДЛЯ ЭТОЙ ПОЧТЫ
            deleted_count = SurveyResponse.objects.filter(
                email__iexact=email
            ).delete()[0]
            
            print(f"Удалено {deleted_count} старых записей для email: {email}")
            
            # Сохраняем данные формы с отметкой о нажатии кнопки
            survey_response = form.save(commit=False)
            survey_response.button_clicked = True
            survey_response.session_id = user_session_id
            survey_response.save()
            return redirect('success_page')
    else:
        form = SurveyForm()
    
    context = {
        'form': form,
        'user_session_id': user_session_id,
    }
    return render(request, 'survey/survey.html', context)

def autosave_form(request):
    """Автосохранение формы (без нажатия кнопки)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_session_id = data.get('session_id')
            email = data.get('email', '').strip()
            
            if not user_session_id or not email:
                return JsonResponse({'status': 'error', 'message': 'No session ID or email'})
            
            # Проверяем, есть ли уже отправленная форма для этого email
            submitted_form = SurveyResponse.objects.filter(
                email__iexact=email,
                button_clicked=True
            ).first()
            
            # Если форма уже отправлена, не сохраняем автосохранение
            if submitted_form:
                return JsonResponse({'status': 'skipped', 'message': 'Form already submitted'})
            
            # УДАЛЯЕМ СТАРЫЕ АВТОСОХРАНЕНИЯ ДЛЯ ЭТОГО EMAIL
            old_autosaves = SurveyResponse.objects.filter(
                email__iexact=email,
                button_clicked=False
            )
            deleted_count = old_autosaves.delete()[0]
            
            if deleted_count > 0:
                print(f"Удалено {deleted_count} старых автосохранений для email: {email}")
            
            # Создаем новую запись автосохранения
            SurveyResponse.objects.create(
                session_id=user_session_id,
                email=email,
                password_compliance=data.get('password_compliance', ''),
                two_factor=data.get('two_factor', ''),
                password_change=data.get('password_change', ''),
                familiar=data.get('familiar', ''),
                button_clicked=False
            )
            
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error'})

def button_click(request):
    """Обработка нажатия кнопки отправки"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_session_id = data.get('session_id')
            email = data.get('email', 'unknown')
            
            # Проверяем, есть ли уже данные формы для этого email
            existing_form = SurveyResponse.objects.filter(
                email__iexact=email
            ).first()
            
            # Если уже есть форма, не создаем дубликат
            if existing_form:
                return JsonResponse({'status': 'skipped', 'message': 'Form already exists'})
            
            # Создаем запись о нажатии кнопки ТОЛЬКО если нет данных формы
            SurveyResponse.objects.create(
                session_id=user_session_id,
                email=email,
                password_compliance='not_submitted',
                two_factor='not_submitted', 
                password_change='not_submitted',
                familiar='not_submitted',
                button_clicked=True
            )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error'})

def download_pdf(request):
    """Скачивание PDF файла"""
    pdf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'pdf', 'regulation.pdf')
    
    if not os.path.exists(pdf_path):
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        return HttpResponse("PDF файл не найден. Пожалуйста, поместите файл regulation.pdf в папку static/pdf/")
    
    with open(pdf_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="regulation_ib.pdf"'
        return response

def success_page(request):
    return render(request, 'survey/success.html')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip