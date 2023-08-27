from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from hotArticle.models import HotArticleModel


class Command(BaseCommand):
    help = "Creates an super user if user does not exist"

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
        )
        parser.add_argument(
            '--email',
        )
        parser.add_argument(
            '--password',
        )
        parser.add_argument(
            '--noinput',
            action='store_true'
        )

    def handle(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(HotArticleModel)

        username = kwargs.get("username", "")
        email = kwargs.get("email", "")
        password = kwargs.get("password", "")

        try:
            User.objects.get(
                username=username,
                email=email,
            )
        except User.DoesNotExist:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            conditions = [
                "add_hotarticlemodel",
                "change_hotarticlemodel",
                "delete_hotarticlemodel",
                "view_hotarticlemodel"
            ]
            permissions = Permission.objects.filter(
                codename__in=conditions,
                content_type=content_type,
            )
            for perm in permissions:
                user.user_permissions.add(perm)

