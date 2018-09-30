from django.contrib import admin
from django.urls import path
from posts.views import *


urlpatterns = [
    
    path('create/', post_create),
    path('<int:pk>/', post_detail, name='detail'),
    
    #path('detail/(?p<id>\d+)/', post_detail),
    path('<int:pk>/edit/', post_update),
    path('', post_list, name='list'),
    path('<int:pk>/delete/', post_delete),


]
