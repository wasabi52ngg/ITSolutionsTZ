import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import TemplateView, FormView, View
from django.urls import reverse_lazy
from .models import Quote, Source, Vote
from .forms import QuoteForm
from django.db import models


class RandomQuoteView(TemplateView):
    """Главная страница с случайной цитатой"""
    template_name = 'quotes/random_quote.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quotes = list(Quote.objects.all())
        
        if not quotes:
            context['quote'] = None
            context['no_quotes'] = True
            return context
        
        weighted_quotes = []
        for quote in quotes:
            weighted_quotes.extend([quote] * quote.weight)
        
        selected_quote = random.choice(weighted_quotes)
        selected_quote.increment_views()
        
        session_id = self.request.session.session_key
        if not session_id:
            self.request.session.create()
            session_id = self.request.session.session_key
        
        user_vote = None
        if session_id:
            try:
                user_vote = Vote.objects.get(quote=selected_quote, session_id=session_id)
            except Vote.DoesNotExist:
                pass
        
        context['quote'] = selected_quote
        context['no_quotes'] = False
        context['user_vote'] = user_vote
        
        return context


class AddQuoteView(FormView):
    """Страница добавления новой цитаты"""
    template_name = 'quotes/add_quote.html'
    form_class = QuoteForm
    success_url = reverse_lazy('quotes:random_quote')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Цитата успешно добавлена!')
        return super().form_valid(form)


class PopularQuotesView(TemplateView):
    """Страница с популярными цитатами"""
    template_name = 'quotes/popular_quotes.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        sort_by = self.request.GET.get('sort', 'likes')
        source_type = self.request.GET.get('type', '')
        search = self.request.GET.get('search', '')
        
        quotes = Quote.objects.all()
        
        if source_type:
            quotes = quotes.filter(source__type=source_type)
        
        if search:
            quotes = quotes.filter(
                Q(text__icontains=search) |
                Q(author__icontains=search) |
                Q(source__name__icontains=search)
            )
        
        if sort_by == 'likes':
            quotes = quotes.order_by('-likes_count', '-views_count')
        elif sort_by == 'views':
            quotes = quotes.order_by('-views_count', '-likes_count')
        elif sort_by == 'popularity':
            quotes = quotes.annotate(
                popularity=models.F('likes_count') - models.F('dislikes_count')
            ).order_by('-popularity', '-views_count')
        elif sort_by == 'recent':
            quotes = quotes.order_by('-created_at')
        
        paginator = Paginator(quotes, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        total_quotes = Quote.objects.count()
        total_sources = Source.objects.count()
        total_views = Quote.objects.aggregate(
            total=models.Sum('views_count')
        )['total'] or 0
        total_likes = Quote.objects.aggregate(
            total=models.Sum('likes_count')
        )['total'] or 0
        
        session_id = self.request.session.session_key
        user_votes = {}
        if session_id:
            votes = Vote.objects.filter(
                quote__in=page_obj,
                session_id=session_id
            ).select_related('quote')
            user_votes = {vote.quote_id: vote.vote_type for vote in votes}
        
        context.update({
            'page_obj': page_obj,
            'total_quotes': total_quotes,
            'total_sources': total_sources,
            'total_views': total_views,
            'total_likes': total_likes,
            'user_votes': user_votes,
            'current_sort': sort_by,
            'current_type': source_type,
            'current_search': search,
        })
        
        return context


class DashboardView(TemplateView):
    """Страница статистики (дашборд)"""
    template_name = 'quotes/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        total_quotes = Quote.objects.count()
        total_views = Quote.objects.aggregate(
            total=models.Sum('views_count')
        )['total'] or 0
        total_likes = Quote.objects.aggregate(
            total=models.Sum('likes_count')
        )['total'] or 0
        total_dislikes = Quote.objects.aggregate(
            total=models.Sum('dislikes_count')
        )['total'] or 0
        
        top_liked_quotes = Quote.objects.order_by('-likes_count')[:10]
        
        top_viewed_quotes = Quote.objects.order_by('-views_count')[:10]
        
        source_stats = Source.objects.values('type').annotate(
            quotes_count=models.Count('quotes'),
            total_views=models.Sum('quotes__views_count'),
            total_likes=models.Sum('quotes__likes_count'),
            total_dislikes=models.Sum('quotes__dislikes_count')
        ).order_by('-quotes_count')
        
        best_ratio_quotes = Quote.objects.annotate(
            ratio=models.Case(
                models.When(dislikes_count=0, then=models.F('likes_count')),
                default=models.F('likes_count') * 1.0 / models.F('dislikes_count')
            )
        ).filter(likes_count__gt=0).order_by('-ratio')[:5]
        
        recent_quotes = Quote.objects.order_by('-created_at')[:5]
        
        context.update({
            'total_quotes': total_quotes,
            'total_views': total_views,
            'total_likes': total_likes,
            'total_dislikes': total_dislikes,
            'top_liked_quotes': top_liked_quotes,
            'top_viewed_quotes': top_viewed_quotes,
            'source_stats': source_stats,
            'best_ratio_quotes': best_ratio_quotes,
            'recent_quotes': recent_quotes,
        })
        
        return context


class LikeQuoteView(View):
    """AJAX endpoint для лайка цитаты"""
    
    def post(self, request, quote_id):
        quote = get_object_or_404(Quote, id=quote_id)
        session_id = request.session.session_key
        
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        
        try:
            existing_vote = Vote.objects.get(quote=quote, session_id=session_id)
            if existing_vote.vote_type == 'like':
                return JsonResponse({
                    'success': False, 
                    'message': 'Вы уже поставили лайк этой цитате'
                })
            elif existing_vote.vote_type == 'dislike':
                existing_vote.vote_type = 'like'
                existing_vote.save()
                quote.dislikes_count -= 1
                quote.likes_count += 1
                quote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(quote=quote, session_id=session_id, vote_type='like')
            quote.like()
        
        return JsonResponse({
            'success': True,
            'likes_count': quote.likes_count,
            'dislikes_count': quote.dislikes_count,
            'message': 'Лайк добавлен!'
        })


class DislikeQuoteView(View):
    """AJAX endpoint для дизлайка цитаты"""
    
    def post(self, request, quote_id):
        quote = get_object_or_404(Quote, id=quote_id)
        session_id = request.session.session_key
        
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        
        try:
            existing_vote = Vote.objects.get(quote=quote, session_id=session_id)
            if existing_vote.vote_type == 'dislike':
                return JsonResponse({
                    'success': False, 
                    'message': 'Вы уже поставили дизлайк этой цитате'
                })
            elif existing_vote.vote_type == 'like':
                existing_vote.vote_type = 'dislike'
                existing_vote.save()
                quote.likes_count -= 1
                quote.dislikes_count += 1
                quote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(quote=quote, session_id=session_id, vote_type='dislike')
            quote.dislike()
        
        return JsonResponse({
            'success': True,
            'likes_count': quote.likes_count,
            'dislikes_count': quote.dislikes_count,
            'message': 'Дизлайк добавлен!'
        })
