from django.db import models



class ShippingCharge(models.Model):
    area = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.area} - ${self.amount}"
