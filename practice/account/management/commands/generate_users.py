from django.core.management.base import BaseCommand
from account.models import CustomUser
from faker import Faker
import random
from datetime import datetime
from django.utils import timezone

class Command(BaseCommand):
    help = 'Generate 10,000 fake users'

    def handle(self, *args, **kwargs):
        fake = Faker()

        departments = ['IT', 'HR', 'Sales', 'Finance']
        roles = ['admin', 'manager', 'employee']
        batch_size = 1000
        total_users = 10000

        users_to_create = []

        temp_user = CustomUser()
        temp_user.set_password('12345')
        hashed_password = temp_user.password

        for i in range(total_users):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            phone = fake.phone_number()
            city = fake.city()
            country = fake.country()
            department = random.choice(departments)
            role = random.choice(roles)
            
            start_date = datetime(1975, 1, 1)
            end_date = datetime(2005, 12, 31)
            birth_date = fake.date_between(start_date=start_date, end_date=end_date)

            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email, 
                phone=phone,
                city=city,
                country=country,
                department=department,
                role=role,
                birth_date=birth_date,
                password=hashed_password,
                is_active=True,
                is_staff=(role=='admin'),
                date_joined=timezone.now()
            )

            users_to_create.append(user)

            if len(users_to_create) >= batch_size:
                CustomUser.objects.bulk_create(users_to_create)
                self.stdout.write(f'Created {i+1} users...')
                users_to_create = []

        if users_to_create:
            CustomUser.objects.bulk_create(users_to_create)
            self.stdout.write(f'Created all {total_users} users!')

        self.stdout.write(self.style.SUCCESS('Successfully generated 10,000 users'))
