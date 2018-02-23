from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('documents/', views.DocumentListView.as_view(), name='documents'),
    path('document/<int:pk>', views.DocumentDetailView.as_view(), name='document-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('add_book/', views.add_book, name='add_book'),
    path('document/<int:pk>/claim/', views.claim_document, name='claim'),
    path('add_article/', views.add_article, name='add_article')
]
