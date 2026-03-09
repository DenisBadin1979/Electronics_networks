from django.db import models
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.model})"


class Contact(models.Model):
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.city}, {self.street} {self.house_number}"


class NetworkNode(models.Model):
    name = models.CharField(max_length=255)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='node')
    products = models.ManyToManyField(Product, related_name='nodes')
    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='distributors'
    )
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(editable=False, default=0)

    def save(self, *args, **kwargs):
        # Автоматический расчёт уровня иерархии
        if self.supplier:
            if self.supplier.level >= 2:
                raise ValidationError("Нельзя создать звено с поставщиком уровня 2 (максимальный уровень).")
            self.level = self.supplier.level + 1
        else:
            self.level = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name