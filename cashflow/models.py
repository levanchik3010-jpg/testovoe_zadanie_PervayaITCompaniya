from django.db import models
from django.utils import timezone

class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name="Статус")
    def __str__(self): return self.name

class TransactionType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип операции")
    def __str__(self): return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, verbose_name="Тип")
    def __str__(self): return f"{self.name} ({self.transaction_type.name})"

class SubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Подкатегория")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    def __str__(self): return self.name

class CashFlowRecord(models.Model):
    date = models.DateField(default=timezone.now, verbose_name="Дата")
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, verbose_name="Статус")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")