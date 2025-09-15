from django.db import models

# Create your models here.

class IPBlock(models.Model):
    id = models.AutoField(primary_key=True)
    ip_number = models.GenericIPAddressField()
    reason = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_number} - {self.reason[:50]}"


