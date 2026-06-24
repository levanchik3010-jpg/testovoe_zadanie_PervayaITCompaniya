from django.contrib import admin
from .models import Status, TransactionType, Category, SubCategory, CashFlowRecord

@admin.register(Status, TransactionType)
class SimpleAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'transaction_type')
    list_filter = ('transaction_type',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

@admin.register(CashFlowRecord)
class CashFlowRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'status', 'sub_category', 'amount', 'comment')
    list_filter = ('date', 'status', 'sub_category__category__transaction_type')