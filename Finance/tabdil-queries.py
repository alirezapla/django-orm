from django.db.models import Avg, Sum, Q, Count
from .models import *
from datetime import datetime, timedelta


def young_employees(job: str):
    return Employee.objects.filter(job=job, age__lt=30)


def cheap_products():
    avg = Product.objects.aggregate(price_avg=Avg("price"))
    x = (
        Product.objects.filter(price__lt=int(avg["price_avg"]))
        .order_by("price")
        .values("name")
    )
    names = []
    for i in x:
        names.append(i["name"])
    return names


def products_sold_by_companies():
    return Company.objects.annotate(sold=Sum("product__sold")).values_list(
        "name", "sold"
    )


def sum_of_income(start_date: str, end_date: str):
    return Order.objects.filter(
        Q(time__gte=datetime.strptime(start_date, "%Y-%m-%d").date())
        & Q(time__lt=datetime.strptime(end_date, "%Y-%m-%d").date())
    ).aggregate(sum=Sum("price"))["sum"]


def good_customers():

    return (
        Customer.objects.filter(
            order__time__date__lte=datetime.today(),
            order__time__date__gt=datetime.today() - timedelta(days=30),
        )
        .annotate(count=Count("order"))
        .filter(count__gt=10)
        .values_list("name", "phone")
    )


def nonprofitable_companies():
    x = (
        Company.objects.filter(product__sold__lt=100)
        .annotate(count=Count("name"))
        .filter(count__gte=4)
        .values("name")
    )
    names = []
    for i in x:
        names.append(i["name"])
    return names
