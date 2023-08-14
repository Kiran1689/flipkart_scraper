from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    url = models.URLField(max_length=1000)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    review_count = models.PositiveIntegerField()
    ratings_count = models.PositiveIntegerField()
    ratings = models.DecimalField(max_digits=3, decimal_places=2)
    media_count = models.PositiveIntegerField()

    def __str__(self):
        return self.title
