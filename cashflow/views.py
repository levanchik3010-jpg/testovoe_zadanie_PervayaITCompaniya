from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import CashFlowRecord, SubCategory, TransactionType, Status, Category
from .serializers import CategorySerializer, SubCategorySerializer


@api_view(['GET'])
def get_categories(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(transaction_type_id=type_id)
    return Response(CategorySerializer(categories, many=True).data)


@api_view(['GET'])
def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id)
    return Response(SubCategorySerializer(subcategories, many=True).data)


def index(request):
    if request.method == 'POST':
        sub_cat_id = request.POST.get('sub_category')
        amount = request.POST.get('amount')
        comment = request.POST.get('comment', '').strip()
        status_id = request.POST.get('status')
        custom_date = request.POST.get('date')

        errors = []
        if not sub_cat_id:
            errors.append('Выберите подкатегорию.')
        if not amount:
            errors.append('Укажите сумму.')
        if not status_id:
            errors.append('Выберите статус.')

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            record = CashFlowRecord(
                sub_category_id=sub_cat_id,
                amount=amount,
                comment=comment or None,
                status_id=status_id
            )
            if custom_date:
                record.date = custom_date
            record.save()
            messages.success(request, 'Запись успешно добавлена.')
            return redirect('index')

    records = CashFlowRecord.objects.select_related(
        'status', 'sub_category__category__transaction_type'
    ).all().order_by('-date')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    filter_status = request.GET.get('status')
    filter_type = request.GET.get('type')
    filter_category = request.GET.get('category')
    filter_subcategory = request.GET.get('subcategory')

    if start_date:
        records = records.filter(date__gte=start_date)
    if end_date:
        records = records.filter(date__lte=end_date)
    if filter_status:
        records = records.filter(status_id=filter_status)
    if filter_type:
        records = records.filter(sub_category__category__transaction_type_id=filter_type)
    if filter_category:
        records = records.filter(sub_category__category_id=filter_category)
    if filter_subcategory:
        records = records.filter(sub_category_id=filter_subcategory)

    return render(request, 'cashflow/index.html', {
        'records': records,
        'types': TransactionType.objects.all(),
        'statuses': Status.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        'today': timezone.now().strftime('%Y-%m-%d'),
        'filter': {
            'start_date': start_date or '',
            'end_date': end_date or '',
            'status': filter_status or '',
            'type': filter_type or '',
            'category': filter_category or '',
            'subcategory': filter_subcategory or '',
        }
    })


def edit_record(request, record_id):
    record = get_object_or_404(CashFlowRecord, id=record_id)

    if request.method == 'POST':
        sub_cat_id = request.POST.get('sub_category')
        amount = request.POST.get('amount')
        status_id = request.POST.get('status')
        comment = request.POST.get('comment', '').strip()
        custom_date = request.POST.get('date')

        errors = []
        if not sub_cat_id:
            errors.append('Выберите подкатегорию.')
        if not amount:
            errors.append('Укажите сумму.')
        if not status_id:
            errors.append('Выберите статус.')

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            record.sub_category_id = sub_cat_id
            record.amount = amount
            record.status_id = status_id
            record.comment = comment or None
            if custom_date:
                record.date = custom_date
            record.save()
            messages.success(request, 'Запись успешно обновлена.')
            return redirect('index')

    return render(request, 'cashflow/edit.html', {
        'record': record,
        'types': TransactionType.objects.all(),
        'statuses': Status.objects.all(),
    })


def delete_record(request, record_id):
    if request.method == 'POST':
        get_object_or_404(CashFlowRecord, id=record_id).delete()
        messages.success(request, 'Запись удалена.')
    return redirect('index')