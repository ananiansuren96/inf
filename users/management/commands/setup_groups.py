from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Article, Category, Tag

class Command(BaseCommand):
    help = 'Setup user groups and permissions'

    def handle(self, *args, **kwargs):
        # Create Groups
        editor_group, created = Group.objects.get_or_create(name='Editor')
        journalist_group, created = Group.objects.get_or_create(name='Journalist')

        # Content Types
        article_ct = ContentType.objects.get_for_model(Article)
        category_ct = ContentType.objects.get_for_model(Category)
        tag_ct = ContentType.objects.get_for_model(Tag)

        # Journalist Permissions (Add/Change Article)
        journalist_perms = Permission.objects.filter(
            content_type=article_ct, 
            codename__in=['add_article', 'change_article', 'view_article']
        )
        journalist_group.permissions.set(journalist_perms)

        # Editor Permissions (All Article, Category, Tag)
        editor_perms = Permission.objects.filter(
            content_type__in=[article_ct, category_ct, tag_ct]
        )
        editor_group.permissions.set(editor_perms)

        self.stdout.write(self.style.SUCCESS('Successfully setup groups and permissions'))
