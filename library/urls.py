from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('documents/', views.DocumentListView.as_view(), name='documents'),
    path('my_documents/<int:pk>/', views.my_documents, name='my_documents'),
    path('document/<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('add_book/', views.add_book, name='add_book'),
    path('add_audio/', views.add_audio, name='add_audio'),
    path('add_video/', views.add_video, name='add_video'),
    path('add_copies/<int:pk>/', views.add_copies, name='add_copies'),
    path('remove_copies/<int:pk>/', views.remove_copies, name='remove_copies'),
    path('document/<int:doc_id>/give/<int:user_id>', views.give_document, name='give_document'),
    path('document/<int:doc_id>/increase_user_priority/<int:user_id>', views.increase_user_priority, name='increase_user_priority'),
    path('document/<int:doc_id>/reserve/', views.reserve, name='reserve'),
    path('document/<int:doc_id>/get_in_queue/', views.get_in_queue, name='get_in_queue'),
    path('document/<int:doc_id>/quit_queue/', views.quit_queue, name='quit_queue'),
    path('document/<int:pk>/take/<int:user_id>', views.take_document, name='take'),
    path('document/<int:pk>/delete_copy/<int:user_id>', views.delete_copy, name='delete_copy'),
    path('document/<int:pk>/delete/', views.delete_document, name='delete'),
    path('document/<int:pk>/editdocument/', views.edit_document, name='editdocument'),
    path('add_article/', views.add_article, name='add_article'),
    path('document/<int:pk>/ask/<int:user_id>', views.ask_for_return, name='ask'),
]
