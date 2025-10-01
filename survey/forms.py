from django import forms
from .models import SurveyResponse

class SurveyForm(forms.ModelForm):
    class Meta:
        model = SurveyResponse
        fields = [
            'email',  # Только email сохраняем
            'password_compliance', 'two_factor', 'password_change', 'familiar'
        ]
        labels = {
            'email': 'Электронная почта',
            'password_compliance': 'Соответствие пароля требованиям',
            'two_factor': 'Двухфакторная аутентификация',
            'password_change': 'Частота смены паролей',
            'familiar': 'Ознакомление с регламентом ИБ'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Введите вашу электронную почту'})
        }