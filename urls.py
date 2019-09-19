from django.conf.urls import url,include
from . import views
app_name ='laundry'
urlpatterns =[
    
url(r'^$',views.index,name='index'),
url(r'^validation/$',views.validation,name='index1'),
url(r'^welcome/$',views.welcome,name='index2'),
url(r'^handler/$',views.handler,name='index3'),
url(r'^session1/$',views.session1,name='index4'),
url(r'^history/$',views.history,name='history'),
url(r'^admin/$',views.admin,name='admin'),
url(r'^advalidation/$',views.advalidation,name='advali'),
url(r'^detaildisplay/$',views.detaildisplay,name='detaildisplay'),
url(r'^rpi1/$',views.rpi1,name='rpi1'),
url(r'^add/$',views.add,name ='add'),
url(r'^remove/$',views.remove,name ='remove'),
url(r'^generate/$',views.generate,name ='generate'),
url(r'^count_change/$',views.count_change,name ='count_change'),
url(r'^pass_change/$',views.pass_change,name ='pass_change'),
url(r'^data_entry/$',views.data_entry,name ='data_entry'),
url(r'^forgot/$',views.forgot,name ='forgot'),
url(r'^resetting/$',views.resetting,name ='resetting'),
url(r'^generate_for_staff/$',views.generate_for_staff,name ='generate_for_staff'),
url(r'^generate_for_inactive_students/$',views.generate_for_inactive_students,name ='generate_for_inactive_students'),
url(r'one_time_only/$',views.one_time_only,name = 'one_time_only'),

]   
