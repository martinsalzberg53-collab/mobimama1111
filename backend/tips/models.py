from django.db import models
from django.conf import settings
# Create your models here.

class Tip(models.Model):
    CATEGORY_CHOICES = [
        ('NUTRITION', 'Nutrition'),
        ('EXERCISE', 'Exercise'),
        ('MENTAL_HEALTH', 'Mental Health'),
        ('FIRST_TRIMESTER', 'First Trimester'),
        ('SECOND_TRIMESTER', 'Second Trimester'),
        ('THIRD_TRIMESTER', 'Third Trimester'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role':'ADMIN'},  # ONLY ADMIN
    )

    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title