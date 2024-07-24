from django.urls import path
from . import views

urlpatterns = [
    path('book/list/', views.book_list),
    path('review/add/', views.add_review),
    path('review/update/', views.update_review),
    path('review/delete/', views.delete_review),
    path('suggest/', views.suggest_book),
]
