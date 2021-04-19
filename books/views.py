from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Book, BookSubscription, Subscription
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    return render(
        request,
        template_name='index_books.html',
    )


def bookstore(request):
    books = Book.objects.all()
    context = {'books': books}

    return render(request, 'base.html', context)


def home_view(request, *args, **kwargs):
    return render(request, 'home.html', {})


def book_detail_view(request, *args, **kwargs):
    try:
        obj = Book.objects.get(id=1)
    except Book.DoesNotExist:
        raise Http404

    return HttpResponse(f"Book id {obj.id}")


def book_details(request, book_id):
    context = {
        'book': Book.objects.get(pk=book_id)
    }
    return render(request, 'detail.html', context)


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_list.html'


def subscribe(request, book_id):
    if request.user.is_authenticated():
        try:
            book = Book.objects.get(pk=book_id)
        except ObjectDoesNotExist:
            pass
        else:
            try:
                subscription = Subscription.objects.get(user=request.user, active=True)
            except ObjectDoesNotExist:
                subscription = Subscription.objects.create(user=request.user)
                subscription.save()
            subscription.subscribe(book_id)
        return redirect('subscription')
    else:
        return redirect('index')


def unsubscribe(request, book_id):
    if request.user.is_authenticated():
        try:
            books = Book.objects.get(pk=book_id)
        except ObjectDoesNotExist:
            pass
        else:
            subscription = Subscription.objects.get(user=request.user, active=True)
            subscription.unsubscribe(book_id)
        return redirect('subscription')
    else:
        return redirect('index')


def subscription(request):
    if request.user.is_authenticated():
        subscription = Subscription.objects.filter(user=request.user.id, active=True)
        orders = BookSubscription.objects.filter(subscription=subscription)
        total = 0
        count = 0
        for order in orders:
            total += (order.book.price * order.quantity)
            count += order.quantity
        context = {
            'subscription': orders,
            'total': total,
            'count': count,
        }
        return render(request, 'subscription.html', context)
    else:
        return redirect('index')