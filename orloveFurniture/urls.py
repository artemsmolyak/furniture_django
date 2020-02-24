from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from .AllOrdersShow import  AllOrdersShow
from .OrderDelete import OrderDelete

from .models import Order

from django.contrib.auth.decorators import login_required, permission_required

from .OrderView import OrderView
from .OrderCreateView import OrderCreateView



urlpatterns = [
    url(r'^login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    url(r'^logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),


    url(r'^$', AllOrdersShow.as_view(), name='index'),
    url(r'^index/$', AllOrdersShow.as_view(), name='index'),


    url(r'^order_create/$', OrderCreateView.as_view(), name='order_create'),

    url(r'^order/(?P<order_id>\d+)/$', OrderView.as_view(), name='order'),


    url(r'^delete/(?P<pk>\d+)/$', OrderDelete.as_view(), name='delete'),


    url(r'^store/$', views.store, name='store'),

    url(r'^requestMaterials/$', views.createRequestMaterials, name='createRequestMaterials'),

    url(r'^reportCompletedApplication/$', views.createReportCompletedApplication, name='reportCompletedApplication'),
    url(r'^reportOutstandingApplication/$', views.createReportOutstandingApplication, name='reportOutstandingApplication'),


    url(r'^xls/$', views.xls, name='xls'),

]
