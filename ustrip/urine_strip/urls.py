from django.urls import path,include
from .views import index,UStripViewSet

urlpatterns = [
    path('',index,name="main upload"),
    path('api/',UStripViewSet.as_view(),name="api"),
]