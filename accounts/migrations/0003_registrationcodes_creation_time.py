# Generated by Django 4.1.3 on 2022-11-04 03:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_registrationcodes_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationcodes',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
