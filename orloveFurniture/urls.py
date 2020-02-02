from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    url(r'^login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    url(r'^logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    url(r'^$', views.orders, name='index'),
    url(r'^index/$', views.orders, name='index'),

    url(r'^order_create/$', views.order_create, name='order_create'),
    url(r'^order/(?P<good_id>\d+)/$', views.order, name='order'),

    url(r'^store/$', views.store, name='store'),

    url(r'^requestMaterials/$', views.createRequestMaterials, name='createRequestMaterials'),

    url(r'^reportCompletedApplication/$', views.createReportCompletedApplication, name='reportCompletedApplication'),

]
