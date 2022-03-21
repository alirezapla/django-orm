from email.mime import base
from django.db.models import F, Sum, Count, Case, When, Min, Q, Max
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
    _max = 1
    departments = (
        Project.objects.filter(
            Q(estimated_end_time__date__gte=F("end_time__date"))
            & Q(estimated_end_time__hour__gte=F("end_time__hour"))
            & Q(estimated_end_time__minute__gte=F("end_time__minute"))
        )
        .values("department_id")
        .annotate(Count("department_id"))
    )
    for department in departments:
        print(department)
        if _max < department["department_id__count"]:
            _max = department["department_id__count"]
            emply = department["department_id"]

    print(Department.objects.filter(id=emply))
    return Department.objects.filter(id=emply).first()


def query_9(x):
    min_late = 0
    employees = (
        Attendance.objects.filter(Q(in_time__hour__gt=x) & Q(in_time__minute__gt=0))
        .values("employee", "in_time", "employee__account__username")
        .annotate(late_count=Count("employee"))
        # .order_by("employee__account__username")
    )
    # return employess
    for i, employee in enumerate(employees):
        print(employee)
        if min_late >= employee["late_count"] or i == 0:
            min_late = employee["late_count"]
            emply = employee["employee"]

    print(Employee.objects.filter(id=emply).values("id", "account__username"))
    return Employee.objects.filter(id=emply).first()


def query_10():
    return {
        "total": Employee.objects.count()
        - Project.objects.filter(employeeprojectrelation__isnull=False)
        .annotate(Count("employees__id", distinct=True))
        .count()
    }
