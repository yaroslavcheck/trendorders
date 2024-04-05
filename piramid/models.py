from django.db import models


class Products(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='piramid/static/piramid/images')
    price = models.IntegerField()
    earn = models.FloatField()
    clicks = models.IntegerField()
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    verif_email = models.BooleanField(default=False)
    password = models.CharField(max_length=255)
    image = models.ImageField(upload_to='piramid/static/piramid/images', default=None)

    active_product = models.IntegerField(default=None)
    activation_time = models.FloatField(default=0)

    balance = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    reg_date = models.DateField(auto_now_add=True)
    clicks = models.IntegerField(default=0)
    ref_code = models.IntegerField(default=0)
    inviter = models.IntegerField(default=0)
    auth_token = models.CharField(default=0, max_length=100)
    deposit_sum = models.FloatField(default=0)
    refferals_profit = models.FloatField(default=0)

    def __str__(self):
        return self.email


class Invoices(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    invoice_id = models.CharField(max_length=255)
    invoice_info = models.JSONField()

    def __str__(self):
        return self.invoice_id


class TempInvoices(models.Model):
    amount = models.IntegerField()
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
