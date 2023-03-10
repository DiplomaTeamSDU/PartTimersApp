from django.db import migrations,models

def create_categories(apps, schema_editor):
    Category = apps.get_model('jobs', 'Category')
    categories = ['Backend', 'Frontend', 'UI', 'Website']
    for category in categories:
        Category.objects.create(name=category)

class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RunPython(create_categories),
    ]
