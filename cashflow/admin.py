from django.contrib import admin
from .models import Status, TransactionType, Category, SubCategory, CashFlowRecord


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'transaction_type')
    list_filter = ('transaction_type',)
    search_fields = ('name',)
    ordering = ('transaction_type__name', 'name')


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_type')
    list_filter = ('category__transaction_type', 'category')
    search_fields = ('name',)
    ordering = ('category__name', 'name')

    @admin.display(description='Тип', ordering='category__transaction_type__name')
    def get_type(self, obj):
        return obj.category.transaction_type.name