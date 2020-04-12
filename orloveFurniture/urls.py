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






    url(r'^api/get/order/(?P<order_id>\d+)/$', views.request_order),

    url(r'^api/get/orders/work/(?P<worker_id>\d+)/$', views.request_orders_in_work),
    url(r'^api/get/orders/ready/(?P<worker_id>\d+)/$', views.request_orders_ready),


    url(r'^api/get/materials/(?P<order_id>\d+)/$', views.request_materials),


    url(r'^api/get/operations/(?P<order_id>\d+)/(?P<worker_id>\d+)/$', views.request_operations),

    url(r'^api/get/user/(?P<user_string>\d+)/(?P<hash_string>\d+)/$', views.request_auth),


    url(r'^api/get/dict/operations/$', views.request_dict_operations),
    url(r'^api/get/dict/materials/$', views.request_dict_materials),

]
