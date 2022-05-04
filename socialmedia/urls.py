"""socialmedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path("sign_up",views.sign_up),
    path("show_posts/",views.show_posts),
    path("create_user",views.create_user),
    path("add_post/",views.add_post),
    path("delete_post/",views.delete_post),
    path("log_in/",views.log_in),
    path("log_out/",views.log_out),
    path("user/account/",views.account),
    path("user/update_profile/",views.update_profile),
]
