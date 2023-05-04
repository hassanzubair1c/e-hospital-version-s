# Generated by Django 4.1.7 on 2023-04-27 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hms', '0002_alter_slots_year_month_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slots',
            name='year_month_field',
        ),
        migrations.AddField(
            model_name='slots',
            name='slot_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]