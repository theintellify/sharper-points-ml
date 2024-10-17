from django.urls import path

from . import views

urlpatterns = [
    path('pretrained_models', views.index, name='index'),
    # path('<str:uuid>',)

]