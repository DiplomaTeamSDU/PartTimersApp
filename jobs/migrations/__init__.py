from django.db import migrations

def set_user_default(apps, schema_editor):
    Company = apps.get_model('jobs', 'Company')
    User = apps.get_model('auth', 'User')
    for company in Company.objects.all():
        user = User.objects.create(username=company.name)
        company.user = user
        company.save()

class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_add_user_to_company'),
    ]

    operations = [
        migrations.RunPython(set_user_default),
    ]