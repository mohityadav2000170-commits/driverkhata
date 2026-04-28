from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    ENTRY_TYPE = (
        ('ADD', 'Add Expense'),   # daily ₹200
        ('PAY', 'Payment'),       # payment to driver
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    type = models.CharField(max_length=10, choices=ENTRY_TYPE)
    note = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.amount}"