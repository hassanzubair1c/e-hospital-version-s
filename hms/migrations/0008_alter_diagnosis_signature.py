# Generated by Django 4.1.7 on 2023-05-15 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hms', '0007_diagnosis_signature_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosis',
            name='signature',
            field=models.ImageField(upload_to='media/signatures/'),
        ),
    ]
