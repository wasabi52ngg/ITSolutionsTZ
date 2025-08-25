from django import forms
from django.core.exceptions import ValidationError
from .models import Quote, Source


class QuoteForm(forms.ModelForm):
    """Форма для добавления новой цитаты"""
    source_name = forms.CharField(
        max_length=200,
        label="Название источника",
        help_text="Введите название фильма, книги или другого источника"
    )
    source_type = forms.ChoiceField(
        choices=Source._meta.get_field('type').choices,
        label="Тип источника",
        initial='other'
    )
    
    class Meta:
        model = Quote
        fields = ['text', 'author', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Введите текст цитаты...'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Автор цитаты'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'type': 'range'
            })
        }
        labels = {
            'text': 'Текст цитаты',
            'author': 'Автор',
            'weight': 'Вес цитаты (1-10)'
        }
        help_texts = {
            'weight': 'Чем выше вес, тем больше шанс показа цитаты на главной странице'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        source_name = cleaned_data.get('source_name')
        source_type = cleaned_data.get('source_type')
        
        if text and source_name and source_type:
            source, created = Source.objects.get_or_create(
                name=source_name,
                type=source_type
            )
            
            if Quote.objects.filter(text__iexact=text, source=source).exists():
                raise ValidationError(
                    "Цитата с таким текстом уже существует у этого источника."
                )
            
            if not created and source.quotes.count() >= 3:
                raise ValidationError(
                    f"У источника '{source_name}' уже есть максимальное количество цитат (3)."
                )
        
        return cleaned_data
    
    def save(self, commit=True):
        quote = super().save(commit=False)
        
        source, created = Source.objects.get_or_create(
            name=self.cleaned_data['source_name'],
            type=self.cleaned_data['source_type']
        )
        
        quote.source = source
        
        if commit:
            quote.save()
        
        return quote
