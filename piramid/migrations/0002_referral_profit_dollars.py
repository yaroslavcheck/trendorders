# Generated by Django 4.2.1 on 2024-04-16 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piramid', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referral',
            name='profit_dollars',
            field=models.FloatField(default=0),
        ),
    ]
