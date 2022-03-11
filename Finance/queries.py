from email.mime import base
from django.db.models import F, Sum, Count, Case, When
from .models import *


def query_0():
    q = Employee.objects.all()
    return q


def query_1():
    saleries = (
        Payslip.objects.filter(payment_id=None, id__lte=24)
        .values("base", "tax", "insurance", "overtime")
        .aggregate(
            total_dept=(Sum("base") + Sum("tax") + Sum("insurance") + Sum("overtime"))
        )
    )
    return saleries


def query_2():
    return (
        Attendance.objects.filter(late_cause=None)
        .exclude(id=15)
        .order_by("id")
        .values("id")
    )


def query_3():
    return Payment.objects.filter(description="salary").aggregate(total=Sum("amount"))


def query_4(x):
    # TODO
    pass


def query_5(x):
    # TODO
    pass


def query_6():
    # TODO
    pass


def query_7():
    # TODO
    pass


def query_8():
    # TODO
    pass


def query_9(x):
    # TODO
    pass


def query_10():
    return {
        "total": Employee.objects.count()
        - Project.objects.filter(employeeprojectrelation__isnull=False)
        .annotate(Count("employees__id", distinct=True))
        .count()
    }
