# Generated by Django 5.0.7 on 2024-07-14 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_heartbeat',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]