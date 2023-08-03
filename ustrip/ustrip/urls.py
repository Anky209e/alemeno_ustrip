from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect

def to_main(request):
    return redirect('/urine_strip')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',to_main,name="Main page redirect"),
    path('urine_strip/',include('urine_strip.urls')),
]
