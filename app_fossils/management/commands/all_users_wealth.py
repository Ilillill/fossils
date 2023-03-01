from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Sum
import json

from app_fossils.models import DBFossil

class Command(BaseCommand):
    def handle(self, *args, **options):
        all_users_wealth = []
        users = User.objects.all()
        for usr in users:
            total_value = DBFossil.objects.filter(fossil_owner=usr).aggregate(Sum('fossil_value'))['fossil_value__sum']
            total_value = float(total_value) if total_value is not None else 0
            all_users_wealth.append({'user': usr.username, 'wealth': total_value})

        with open('all_users_wealth.json', 'w') as f:
            json.dump(all_users_wealth, f)