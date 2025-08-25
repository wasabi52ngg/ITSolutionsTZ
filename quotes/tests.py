from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Source, Quote, Vote
from .forms import QuoteForm
import json


class SourceModelTest(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            name="Тестовый фильм",
            type="movie"
        )
    
    def test_source_creation(self):
        self.assertEqual(self.source.name, "Тестовый фильм")
        self.assertEqual(self.source.type, "movie")
    
    def test_source_quotes_count(self):
        Quote.objects.create(
            text="Тестовая цитата",
            source=self.source,
            weight=5
        )
        self.assertEqual(self.source.quotes_count, 1)


class QuoteModelTest(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            name="Тестовый фильм",
            type="movie"
        )
        self.quote = Quote.objects.create(
            text="Тестовая цитата",
            author="Тестовый автор",
            source=self.source,
            weight=5
        )
    
    def test_quote_creation(self):
        self.assertEqual(self.quote.text, "Тестовая цитата")
        self.assertEqual(self.quote.author, "Тестовый автор")
        self.assertEqual(self.quote.weight, 5)
    
    def test_quote_increment_views(self):
        initial_views = self.quote.views_count
        self.quote.increment_views()
        self.assertEqual(self.quote.views_count, initial_views + 1)
    
    def test_quote_like(self):
        initial_likes = self.quote.likes_count
        self.quote.like()
        self.assertEqual(self.quote.likes_count, initial_likes + 1)


class QuoteFormTest(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            name="Тестовый фильм",
            type="movie"
        )
    
    def test_valid_form(self):
        form_data = {
            'text': 'Тестовая цитата',
            'author': 'Тестовый автор',
            'source_name': 'Новый фильм',
            'source_type': 'movie',
            'weight': 7
        }
        form = QuoteForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_missing_text(self):
        form_data = {
            'author': 'Тестовый автор',
            'source_name': 'Новый фильм',
            'source_type': 'movie',
            'weight': 7
        }
        form = QuoteForm(data=form_data)
        self.assertFalse(form.is_valid())


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.source = Source.objects.create(
            name="Тестовый фильм",
            type="movie"
        )
        self.quote = Quote.objects.create(
            text="Тестовая цитата",
            author="Тестовый автор",
            source=self.source,
            weight=5
        )
    
    def test_random_quote_view(self):
        response = self.client.get(reverse('quotes:random_quote'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовая цитата")
    
    def test_add_quote_view_get(self):
        response = self.client.get(reverse('quotes:add_quote'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Добавить новую цитату")
    
    def test_add_quote_view_post(self):
        form_data = {
            'text': 'Новая цитата',
            'author': 'Новый автор',
            'source_name': 'Новый фильм',
            'source_type': 'movie',
            'weight': 8
        }
        response = self.client.post(reverse('quotes:add_quote'), form_data)
        self.assertEqual(response.status_code, 302)
        
        new_quote = Quote.objects.get(text='Новая цитата')
        self.assertEqual(new_quote.author, 'Новый автор')
    
    def test_popular_quotes_view(self):
        response = self.client.get(reverse('quotes:popular_quotes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Популярные цитаты")
    
    def test_like_quote_view(self):
        response = self.client.post(
            reverse('quotes:like_quote', args=[self.quote.id]),
            {},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['likes_count'], 1)
