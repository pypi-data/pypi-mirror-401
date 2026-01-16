from django.db import models

class Receipt(models.Model):
    receipt_date = models.DateField(blank=False, null=False)
    receipt_value = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)
    description = models.TextField("Description", blank=False, null=False)
    document = models.TextField(blank=False, nulll=False)
    observation = models.TextField(blank=True, null=True)
    
    
    