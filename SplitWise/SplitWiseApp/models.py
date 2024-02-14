from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class User(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default="abc")
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name



class Expense(models.Model):
    EQUAL = 'EQUAL'
    EXACT = 'EXACT'
    PERCENT = 'PERCENT'

    EXPENSE_TYPES = [
        (EQUAL, 'Equal'),
        (EXACT, 'Exact'),
        (PERCENT, 'Percent'),
    ]
    description = models.CharField(max_length=255,default=" ")
    expense_type = models.CharField(max_length=10, choices=EXPENSE_TYPES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default = 0.00)
    participants = models.ManyToManyField(User)
    MAX_PARTICIPANTS = 1000
    MAX_AMOUNT = 10000000 


    def clean(self):
        super().clean()
        if self.new_participants.count() > self.MAX_PARTICIPANTS:
            raise ValidationError("Expense can't have more than 1000 participants.")
        if self.total_amount > self.MAX_AMOUNT:
            raise ValidationError("Expense amount can't exceed INR 1,00,00,000/-.")

    def __str__(self):
        return f"{self.type} Expense ({self.total_amount})"


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    share = models.DecimalField(max_digits=12, decimal_places=2)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} ({self.user.username}): {self.amount} INR"

    class Meta:
        ordering = ['-timestamp']  # Show latest transactions first