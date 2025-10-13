from django.db import models

class SurveyResponse(models.Model):
    session_id = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(verbose_name="Электронная почта")
    password_compliance = models.CharField(max_length=20, verbose_name="Соответствие пароля")
    two_factor = models.CharField(max_length=20, verbose_name="Двухфакторная аутентификация")
    password_change = models.CharField(max_length=20, verbose_name="Смена паролей")
    familiar = models.CharField(max_length=20, verbose_name="Ознакомление с регламентом")
    button_clicked = models.BooleanField(default=False, verbose_name="Кнопка нажата")
    pdf_downloaded = models.BooleanField(default=False, verbose_name="PDF скачан")
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

# НОВАЯ МОДЕЛЬ ДЛЯ СЧЕТЧИКА ПОСЕЩЕНИЙ ПО IP
class IPVisitCounter(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес", unique=True)
    visit_count = models.IntegerField(default=0, verbose_name="Количество посещений")
    first_visit = models.DateTimeField(auto_now_add=True, verbose_name="Первое посещение")
    last_visit = models.DateTimeField(auto_now=True, verbose_name="Последнее посещение")
    pdf_downloaded = models.BooleanField(default=False, verbose_name="PDF скачан с этого IP")
    
    def __str__(self):
        return f"{self.ip_address} - {self.visit_count} посещений"
    
    class Meta:
        verbose_name = "Счетчик посещений по IP"
        verbose_name_plural = "Счетчики посещений по IP"
        ordering = ['-visit_count', '-last_visit']