# Generated by Django 4.2.9 on 2024-01-15 23:41

from django.db import migrations

from django.core.paginator import Paginator

def migrate_new_assigned_fields(apps, schema_editor):
    Result = apps.get_model('django_datawatch', 'Result')
    ThroughResultAssignedGroups = Result.assigned_groups.through
    ThroughResultAssignedUsers = Result.assigned_users.through

    for result in Result.objects.all():
        result.assigned_groups = result.assigned_groups.all()
        result.assigned_users = result.assigned_users.all()
        result.save(update_fields=['assigned_groups', 'assigned_users'])

    # Paginate the queryset to avoid memory issues
    paginator = Paginator(
        Result.objects.only("assigned_to_user", "assigned_to_group"),
        5000,
    )

    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        group_instances = []
        user_instances = []

        for result in page.object_list:
            if result.assigned_to_group:
                group_instances.append(ThroughResultAssignedGroups(
                    result_id=result.pk,
                    group_id=result.assigned_to_group.pk,
                ))
            if result.assigned_to_user:
                user_instances.append(ThroughResultAssignedUsers(
                    result_id=result.pk,
                    user_id=result.assigned_to_user.pk,
                ))

        ThroughResultAssignedGroups.objects.bulk_create(group_instances)
        ThroughResultAssignedUsers.objects.bulk_create(user_instances)


class Migration(migrations.Migration):

    dependencies = [
        ('django_datawatch', '0004_result_assigned_groups_result_assigned_users'),
    ]

    operations = [
        migrations.RunPython(migrate_new_assigned_fields)
    ]
