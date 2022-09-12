from django.db import models
from utils.models import CreateUpdateTracker

# Create your models here.


class Product(CreateUpdateTracker):
    title = models.CharField(max_length=128, verbose_name="Nomi")
    price = models.CharField(max_length=128, verbose_name="narxi")
    amount = models.DecimalField(
        max_digits=19, decimal_places=2, editable=False, default=0)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"


AMOUNT_TYPE = (
    ("plus", "Qo'shish"),
    ("minus", "Ayirish")
)


class ProductAmount(CreateUpdateTracker):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='amount')
    amount = models.DecimalField(
        max_digits=19, decimal_places=2, editable=False, default=0)
    type = models.CharField(max_length=10, choices=AMOUNT_TYPE)

    def __str__(self) -> str:
        return f"{self.amount}-{self.type}"

    class Meta:
        verbose_name = "Mahsulot soni"
        verbose_name_plural = "Mahsulot sonlari"
