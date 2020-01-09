from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.orders, name='index'),

    url(r'^order_create/$', views.order_create, name='order_create'),
    url(r'^order/(?P<good_id>\d+)/$', views.order, name='order'),

]
