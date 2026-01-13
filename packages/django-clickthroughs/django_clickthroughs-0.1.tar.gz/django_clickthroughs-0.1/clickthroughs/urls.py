from django.urls import path

from . import views


app_name = 'clickthroughs'

urlpatterns = [

    path('', views.ClickthroughView.as_view(), name='go'),

]
