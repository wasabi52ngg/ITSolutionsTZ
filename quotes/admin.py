from django.contrib import admin
from django.utils.html import format_html
from .models import Quote, Source, Vote


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'quotes_count', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['name']
    ordering = ['-created_at']
    
    def quotes_count(self, obj):
        return obj.quotes_count
    quotes_count.short_description = 'Количество цитат'


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'author', 'source', 'weight', 'views_count', 'likes_count', 'dislikes_count', 'popularity_score', 'created_at']
    list_filter = ['source__type', 'weight', 'created_at']
    search_fields = ['text', 'author', 'source__name']
    ordering = ['-created_at']
    readonly_fields = ['views_count', 'likes_count', 'dislikes_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('text', 'author', 'source', 'weight')
        }),
        ('Статистика', {
            'fields': ('views_count', 'likes_count', 'dislikes_count'),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def text_preview(self, obj):
        return format_html('<div style="max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{}</div>', obj.text)
    text_preview.short_description = 'Текст цитаты'
    
    def popularity_score(self, obj):
        score = obj.popularity_score
        if score > 0:
            color = 'green'
            icon = '👍'
        elif score < 0:
            color = 'red'
            icon = '👎'
        else:
            color = 'gray'
            icon = '➖'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color, icon, score
        )
    popularity_score.short_description = 'Популярность'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('source')
    
    def save_model(self, request, obj, form, change):
        if not change:
            if obj.source.quotes.count() >= 3:
                self.message_user(
                    request,
                    f'У источника "{obj.source.name}" уже есть максимальное количество цитат (3).',
                    level='WARNING'
                )
        
        super().save_model(request, obj, form, change)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['quote_preview', 'vote_type', 'session_id', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['quote__text', 'session_id']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    def quote_preview(self, obj):
        return format_html('<div style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{}</div>', obj.quote.text)
    quote_preview.short_description = 'Цитата'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('quote')
