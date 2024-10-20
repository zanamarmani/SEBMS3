
from django.http import JsonResponse
from django.db.models import Count, Sum, Q 
from bill.models import Bill
def bills_per_month(request):
    # Example data: Total bills and paid bills per month
    bills_data = Bill.objects.all().annotate(
        total_bills=Count('id'),
        paid_bills=Count('id', filter=Q(paid=True))
    ).order_by('month')

    labels = [data['month'].strftime('%Y-%m') for data in bills_data]
    total_bills = [data['total_bills'] for data in bills_data]
    paid_bills = [data['paid_bills'] for data in bills_data]

    return JsonResponse({
        'labels': labels,
        'total_bills': total_bills,
        'paid_bills': paid_bills
    })



def bills_per_year(request):
    bills_data = Bill.objects.values('month__year').annotate(
        paid_bills=Count('id', filter=Q(paid=True)),
        unpaid_bills=Count('id', filter=Q(paid=False))
    ).order_by('month__year')

    labels = [str(data['month__year']) for data in bills_data]
    paid_bills = [data['paid_bills'] for data in bills_data]
    unpaid_bills = [data['unpaid_bills'] for data in bills_data]

    return JsonResponse({
        'labels': labels,
        'paid_bills': paid_bills,
        'unpaid_bills': unpaid_bills
    })
