from django.db import migrations
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.utils import timezone


def create_groups_and_users(apps, schema_editor):
    User = get_user_model()

    clients_group, created = Group.objects.get_or_create(name="Clients")
    client_user, user_created = User.objects.get_or_create(
        username="client",
        email="client@example.com",
        last_login=timezone.now(),
    )
    if user_created:
        client_user.set_password("client")
        client_user.save()
    client_user.groups.add(clients_group)

    sellers_group, created = Group.objects.get_or_create(name="Sellers")
    seller_user, user_created = User.objects.get_or_create(
        username="seller",
        email="seller@example.com",
        last_login=timezone.now(),
    )
    if user_created:
        seller_user.set_password("seller")
        seller_user.save()
    seller_user.groups.add(sellers_group)

    admin_user, user_created = User.objects.get_or_create(
        username="admin",
        email="admin@example.com",
        is_staff=True,
        is_superuser=True,
        last_login=timezone.now(),
    )
    if user_created:
        admin_user.set_password("admin")
        admin_user.save()


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_groups_and_users),
    ]
