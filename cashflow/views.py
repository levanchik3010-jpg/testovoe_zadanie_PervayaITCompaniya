from django.shortcuts import render, redirect, get_object_or_404
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
        comment = request.POST.get('comment')
        status_id = request.POST.get('status')
        custom_date = request.POST.get('date')

        if sub_cat_id and amount:
            record = CashFlowRecord(
                sub_category_id=sub_cat_id,
                amount=amount,
                comment=comment,
                status_id=status_id
            )
            if custom_date:
                record.date = custom_date
            record.save()
            return redirect('index')

    records = CashFlowRecord.objects.all().order_by('-date')

    if request.GET.get('start_date'): records = records.filter(date__gte=request.GET.get('start_date'))
    if request.GET.get('end_date'): records = records.filter(date__lte=request.GET.get('end_date'))
    if request.GET.get('status'): records = records.filter(status_id=request.GET.get('status'))
    if request.GET.get('type'): records = records.filter(
        sub_category__category__transaction_type_id=request.GET.get('type'))
    if request.GET.get('category'): records = records.filter(sub_category__category_id=request.GET.get('category'))
    if request.GET.get('subcategory'): records = records.filter(sub_category_id=request.GET.get('subcategory'))

    return render(request, 'cashflow/index.html', {
        'records': records,
        'types': TransactionType.objects.all(),
        'statuses': Status.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        'today': timezone.now().strftime('%Y-%m-%d')
    })


def edit_record(request, record_id):
    record = get_object_or_404(CashFlowRecord, id=record_id)
    if request.method == 'POST':
        record.amount = request.POST.get('amount')
        record.comment = request.POST.get('comment')
        if request.POST.get('date'):
            record.date = request.POST.get('date')
        record.save()
        return redirect('index')
    return render(request, 'cashflow/edit.html', {'record': record})


def delete_record(request, record_id):
    get_object_or_404(CashFlowRecord, id=record_id).delete()
    return redirect('index')