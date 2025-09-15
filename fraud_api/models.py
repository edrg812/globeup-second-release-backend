from django.db import models

# Create your models here.
from django.db import models

class FraudAPI(models.Model):
    API_TYPE_CHOICES = [
        ('ip', 'IP Fraud Detection'),
        ('email', 'Email Fraud Detection'),
        ('phone', 'Phone Fraud Detection'),
        ('custom', 'Custom API'),
    ]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=API_TYPE_CHOICES, default="Phone Fraud Detection")
    api_url = models.URLField()
    api_key = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.api_url}"



