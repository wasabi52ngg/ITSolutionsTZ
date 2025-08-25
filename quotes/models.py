from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Source(models.Model):
    """Модель для источников цитат (фильмы, книги и т.д.)"""
    name = models.CharField(max_length=200, verbose_name="Название источника")
    type = models.CharField(
        max_length=50, 
        choices=[
            ('movie', 'Фильм'),
            ('book', 'Книга'),
            ('series', 'Сериал'),
            ('other', 'Другое'),
        ],
        default='other',
        verbose_name="Тип источника"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники"
        unique_together = ['name', 'type']
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"
    
    @property
    def quotes_count(self):
        return self.quotes.count()


class Quote(models.Model):
    """Модель для цитат"""
    text = models.TextField(verbose_name="Текст цитаты")
    author = models.CharField(max_length=100, blank=True, verbose_name="Автор")
    source = models.ForeignKey(
        Source, 
        on_delete=models.CASCADE, 
        related_name='quotes',
        verbose_name="Источник"
    )
    weight = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Вес цитаты (1-10)"
    )
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    likes_count = models.PositiveIntegerField(default=0, verbose_name="Количество лайков")
    dislikes_count = models.PositiveIntegerField(default=0, verbose_name="Количество дизлайков")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.text[:50]}..."
    
    def increment_views(self):
        """Увеличивает счетчик просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def like(self):
        """Увеличивает счетчик лайков"""
        self.likes_count += 1
        self.save(update_fields=['likes_count'])
    
    def dislike(self):
        """Увеличивает счетчик дизлайков"""
        self.dislikes_count += 1
        self.save(update_fields=['dislikes_count'])
    
    @property
    def popularity_score(self):
        """Вычисляет популярность цитаты"""
        return self.likes_count - self.dislikes_count
    
    @property
    def display_text(self):
        """Возвращает текст цитаты с кавычками"""
        return f'"{self.text}"'


class Vote(models.Model):
    """Модель для отслеживания голосов пользователей"""
    VOTE_CHOICES = [
        ('like', 'Лайк'),
        ('dislike', 'Дизлайк'),
    ]
    
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='votes')
    session_id = models.CharField(max_length=100, verbose_name="ID сессии")
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICES, verbose_name="Тип голоса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата голоса")
    
    class Meta:
        verbose_name = "Голос"
        verbose_name_plural = "Голоса"
        unique_together = ['quote', 'session_id']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_vote_type_display()} для цитаты {self.quote.id}"
