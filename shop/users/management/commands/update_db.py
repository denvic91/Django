from django.core.management.base import BaseCommand
from users.models import User
from users.models import ShopUserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.all():
            ShopUserProfile.objects.create(user=user)