from django.contrib import admin
from .models import SurveyResponse, PageVisit

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['email', 'button_clicked_status', 'password_compliance', 'two_factor', 'password_change', 'familiar', 'created_at']
    list_filter = ['button_clicked', 'password_compliance', 'two_factor', 'password_change', 'familiar', 'created_at']
    search_fields = ['email']
    readonly_fields = ['created_at', 'session_id']
    fieldsets = (
        ('Контактная информация', {
            'fields': ('email',)
        }),
        ('Ответы на вопросы', {
            'fields': ('password_compliance', 'two_factor', 'password_change', 'familiar')
        }),
        ('Статус', {
            'fields': ('button_clicked',)
        }),
        ('Системная информация', {
            'fields': ('session_id', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def button_clicked_status(self, obj):
        if obj.button_clicked:
            if obj.password_compliance == 'not_submitted':
                return '❌ Нажата кнопка (форма не заполнена)'
            else:
                return '✅ Форма отправлена'
        else:
            return '💾 Автосохранение'
    button_clicked_status.short_description = 'Статус'
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'visited_at', 'user_agent_short']
    list_filter = ['visited_at']
    search_fields = ['ip_address']
    readonly_fields = ['ip_address', 'user_agent', 'visited_at']
    
    def user_agent_short(self, obj):
        return obj.user_agent[:50] + '...' if len(obj.user_agent) > 50 else obj.user_agent
    user_agent_short.short_description = 'User Agent (коротко)'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False