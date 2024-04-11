import datetime
import time
import requests

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from piramid.forms import LoginForm, UserRegistrationForm, DepositForm
from piramid.models import Products, User, Invoices


def index(request):

    return render(request=request, template_name="piramid/index.html")


def earn_func(request, pk):
    try:
        data_user = get_object_or_404(User, email=request.user.email)
        product = Products.objects.filter(id=pk)

        if data_user.active_product == 0:
            data_user.active_product = pk
            data_user.activation_time = datetime.datetime.now().timestamp()

            data_user.save()

            return redirect(to="earn")

    except Exception as e:
        print(e)
        return redirect(to="login")


def stats(request):
    data_user = get_object_or_404(User, email=request.user.email)

    return render(request=request, template_name='account/statisctic.html',
                  context={
                      'data': {
                          'profit': data_user.profit,
                          'profit_refferals': data_user.refferals_profit,
                          'dep_sum': data_user.deposit_sum
                      }
                  })


def ref_code(request):
    return render(request=request, template_name='account/invite.html')


def earn(request):
    try:
        data_user = get_object_or_404(User, email=request.user.email)
        user_data = {
            'auth_user': True,
            'data_user': data_user,

        }

        if data_user.active_product != 0:
            product = get_object_or_404(Products, id=data_user.active_product)

            if datetime.datetime.now().timestamp() - data_user.activation_time >= 10:
                data_user.balance += data_user.balance * float(product.earn / 100)
                data_user.profit += data_user.balance * (product.earn / 100)
                data_user.active_product = 0
                data_user.activation_time = 0

                data_user.save()

        data_user = get_object_or_404(User, email=request.user.email)

    except AttributeError:
        print(1)
        data_user = None
        user_data = {
            'auth_user': False
        }

    except Exception as e:
        print(e)

    db_data = Products.objects.filter(is_published=1)
    contex_data = []

    for product in db_data:
        if data_user is not None and int(data_user.balance) >= int(product.price):
            contex_data.append({
                'id': product.id,
                'title': product.title,
                'price': product.price,
                'earn': product.earn,
                'image': product.image.name[30:],
                'clicks': product.clicks,
            })

        elif data_user is None:
            contex_data.append({
                'id': product.id,
                'title': product.title,
                'price': product.price,
                'earn': product.earn,
                'image': product.image.name[30:],
                'clicks': product.clicks
            })

    return render(request=request, template_name="piramid/products.html",
                  context={
                      'data': contex_data,
                      'user_data': user_data
                  })


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('account')
                else:
                    form.add_error(None, 'Аккаунт удален.')
                    return render(request, 'account/login.html', {'form': form})

            else:
                form.add_error(None, 'Не правильный логин или пароль.')
                return render(request, 'account/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            print(User.objects.filter(username='alex').exists())
            new_user = user_form.save(commit=False)

            user_model = User(
                name=user_form.cleaned_data['first_name'],
                username=user_form.cleaned_data['username'],
                email=user_form.cleaned_data['email'],
                password=user_form.cleaned_data['password']
            )
            user_model.save()

            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            return render(request, 'verif/success_reg.html')

        if 'password2' not in user_form.cleaned_data:
            user_form.add_error(None, 'Пароли не совпадают!')
            user_form.fields['password'].widget.attrs.update({
                'class': 'form-control is-invalid',
                'placeholder': '********',
            })

            user_form.fields['password2'].widget.attrs.update({
                'class': 'form-control is-invalid',
                'placeholder': '********',
            })

        if 'email' not in user_form.cleaned_data:
            user_form.add_error(None, 'Почта уже занята!')
            user_form.fields['email'].widget.attrs.update({
                'class': 'form-control is-invalid',
                'placeholder': '********',
            })

        if 'username' not in user_form.cleaned_data:
            user_form.add_error(None, 'Имя пользователя уе занято!')
            user_form.fields['username'].widget.attrs.update({
                'class': 'form-control is-invalid',
                'placeholder': '********',
            })

        return render(request, 'account/register.html', {
            'user_form': user_form,
            'errors': str(user_form.errors)
        })

    else:
        user_form = UserRegistrationForm()

    return render(request, 'account/register.html', {'user_form': user_form})


def account(request):
    data_user = get_object_or_404(User, email=request.user.email)

    data = {
        'first_name': data_user.name,
        'balance': str(data_user.balance).replace(",", "."),
        'image': data_user.image,
        'profit': str(data_user.profit).replace(",", "."),
        'reg_date': data_user.reg_date.strftime("%m.%d.%Y")
    }

    print(data)

    return render(request, template_name='piramid/account.html', context={'data': data})


def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            url = "https://api.cryptocloud.plus/v2/invoice/create"
            headers = {
                "Authorization": "Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dWlkIjoiTWpBd056TT0iLCJ0eXBlIjoicHJvamVjdCIsInYiOiI2NzExMDFmMDMzODZmYjM4Zjk4ZDZkMjk1ZTZhNWQwOGM3ODViODhhMmIyNGE3NmRmNjQzMzMwZTRjOTQzZDhhIiwiZXhwIjo4ODExMTg4NjE0M30.JUPPbV3GT9GslOZB1klP5QBhYj0ZMIvtiXsAgpR_O38",
                "Content-Type": "application/json",
            }

            data = {
                "shop_id": "3svtTZV0YhYBllo0",
                "amount": int(form.cleaned_data['amount']),
                "currency": "USD"
            }

            response = requests.post(url, headers=headers, json=data)

            user = get_object_or_404(User, email=request.user.email)
            invoice_model = Invoices(
                user=user,
                invoice_id=response.json()['result']['uuid'],
                invoice_info=response.json()
            )

            invoice_model.save()

            return redirect(to=response.json()['result']['link'])

    else:
        form = DepositForm()

    return render(request, 'account/deposit.html', {'form': form})


@csrf_exempt
@require_http_methods(['POST'])
def cryptocloud_webhook(request):
    status = request.form.get('status')
    invoice_id = request.form.get('invoice_id')
    amount_crypto = request.form.get('amount_crypto')
    currency = request.form.get('currency')
    order_id = request.form.get('order_id')
    token = request.form.get('token')

    print(status)

    return ({'message': 'Postback received'}), 200
