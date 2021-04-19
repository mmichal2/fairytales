from django.urls import path
from .views import BookListView, BookDetailView
from books.views import index
from books import views

urlpatterns = [
    path('bookstore/', views.bookstore, name="bookstore"),
    path('bookdetails/', views.book_details, name="book_details"),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/', views.subscribe, name='unsubscribe'),
    path('subscription/', views.subscription, name='subscription'),
    path('books/', BookListView.as_view(), name='book-list'),
   # path('books/<pk>', BookDetailView.as_view(), name='book-detail'),
    path('books/1/', views.book_detail_view),
    path('', index, name='index'),

]
