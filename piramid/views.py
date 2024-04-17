import datetime
import random
import requests

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.template import loader

from piramid.forms import LoginForm, UserRegistrationForm, DepositForm
from piramid.models import Products, User, Invoices, Profits, EarnModel, Referral


def index(request, referral_code=None):
    content = loader.render_to_string(template_name="piramid/index.html")
    response = HttpResponse(content=content)
    response.set_cookie('ref_code', referral_code)

    if not referral_code:
        response.set_cookie('ref_code', None)

    else:
        if User.objects.filter(ref_code=referral_code).exists():
            inviter = get_object_or_404(User, ref_code=referral_code)
            response.set_cookie('inviter', inviter.id)

            if Referral.objects.filter(is_invited=inviter).exists():
                second_referral_referral_model = Referral.objects.get(is_invited=inviter)
                second_referral = get_object_or_404(
                    User,
                    id=second_referral_referral_model.inviter.values_list('id', flat=True)[0]
                )

                response.set_cookie('second_referral', second_referral_referral_model.id)

                if Referral.objects.filter(is_invited=second_referral).exists():
                    first_referral_referral_model = Referral.objects.filter(is_invited=inviter)
                    response.set_cookie('first_referral', first_referral_referral_model.id)

                else:
                    response.set_cookie('first_referral', None)

            else:
                response.set_cookie('second_referral', None)
                response.set_cookie('first_referral', None)

        else:
            response.set_cookie('ref_code', None)
            response.set_cookie('second_referral', None)
            response.set_cookie('first_referral', None)

    return response
    # return render(request=request, template_name="piramid/index.html").set_cookie('test2', 'test3')


def earn_func(request, pk):
    try:
        data_user = get_object_or_404(User, email=request.user.email)
        product = get_object_or_404(Products, id=pk)

        if not EarnModel.objects.filter(user=data_user).exists():
            try:
                earn_model = EarnModel.objects.get(user=data_user)
                earn_model.product = product
                earn_model.save()

            except Exception as _ex:
                print(_ex)
                earn_model = EarnModel(
                    user=data_user,
                    product=product,
                )
                earn_model.save()

            return redirect(to="earn")

    except Exception as e:
        print(e)
        return redirect(to="login")


def stats(request):
    data_user = get_object_or_404(User, email=request.user.email)

    profits_model = Profits.objects.filter(user=data_user)
    profits_sum = 0

    for profit in profits_model:
        profits_sum += profit.sum

    referrals_profit = Referral.objects.filter(inviter=data_user).all()
    profit_ref = 0

    for profit in referrals_profit.values('profit_dollars'):
        profit_ref += profit['profit_dollars']

    return render(request=request, template_name='account/statisctic.html',
                  context={
                      'data': {
                          'profit': profits_sum,
                          'profit_refferals': profit_ref,
                          'dep_sum': 0,
                          'all_refs': len(referrals_profit)
                      }
                  })


def details_profit(request):
    user = get_object_or_404(User, email=request.user.email)

    profits_model = Profits.objects.filter(user=user)
    profits_data = []
    for profit in profits_model:
        profits_data.append([round(profit.sum, 2), profit.date])

    return render(request=request,
                  template_name='account/details-profit.html',
                  context={'profits_data': profits_data[::-1]})


def ref_code(request):
    user_data = get_object_or_404(User, email=request.user.email)
    if user_data.ref_code == "":
        new_ref_code = 1000
        while User.objects.filter(ref_code=new_ref_code).exists():
            new_ref_code = random.randint(1000, 9999)

        referral_code = new_ref_code

        user_data.ref_code = new_ref_code
        user_data.save()

    else:
        referral_code = user_data.ref_code

    if Referral.objects.filter(inviter=user_data).exists():
        referrals_profit = Referral.objects.filter(inviter=user_data).all()
        profit_ref = 0

        for profit in referrals_profit.values('profit_dollars'):
            profit_ref += profit['profit_dollars']

    else:
        referrals_profit = 0
        profit_ref = 0

    print(referral_code)
    return render(request=request, template_name='account/invite.html',
                  context={'ref_code': referral_code,
                           'profit': profit_ref,
                           'all_refs': len(referrals_profit)})


def earn(request):
    print(request.COOKIES)
    try:
        data_user = get_object_or_404(User, email=request.user.email)
        profits = Profits.objects.filter(user=data_user)

        profit_sum = 0
        for profit in profits:
            profit_sum += profit.sum

        user_data = {
            'auth_user': True,
            'data_user': data_user,
            'profit': profit_sum
        }

        if EarnModel.objects.filter(user=data_user).exists():
            active_product_model = get_object_or_404(EarnModel, user=data_user)
            user_data['active_product'] = active_product_model.product.id

        else:
            user_data['active_product'] = 0

        if user_data['active_product'] != 0:
            product = get_object_or_404(Products, id=user_data['active_product'])

            if datetime.datetime.now().timestamp() - active_product_model.activation_time.timestamp() >= 1:
                data_user.balance += data_user.balance * float(product.earn / 100)

                profit = Profits(
                    user=data_user,
                    product=product,
                    sum=data_user.balance * float(product.earn / 100)
                )
                profit.save()

                ref_object = Referral.objects.get(is_invited=data_user)

                ref_model = get_object_or_404(Referral, is_invited=data_user)
                ref_model.profit_dollars += (data_user.balance * float(product.earn / 100)) * 0.02
                ref_model.save()

                ref_user = get_object_or_404(User, id=ref_object.inviter.values_list('id', flat=True)[0])
                ref_user.balance += (data_user.balance * float(product.earn / 100)) * 0.02
                ref_user.save()

                user_data['active_product'] = 0

                data_user.save()
                active_product_model.delete()

        data_user = get_object_or_404(User, email=request.user.email)

    except AttributeError as _ex:
        print(_ex)
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
            })

        elif data_user is None:
            contex_data.append({
                'id': product.id,
                'title': product.title,
                'price': product.price,
                'earn': product.earn,
                'image': product.image.name[30:],
            })

        print(contex_data)

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
    cookies = request.COOKIES
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
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

            if cookies['ref_code'] != 'None':
                inviter = User.objects.filter(id=int(cookies['inviter']))
                if cookies['second_referral'] != 'None':
                    second_referral = User.objects.filter(id=int(cookies['second_referral']))
                else:
                    second_referral = User.objects.filter(ref_code=1000)

                if cookies['first_referral'] != 'None':
                    first_referral = User.objects.filter(id=int(cookies['first_referral']))
                else:
                    first_referral = User.objects.filter(ref_code=1000)

                referral_model = Referral.objects.create(
                    is_invited=user_model,
                    profit=0.2 if second_referral != User.objects.filter(ref_code=1000) else 0.1
                )

                referral_model.inviter.set(inviter)
                referral_model.second_ref.set(second_referral)
                referral_model.first_ref.set(first_referral)

                referral_model.save()

            return render(request=request, template_name='verif/success_reg.html')

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
    try:
        profits_model = Profits.objects.filter(user=data_user)
        profits_user = 0
        for profit in profits_model:
            profits_user += profit.sum
    except Exception as _ex:
        print(_ex)
        profits_user = 0.0

    data = {
        'first_name': data_user.name,
        'balance': str(data_user.balance).replace(",", "."),
        'image': data_user.image,
        'profit': profits_user,
        'reg_date': data_user.reg_date.strftime("%m.%d.%Y"),
    }

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
