from django.template.defaulttags import url
from django.urls import path, include
from piramid import views
from django.contrib.auth import views as authViews


urlpatterns = [
    path('', views.index, name='main'),
    path('earn/', views.earn, name='earn'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('account/', views.account, name='account'),
    path('exit/', authViews.LogoutView.as_view(next_page='main'), name='exit'),
    path('earn/<int:pk>', views.earn_func, name='earn_func'),
    path('stats/', views.stats, name='stats'),
    path('ref_code/', views.ref_code, name='ref_code'),
    path('deposit/', views.deposit, name='deposit'),
    path('callback/', views.cryptocloud_webhook, name='callback')
    # path('success_reg/', views.success_reg, name='success')
]
