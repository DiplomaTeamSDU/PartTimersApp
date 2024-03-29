# Generated by Django 4.1.7 on 2023-04-28 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0012_company_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=25, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.position'),
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='occupation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.position'),
        ),
    ]
