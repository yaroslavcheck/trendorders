# Generated by Django 4.2.1 on 2024-04-01 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('piramid', '0014_user_activation_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.CharField(max_length=255)),
                ('invoice_info', models.JSONField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='piramid.user')),
            ],
        ),
        migrations.DeleteModel(
            name='TestModel',
        ),
    ]
