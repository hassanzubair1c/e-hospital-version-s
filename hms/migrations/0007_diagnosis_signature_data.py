# Generated by Django 4.1.7 on 2023-05-15 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hms', '0006_diagnosis'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnosis',
            name='signature_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]
