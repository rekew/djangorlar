from account.models import CustomUser
from django.core.management.base import BaseCommand
from django.db.models import (
    Count, 
    Avg, 
    Max, 
    Min, 
    F, 
    Q, 
    Case, 
    When, 
    Value, 
    IntegerField, 
    ExpressionWrapper, 
    Sum,
    DurationField,
)
from django.db.models.functions import Concat, ExtractYear, Now
from django.utils import timezone

class Command(BaseCommand):
    help = 'Run example ORM queries on CustomUser'
    objects: CustomUser = CustomUser.objects

    def add_arguments(self, parser):
        parser.add_argument(
            '--query',
            type=str,
            help='Specify which query function to run',
        )

    def handle(self, *args, **options):
        query_name = options.get('query')
        if query_name:
            if hasattr(self, query_name):
                getattr(self, query_name)()
            else:
                self.stdout.write(self.style.ERROR(f"No query function named '{query_name}'"))
        else:
            self.stdout.write("No query specified, running all queries...")
            self.run_all_queries()

    def run_all_queries(self):
        self.stdout.write(self.style.SUCCESS("Running all 50 queries...\n"))

        query_methods = [
            "get_active_users",
            "get_users_with_gmail",
            "get_users_from_almaty_city",
            "get_users_not_from_almaty",
            "get_users_salary_gt_500000",
            "get_users_it_kazakhstan",
            "get_users_birthdate_null",
            "get_users_firstname_startswith_a",
            "get_total_users",
            "get_first_20_by_date_joined_desc",
            "get_distinct_cities",
            "count_users_in_sales",
            "get_users_last_7_days_login",
            "get_users_name_or_surname_contains_bek",
            "get_users_salary_between_300k_700k",
            "get_users_in_departments_it_hr_finance",
            "group_users_by_department",
            "group_users_by_department_order_desc",
            "top_5_cities_by_users",
            "get_users_never_logged_in",
            "get_avg_salary",
            "get_max_min_salary",
            "get_users_with_phone_plus7",
            "annotate_full_name",
            "annotate_birth_year_order",
            "get_users_born_in_may",
            "get_managers_salary_gt_400k",
            "get_employees_or_hr",
            "count_active_users_per_city",
            "get_10_earliest_users",
            "users_city_starts_a_salary_gt_300k",
            "get_users_with_empty_department",
            "stats_by_country",
            "get_staff_users_order_last_login",
            "users_email_not_example_com",
            "users_salary_higher_than_avg",
            "find_duplicate_emails",
            "annotate_salary_level",
            "get_users_current_year_joined",
            "total_payroll_per_department",
            "users_it_never_logged_in",
            "users_kazakhstan_city_null_or_empty",
            "users_birth_before_1990_salary_not_null",
            "annotate_years_since_joined",
            "users_sales_gmail_salary_gt_350k",
            "get_users_order_country_salary_desc",
            "count_users_per_role_gt_100",
            "users_last_login_before_date_joined",
            "annotate_is_senior",
            "departments_avg_salary_min_20_users",
        ]

        for method_name in query_methods:
            if hasattr(self, method_name):
                self.stdout.write(self.style.SUCCESS(f"\nRunning {method_name}:\n"))
                getattr(self, method_name)()
            else:
                self.stdout.write(self.style.ERROR(f"Method {method_name} not found"))


    def get_active_users(self):
        active_users = self.objects.filter(is_active=True)
        self.stdout.write("Active users:")
        self.print_users(active_users)

    def get_users_with_gmail(self):
        users = self.objects.filter(email__endswith = '@gmail.com')

        self.print_users(users)

    def get_users_from_almaty_city(self):
        users = self.objects.filter(city = 'Almaty')

        self.print_users(users)
    
    def get_users_not_from_almaty(self):
        users = self.objects.exclude(city = 'Almaty')
        
        self.print_users(users)

    def get_active_users(self):
        users = self.objects.filter(is_active=True)
        self.print_users(users)

    def get_users_with_gmail(self):
        users = self.objects.filter(email__endswith='@gmail.com')
        self.print_users(users)

    def get_users_from_almaty_city(self):
        users = self.objects.filter(city='Almaty')
        self.print_users(users)

    def get_users_not_from_almaty(self):
        users = self.objects.exclude(city='Almaty')
        self.print_users(users)

    def get_users_salary_gt_500000(self):
        users = self.objects.filter(salary__gt=500000)
        self.print_users(users)

    def get_users_it_kazakhstan(self):
        users = self.objects.filter(department='IT', country='Kazakhstan')
        self.print_users(users)

    def get_users_birthdate_null(self):
        users = self.objects.filter(birth_date__isnull=True)
        self.print_users(users)

    def get_users_firstname_startswith_a(self):
        users = self.objects.filter(first_name__istartswith='A')
        self.print_users(users)

    def get_total_users(self):
        total = self.objects.count()
        self.stdout.write(f"Total users: {total}")

    def get_first_20_by_date_joined_desc(self):
        users = self.objects.order_by('-date_joined')[:20]
        self.print_users(users)

    def get_distinct_cities(self):
        cities = self.objects.values_list('city', flat=True).distinct()
        self.stdout.write("Distinct cities:")
        for city in cities:
            self.stdout.write(f" - {city}")

    def count_users_in_sales(self):
        count = self.objects.filter(department='Sales').count()
        self.stdout.write(f"Users in Sales: {count}")

    def get_users_last_7_days_login(self):
        week_ago = timezone.now() - timezone.timedelta(days=7)
        users = self.objects.filter(last_login__gte=week_ago)
        self.print_users(users)

    def get_users_name_or_surname_contains_bek(self):
        users = self.objects.filter(Q(first_name__icontains='bek') | Q(last_name__icontains='bek'))
        self.print_users(users)

    def get_users_salary_between_300k_700k(self):
        users = self.objects.filter(salary__gte=300000, salary__lte=700000)
        self.print_users(users)

    def get_users_in_departments_it_hr_finance(self):
        users = self.objects.filter(department__in=['IT', 'HR', 'Finance'])
        self.print_users(users)

    def group_users_by_department(self):
        groups = self.objects.values('department').annotate(count=Count('id'))
        for g in groups:
            self.stdout.write(f"{g['department']}: {g['count']}")

    def group_users_by_department_order_desc(self):
        groups = self.objects.values('department').annotate(count=Count('id')).order_by('-count')
        for g in groups:
            self.stdout.write(f"{g['department']}: {g['count']}")

    def top_5_cities_by_users(self):
        cities = self.objects.values('city').annotate(count=Count('id')).order_by('-count')[:5]
        for c in cities:
            self.stdout.write(f"{c['city']}: {c['count']}")

    def get_users_never_logged_in(self):
        users = self.objects.filter(last_login__isnull=True)
        self.print_users(users)

    def get_avg_salary(self):
        avg = self.objects.aggregate(avg_salary=Avg('salary'))['avg_salary']
        self.stdout.write(f"Average salary: {avg}")

    def get_max_min_salary(self):
        stats = self.objects.aggregate(max_salary=Max('salary'), min_salary=Min('salary'))
        self.stdout.write(f"Max salary: {stats['max_salary']}, Min salary: {stats['min_salary']}")

    def get_users_with_phone_plus7(self):
        users = self.objects.filter(phone__contains='+7')
        self.print_users(users)

    def annotate_full_name(self):
        users = self.objects.annotate(full_name=Concat(F('first_name'), Value(' '), F('last_name')))
        self.print_users(users)

    def annotate_birth_year_order(self):
        users = self.objects.annotate(birth_year=ExtractYear('birth_date')).order_by('birth_year')
        self.print_users(users)

    def get_users_born_in_may(self):
        users = self.objects.filter(birth_date__month=5)
        self.print_users(users)

    def get_managers_salary_gt_400k(self):
        users = self.objects.filter(role='manager', salary__gt=400000)
        self.print_users(users)

    def get_employees_or_hr(self):
        users = self.objects.filter(Q(role='employee') | Q(department='HR'))
        self.print_users(users)

    def count_active_users_per_city(self):
        groups = self.objects.filter(is_active=True).values('city').annotate(count=Count('id'))
        for g in groups:
            self.stdout.write(f"{g['city']}: {g['count']}")

    def get_10_earliest_users(self):
        users = self.objects.order_by('date_joined')[:10]
        self.print_users(users)

    def users_city_starts_a_salary_gt_300k(self):
        users = self.objects.filter(city__startswith='A', salary__gt=300000)
        self.print_users(users)

    def get_users_with_empty_department(self):
        users = self.objects.filter(Q(department__isnull=True) | Q(department=''))
        self.print_users(users)

    def stats_by_country(self):
        stats = self.objects.values('country').annotate(count=Count('id'), avg_salary=Avg('salary'))
        for s in stats:
            self.stdout.write(f"{s['country']}: count={s['count']}, avg_salary={s['avg_salary']}")

    def get_staff_users_order_last_login(self):
        users = self.objects.filter(is_staff=True).order_by('-last_login')
        self.print_users(users)

    def users_email_not_example_com(self):
        users = self.objects.exclude(email__icontains='example.com')
        self.print_users(users)

    def users_salary_higher_than_avg(self):
        avg = self.objects.aggregate(avg_salary=Avg('salary'))['avg_salary']
        if avg is None:
            self.stdout.write("No salary data to compare.")
            return

        users = self.objects.filter(salary__gt=avg)
        self.print_users(users)


    def find_duplicate_emails(self):
        emails = self.objects.values('email').annotate(count=Count('id')).filter(count__gt=1)
        for e in emails:
            self.stdout.write(f"Duplicate email: {e['email']} (count={e['count']})")

    def annotate_salary_level(self):
        users = self.objects.annotate(
            salary_level=Case(
                When(salary__lt=300000, then=Value('low')),
                When(salary__gte=300000, salary__lte=700000, then=Value('medium')),
                When(salary__gt=700000, then=Value('high')),
                output_field=IntegerField()
            )
        ).order_by('salary_level')
        self.print_users(users)

    def get_users_current_year_joined(self):
        year = timezone.now().year
        users = self.objects.filter(date_joined__year=year)
        self.print_users(users)

    def total_payroll_per_department(self):
        stats = self.objects.values('department').annotate(total_salary=Sum('salary'))
        for s in stats:
            self.stdout.write(f"{s['department']}: {s['total_salary']}")

    def users_it_never_logged_in(self):
        users = self.objects.filter(department='IT', last_login__isnull=True)
        self.print_users(users)

    def users_kazakhstan_city_null_or_empty(self):
        users = self.objects.filter(country='Kazakhstan').filter(Q(city__isnull=True) | Q(city=''))
        self.print_users(users)

    def users_birth_before_1990_salary_not_null(self):
        users = self.objects.filter(birth_date__lt='1990-01-01').exclude(salary__isnull=True)
        self.print_users(users)

    def annotate_years_since_joined(self):
        users = self.objects.annotate(
            days_since_joined=ExpressionWrapper(
                Now() - F('date_joined'),
                output_field=DurationField()
            )
        )

        self.stdout.write("Users with years_since_joined:")
        for user in users:
            if user.date_joined:
                years = (timezone.now() - user.date_joined).days / 365.25
                self.stdout.write(f"{user} - {years:.2f} years")
            else:
                self.stdout.write(f"{user} - no date_joined")

    def users_sales_gmail_salary_gt_350k(self):
        users = self.objects.filter(
            department='Sales', email__endswith='@gmail.com', salary__gt=350000
        )
        self.print_users(users)

    def get_users_order_country_salary_desc(self):
        users = self.objects.order_by('country', '-salary')
        self.print_users(users)

    def count_users_per_role_gt_100(self):
        groups = self.objects.values('role').annotate(count=Count('id')).filter(count__gt=100)
        for g in groups:
            self.stdout.write(f"{g['role']}: {g['count']}")

    def users_last_login_before_date_joined(self):
        users = self.objects.filter(last_login__lt=F('date_joined'))
        self.print_users(users)

    def annotate_is_senior(self):
        users = self.objects.annotate(
            is_senior=Case(
                When(birth_date__lt='1985-01-01', then=Value(True)),
                default=Value(False),
                output_field=IntegerField()
            )
        )
        self.print_users(users)

    def departments_avg_salary_min_20_users(self):
        departments = self.objects.values('department').annotate(
            avg_salary=Avg('salary'), count=Count('id')
        ).filter(count__gte=20).order_by('-avg_salary')
        for d in departments:
            self.stdout.write(f"{d['department']}: avg_salary={d['avg_salary']}, count={d['count']}")

    def print_users(self, users):
        for user in users:
            print(user)