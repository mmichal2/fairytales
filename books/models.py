
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# Books model

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="books"
    )
    author = models.ForeignKey(
        Author, on_delete=models.PROTECT, related_name="books"
    )
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} {self.description} {self.category} {self.author}"


# Subscription model

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="books")
    active = models.BooleanField(default=True)
    subscription_date = models.DateField(null=True)
    payment_type = models.CharField(max_length=80, null=True)
    payment_id = models.CharField(max_length=80, null=True)

    def subscribe(self, book_id):
        book = Book.objects.get(pk=book_id)
        try:
            already_subscribed = BookSubscription.objects.get(book=book, subscription=self)
            already_subscribed.quantity += 1
            already_subscribed.save()
        except BookSubscription.DoesNotExist:
            new_subscription = BookSubscription.objects.create(
                book=book,
                subscription=self,
                quantiti=1
            )
            new_subscription.save()

    def remove_subscription(self, book_id):
        book = Book.objects.get(pk=book_id)
        try:
            already_subscribed = BookSubscription.objects.get(book=book, subscription=self)
            if already_subscribed.quantity > 1:
                already_subscribed.quantity -= 1
                already_subscribed.save()
            else:
                already_subscribed.delete()
        except BookSubscription.DoesNotExist:
            pass


class BookSubscription(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="books")
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT, related_name="books")
    quantity = models.IntegerField()