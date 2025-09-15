from django.db import models
from user.models import User


class Earning(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("on_hold", "On Hold"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="earnings")
    
    # 💰 Balances which is withdrawable
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    #total reselling price
    total_sales_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    pending_payout = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    completed_payout = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    #reseller commission
    # 💰 Commission percentage (fixed, not to be used as money)
    commission_percent = models.DecimalField(
        max_digits=5, decimal_places=2, default=95.00,
        help_text="Reseller commission percentage"
    )

    # total balance= reselling_price- wholesale price
    total_commission_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    
    # Last user withdrawal request
    user_requested_amount_withdraw = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # 📊 Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.phone_number} | Balance: {self.current_balance} | Status: {self.status}"

    # 🔹 User requests a withdrawal
    def request_withdraw(self, amount):
        """Move money from balance into pending payout."""
        if amount <= 0:
            return False, "Invalid amount"
        if self.current_balance < amount:
            return False, "Not enough balance"

        self.current_balance -= amount
        self.pending_payout += amount
        self.user_requested_amount_withdraw = amount
        self.status = "pending"
        self.save()
        return True, "Withdrawal request submitted"

    # 🔹 Mark payout as paid
    def mark_as_paid(self):
        """Move money from pending to completed payout."""
        if self.user_requested_amount_withdraw > 0 and self.pending_payout >= self.user_requested_amount_withdraw:
            amount = self.user_requested_amount_withdraw

            self.pending_payout -= amount
            self.completed_payout += amount
            self.user_requested_amount_withdraw = 0
            self.status = "paid"
            self.save()
            return True, f"{amount} marked as paid"

        return False, "No pending payout to complete"

   
    
    def mark_as_failed(self):
        """Return money to current balance if payout failed."""
        if self.status == "pending" and self.user_requested_amount_withdraw > 0:
            amount = self.user_requested_amount_withdraw
            
            # Return the money to current balance
            self.current_balance += amount
            self.pending_payout -= amount
            self.user_requested_amount_withdraw = 0
            self.status = "failed"
            self.save()
            return True, f"{amount} returned to balance"
        
        return False, "No pending withdrawal to fail"


















