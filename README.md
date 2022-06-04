# django-orm


##### Table of Contents  
[Intro](#Intro)  
[Methods that return new QuerySets](#Methods-that-return-new-QuerySets)  
[Operators that return new QuerySets](#Operators-that-return-new-QuerySets)  
[Methods that do not return QuerySets](#Methods-that-do-not-return-QuerySets)   
[Aggregation functions](#Aggregation-functions)  
[Query-related tools](#Query-related-tools)   
<a name="Intro"/>
<a name="Methods-that-return-new-QuerySets"/>
<a name="Operators-that-return-new-QuerySets"/>
<a name="Methods-that-do-not-return-QuerySets"/> 
<a name="Aggregation-functions"/>
<a name="Query-related-tools"/>
 




# Intro
Current ```Django``` Version: [3.0](https://docs.djangoproject.com/en/3.0/ref/models/querysets/)

you can add the dataset to your database :

```python
python manage.py loaddata Finance/fixtures/auth_sample.json
python manage.py loaddata Finance/fixtures/data_sample.json
````



# Methods that return new [QuerySets](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#methods-that-return-new-querysets)

****
## ATTENDANCE MODEL
|id	|date	|in_time	|out_time	|late_cause	|employee_id|
| :---: | :---: | :---: | :---: | :---: | :---: | 
|15	|2017-12-21	|09:13:31	|19:34:10	|NULL	|116|
|18	|2017-08-03	|08:34:20	|19:24:23	|NULL	|122|
|20	|2017-12-07	|11:44:22	|18:40:31	|NULL	|119|
|23	|2017-09-30	|09:07:14	|19:55:12	|NULL	|127|
|30	|2018-01-21	|10:43:14	|19:37:34	|NULL	|127|
|31	|2018-03-18	|10:20:21	|18:12:46	|NULL	|127|


**Can be chained:**


```python
Attendance.objects.filter(late_cause=None)
        .exclude(id=15)
        .order_by("id")
        .values("id")
```
````python
Attendance : <QuerySet [{'id': 18}, {'id': 20}, {'id': 23}, {'id': 30}, {'id':31}]>
````

****
## PROJECT MODEL
|id|title|estimated_end_time|end_time|department_id|
| :---: | :---: | :---: | :---: | :---: | 
|13|Torrance|2015-06-10 00:26:12.473000|2003-03-08 14:25:37.396000|10|
|21|Brannon|2004-01-18 04:08:10.534000|2001-10-11 05:20:13.552000|7|
|31|Leif|1991-12-08 04:06:11.248000|2014-10-17 11:57:02.961000|3|
|36|Antonette|1998-08-10 14:56:44.377000|1990-08-14 05:32:47.514000|5|
|38|Cedrick|1999-06-03 09:21:45.416000|2008-05-16 18:27:27.612000|6|
|40|Larry|2000-01-28 20:46:53.408000|2013-02-12 04:08:34.384000|5|
|48|Vivian|1990-01-27 22:50:36.335000|2008-11-09 23:37:36.341000|3|

```python
departments = (
        Project.objects.filter(
            Q(estimated_end_time__date__gte=F("end_time__date"))
            & Q(estimated_end_time__hour__gte=F("end_time__hour"))
            & Q(estimated_end_time__minute__gte=F("end_time__minute"))
        )
        .values("department_id")
        .annotate(Count("department_id"))
    )
```
```python
<QuerySet [{'department_id': 4, 'department_id__count': 1}, {'department_id': 5, 'department_id__count': 2}, {'department_id': 6, 'department_id__count': 1}, {'department_id': 7, 'department_id__count': 1}, {'department_id': 9, 'department_id__count': 1}]>
```
```python
for department in departments:
        print(department)
```
```python
{'department_id': 4, 'department_id__count': 1}
{'department_id': 5, 'department_id__count': 2}
{'department_id': 6, 'department_id__count': 1}
{'department_id': 7, 'department_id__count': 1}
{'department_id': 9, 'department_id__count': 1}
```
****
## EMPLOYEE PROJECT RELATION MODEL
|id|hours|role|employee_id|project_id|
| :---: | :---: | :---: | :---: | :---: | 
|1|1|Information Systems Manager|121|40|
|16|16|Account Executive|132|13|
|19|19|VP Product Management|119|21|
|38|38|Analyst Programmer|116|48|
|47|47|Mechanical Systems Engineer|115|31|
|55|55|Assistant Professor|123|38|
|95|95|Product Engineer|115|36|

```python
Project.objects.filter(employeeprojectrelation__isnull=False)
        .annotate(Count("employees__id", distinct=True))
        .count()
```
```python
7
```
```python
 Project.objects.filter(employeeprojectrelation__isnull=False)
        .values("employees__id")
        .annotate(Count("employees__id", distinct=True))
```
```python
<QuerySet [{'employees__id': 115, 'employees__id__count': 1}, {'employees__id': 116, 'employees__id__count': 1}, {'employees__id': 119, 'employees__id__count': 1}, {'employees__id': 121, 'employees__id__count': 1}, {'employees__id': 123, 'employees__id__count': 1}, {'employees__id': 132, 'employees__id__count': 1}]>
```

****
```sql
SELECT name, age FROM Person;
```
```python
Person.objects.only('name','age')
```
****
```sql
SELECT * FROM Person WHERE age BETWEEN 10 AND 20;
```
```python
Person.objects.filter(age__range=(10, 20))
```
****
```sql
SELECT * FROM Person order by age;

SELECT * FROM Person ORDER BY age DESC;
```
```python
Person.objects.order_by('age')

Person.objects.order_by('-age')
```
****
### -> select_related

```sql
SELECT ... FROM "blog_entry" ...;
```
```python
entry = Entry.objects.first()
```

this attribute access runs a second query
```python
blog = entry.blog
```
```sql
SELECT ... FROM "blog_blog" WHERE ...;
```
#### fewer queries

```sql
SELECT "blog_entry"."id", ... "blog_blog"."id", ...
FROM "blog_entry"
INNER JOIN "blog_blog" ...;
```
```python
entry = Entry.objects.select_related("blog").first()
```
```python
blog = entry.blog
```
no query is run because we JOINed with the blog table above

****
 * [filter](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#filter)
 * [exclude](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#exclude)
 * [annotate](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#annotate)
 * [order_by](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#order-by)
 * [reverse](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#reverse)
 * [distinct](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#distinct)
 * [values](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#values)
 * [values_list](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#values-list)
 * [dates](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#dates)
 * [datetimes](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#datetimes)
 * [none](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#none)
 * [all](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#all)
 * [union](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#union)
 * [intersection](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#intersection)
 * [difference](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#difference)
 * [select_related](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#select-related)
 * [prefetch_related](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#prefetch-related)
 * [extra](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#extra)
 * [defer](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#defer)
 * [only](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#only)
 * [using](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#using)
 * [select_for_update](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#select-for-update)
 * [raw](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#raw)

```diff
- Only Opposite to defer 
```


# Operators that return new QuerySets

 * [AND (&)](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#and)
 * [OR (|)](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#or)

# Methods that do not return QuerySets

## SALERY MODEL
|id |	base	| tax |	insurance |	overtime	|employee_id|
| :---: | :---: | :---: | :---: | :---: | :---: |
|1	|1757.05	|0.3	|3.3	|1	|105|
|2	|1983.48	|0.5	|0	|2	|106|
|3	|1010.26	|1.7	|3.2	|3	|107|
|4	|1926.78	|5.3	|3.9	|4	|108|
|5	|1907.07	|6	|3.1	|5	|109|
****
x=1000

````python
Payslip.objects.filter(payment__isnull=False, payment__amount__gt=x)
        .values("salary__employee_id")
        .distinct()
````
````python
<QuerySet [{'salary__employee_id': 112}, {'salary__employee_id': 119}, {'salary__employee_id': 111}, {'salary__employee_id': 128}]>
````
````python
list(
        Payslip.objects.filter(payment__isnull=False, payment__amount__gt=x)
        .values_list("salary__employee_id", flat=True)
        .distinct()
    )
````
````python
[112, 119, 111, 128]
````
****
## PAYSLIB MODEL
|id	| base	| tax	 | insurance	| overtime |	created |	payment_id |	salary_id|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|9	|1076.37	|85	|103	|495	|2018-07-28	|NULL	|18|
|14	|1807.86	|67	|108	|149	|2018-07-28	|1096	|8|
|15	|1750.22	|53	|187	|425	|2018-07-28	|735	|15|
|19	|1739.45	|46	|159	|366	|2018-07-28	|NULL	|16|
|21	|1696.11	|33	|104	|268	|2018-07-28	|793	|7|
|24	|1716.24	|40	|104	|112	|2018-07-28	|NULL	|13|

````python
saleries = (
        Payslip.objects.filter(payment_id=None,id__lte=24)
        .values("base", "tax", "insurance", "overtime")
        .aggregate(
            total_dept=(Sum("base") + Sum("tax") + Sum("insurance") + Sum("overtime"))
        )
    )
````
````python
{'total_dept': Decimal('6042.06')}
````

 * [get](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#get)
 * [create](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#create)
 * [get_or_create](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#get-or-create)
 * [update_or_create](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#update-or-create)
 * [bulk_create](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#bulk-create)
 * [bulk_update](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#bulk-update)
 * [count](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#count)
 * [in_bulk](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#in-bulk)
 * [iterator](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#iterator)
 * [latest](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#latest)
 * [earliest](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#earliest)
 * [first](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#first)
 * [last](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#last)
 * [aggregate](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#aggregate)
 * [exists](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#exists)
 * [update](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#update)
 * [delete](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#delete)
 * [as_manager](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#as-manager)
 * [explain](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#explain)

## Field lookups

Field lookups are how you specify the meat of an SQL WHERE clause. They’re specified as keyword arguments to the QuerySet methods `filter()`, `exclude()` and `get()`

## EmployeeProjectRelation Model

|id	|hours	|role	|employee_id	|project_id|
| :---: | :---: | :---: | :---: | :---: | 
|1	|1	|Information |Systems Manager	|121	|40|
|16	|16	|Account |Executive	|132	|13|
|19	|19	|VP Product |Management	|119	|21|
|38	|38	|Analyst |Programmer	|116	|48|
|47	|47	|Mechanical |Systems Engineer	|115	|31|
|55	|55	|Assistant |Professor	|123	|38|
|95	|95	|Product |Engineer	|115	|36|

```python
Example: Entry.objects.get(id__exact=14)  # note double underscore.
```

```python
Query = Project.objects.filter(employeeprojectrelation__isnull=False)
```
```python
Query : {<QuerySet [<Project: Torrance>, <Project: Brannon>, <Project: Leif>, 
                    <Project: Antonette>, <Project: Cedrick>, <Project: Larry>
                    , <Project: Vivian>]>}
```

****
```sql
WHERE name like '%A%';
WHERE name like binary '%A%';
WHERE name like 'A%';
WHERE name like binary 'A%';
WHERE name like '%A';
WHERE name like binary '%A';
```
```python
Person.objects.filter(name__icontains='A')
Person.objects.filter(name__contains='A')
Person.objects.filter(name__istartswith='A')
Person.objects.filter(name__startswith='A')
Person.objects.filter(name__iendswith='A')
Person.objects.filter(name__endswith='A')
```

 * [exact](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#exact)
 * [iexact](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#iexact)
 * [contains](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#contains)
 * [icontains](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#icontains)
 * [in](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#in)
 * [gt](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#gt)
 * [gte](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#gte)
 * [lt](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#lt)
 * [lte](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#lte)
 * [startswith](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#startswith)
 * [istartswith](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#istartswith)
 * [endswith](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#endswith)
 * [iendswith](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#iendswith)
 * [range](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#range)
 * [date](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#date)
 * [year](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#year)
 * [iso_year](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#iso-year)
 * [month](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#month)
 * [day](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#day)
 * [week](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#week)
 * [week_day](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#week-day)
 * [quarter](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#quarter)
 * [time](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#time)
 * [hour](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#hour)
 * [minute](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#minute)
 * [second](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#second)
 * [isnull](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#isnull)
 * [regex](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#regex)
 * [iregex](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#iregex)

**Protip: Use [in](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#in) to avoid chaining [filter()](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#filter) and [exclude()](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#exclude)**

```python
Entry.objects.filter(status__in=['Hung over', 'Sober', 'Drunk'])
```

# Aggregation functions 

```sql
SELECT MIN(age) FROM Person;
SELECT MAX(age) FROM Person;
SELECT AVG(age) FROM Person;
SELECT SUM(age) FROM Person;
SELECT COUNT(*) FROM Person;
```
```python
from django.db.models import Min, Max, Avg, Sum

Person.objects.all().aggregate(Min('age'))
{'age__min': 0}

Person.objects.all().aggregate(Max('age'))
{'age__max': 100}

Person.objects.all().aggregate(Avg('age'))
{'age__avg': 50}

Person.objects.all().aggregate(Sum('age'))
{'age__sum': 5050}

Person.objects.count()
```

 * [output_field](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#output-field)
 * [filter](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#aggregate-filter)
 * [\*\*extra](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#id7)
 * [Avg](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#avg)
 * [Count](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#id8)
 * [Max](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#max)
 * [Min](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#min)
 * [StdDev](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#stddev)
 * [Sum](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#sum)
 * [Variance](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#variance)

<!-- # Query-related tools ([link](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#query-related-tools)) -->
# Query-related 
do a NOT query in Django queryset
```python
from django.db.models import Q
queryset = User.objects.filter(~Q(id__lt=5))
queryst
<QuerySet [<User: Ritesh>, <User: Billy>, <User: Radha>, <User: sohan>, <User: Raghu>,
˓<User: rishab>]>
```
 * [Q() objects](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#q-objects)
 * [Prefetch() objects](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#prefetch-objects)
 * [prefetch_related_objects()](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#prefetch-related-objects)
 * [FilteredRelation() objects](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#filteredrelation-objects)

- - -
