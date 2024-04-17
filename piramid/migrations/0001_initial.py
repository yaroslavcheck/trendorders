# Generated by Django 4.2.1 on 2024-04-13 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='piramid/static/piramid/images')),
                ('price', models.IntegerField()),
                ('earn', models.FloatField()),
                ('is_published', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('is_verif', models.BooleanField(default=False)),
                ('password', models.CharField(max_length=255)),
                ('image', models.ImageField(default=None, upload_to='piramid/static/piramid/images')),
                ('balance', models.FloatField(default=0)),
                ('reg_date', models.DateField(auto_now_add=True)),
                ('ref_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Withdrawals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(max_length=10)),
                ('transfer_to', models.CharField(max_length=50)),
                ('number_of_withdrawal', models.IntegerField()),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='piramid.user')),
            ],
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('profit', models.FloatField()),
                ('first_ref', models.ManyToManyField(related_name='first_ref', to='piramid.user')),
                ('inviter', models.ManyToManyField(related_name='inviter', to='piramid.user')),
                ('is_invited', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='piramid.user')),
                ('second_ref', models.ManyToManyField(related_name='second_ref', to='piramid.user')),
            ],
        ),
        migrations.CreateModel(
            name='Profits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='piramid.products')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='piramid.user')),
            ],
        ),
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.CharField(max_length=255)),
                ('invoice_info', models.JSONField()),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='piramid.user')),
            ],
        ),
        migrations.CreateModel(
            name='EarnModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_time', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='piramid.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='piramid.user')),
            ],
        ),
        migrations.CreateModel(
            name='Deposits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.FloatField()),
                ('invoice_id', models.CharField(max_length=20)),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='piramid.user')),
            ],
        ),
    ]
