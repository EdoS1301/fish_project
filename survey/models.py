from django.db import models

class SurveyResponse(models.Model):
    session_id = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(verbose_name="Электронная почта")  # Новое поле
    password_compliance = models.CharField(max_length=20, verbose_name="Соответствие пароля")
    two_factor = models.CharField(max_length=20, verbose_name="Двухфакторная аутентификация")
    password_change = models.CharField(max_length=20, verbose_name="Смена паролей")
    familiar = models.CharField(max_length=20, verbose_name="Ознакомление с регламентом")
    button_clicked = models.BooleanField(default=False, verbose_name="Кнопка нажата")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        status = "отправлено" if self.button_clicked else "автосохранено"
        return f"{self.email} - {status} - {self.created_at.strftime('%d.%m.%Y %H:%M')}"
    
    class Meta:
        verbose_name = "Ответ на опрос"
        verbose_name_plural = "Ответы на опрос"
        ordering = ['-created_at']

class PageVisit(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    user_agent = models.TextField(verbose_name="User Agent")
    visited_at = models.DateTimeField(auto_now_add=True, verbose_name="Время посещения")
    
    def __str__(self):
        return f"Посещение от {self.ip_address} - {self.visited_at.strftime('%d.%m.%Y %H:%M')}"
    
    class Meta:
        verbose_name = "Посещение страницы"
        verbose_name_plural = "Посещения страниц"
        ordering = ['-visited_at']