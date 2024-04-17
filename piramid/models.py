from django.db import models
from django.contrib import admin


class Products(models.Model):
    title = models.CharField(
        max_length=255
    )
    image = models.ImageField(
        upload_to='piramid/static/piramid/images'
    )
    price = models.IntegerField()
    earn = models.FloatField()
    is_published = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.title


class User(models.Model):
    name = models.CharField(
        max_length=255
    )
    username = models.CharField(
        max_length=255
    )
    email = models.EmailField()
    is_verif = models.BooleanField(
        default=False
    )
    password = models.CharField(
        max_length=255
    )
    image = models.ImageField(
        upload_to='piramid/static/piramid/images',
        default=None
    )
    balance = models.FloatField(
        default=0
    )
    reg_date = models.DateField(
        auto_now_add=True
    )
    ref_code = models.CharField(
        max_length=10
    )

    def __str__(self):
        return self.email


class Invoices(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=1
    )
    invoice_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='0')
    invoice_info = models.JSONField()

    def __str__(self):
        return self.invoice_id


class Deposits(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=1
    )
    sum = models.FloatField()
    invoice_id = models.CharField(
        max_length=20
    )
    date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return self.invoice_id


class Withdrawals(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=1
    )
    sum = models.FloatField()
    date = models.DateField(
        auto_now_add=True
    )
    status = models.CharField(
        max_length=10
    )
    transfer_to = models.CharField(
        max_length=50
    )
    number_of_withdrawal = models.IntegerField()

    def __str__(self):
        return self.user


class Profits(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=1
    )
    sum = models.FloatField()
    product = models.ForeignKey(
        Products,
        on_delete=models.SET_DEFAULT,
        default=1
    )
    date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return str(self.sum)


class Referral(models.Model):
    inviter = models.ManyToManyField(
        to=User,
        related_name="inviter"
    )
    is_invited = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=1
    )
    date = models.DateField(
        auto_now_add=True
    )
    first_ref = models.ManyToManyField(
        to=User,
        related_name="first_ref",
    )
    second_ref = models.ManyToManyField(
        to=User,
        related_name="second_ref"
    )
    profit = models.FloatField()
    profit_dollars = models.FloatField(default=0)

    def __str__(self):
        return str(self.date)


class EarnModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE
    )
    activation_time = models.DateTimeField(
        auto_now_add=True,
    )

