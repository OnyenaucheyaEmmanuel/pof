from django.db import models

class FormEntry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank_name = models.CharField(max_length=100)
    start_date = models.DateField()
    expiration_days = models.PositiveIntegerField()

    def __str__(self):
        return self.name
