from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.RandomQuoteView.as_view(), name='random_quote'),
    path('add/', views.AddQuoteView.as_view(), name='add_quote'),
    path('popular/', views.PopularQuotesView.as_view(), name='popular_quotes'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('like/<int:quote_id>/', views.LikeQuoteView.as_view(), name='like_quote'),
    path('dislike/<int:quote_id>/', views.DislikeQuoteView.as_view(), name='dislike_quote'),
]
