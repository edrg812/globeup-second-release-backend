from django.db import models


class WithdrawRequestByReseller(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='withdraw_requests')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method= models.CharField(max_length=100)
    account_details = models.TextField()

    requested_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Withdraw Request by {self.user.phone_number} for {self.amount}"