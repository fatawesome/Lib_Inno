from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('documents/', views.DocumentListView.as_view(), name='documents'),
    path('my_documents/<int:pk>/', views.my_documents, name='my_documents'),
    path('document/<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_book/', views.add_book, name='add_book'),
    path('add_audio/', views.add_audio, name='add_audio'),
    path('add_video/', views.add_video, name='add_video'),
    path('add_copies/<int:pk>/', views.add_copies, name='add_copies'),
    path('document/<int:pk>/claim/', views.claim, name='claim'),
    path('document/<int:pk>/take/<int:doc_id>', views.take_document, name='take'),
    path('document/<int:pk>/delete/', views.delete_document, name='delete'),
    path('document/<int:pk>/editdocument/', views.edit_document, name='editdocument'),
    path('add_article/', views.add_article, name='add_article'),
    path('document/<int:pk>/ask/<int:doc_id>', views.ask_for_return, name='ask'),
]
