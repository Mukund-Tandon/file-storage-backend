"""file_storage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from api import views

urlpatterns = [
    path('upload_files/',views.upload_files,name='upload_files'),
    path('check_server/',views.check_server,name='check_server'),
    path('get_files/<str:pk>',views.get_all_files,name='get_files'),
    path('get_space_used/<str:pk>',views.get_space_used,name='get_space_used'),
    path('get_user_data/<str:pk>',views.get_user_data,name='get_user_data'),
    path('create_new_user/',views.create_new_user,name='create_new_user'),
    path('stripe_home/<str:user_id>', views.home, name='stripe_home'),
    path('config/', views.stripe_config,name='config'),
    path('success/', views.success,name='success'),  # new
    path('cancel/', views.cancel,name='cancel'),
    path('create-checkout-session/<str:user_id>', views.create_checkout_session,name='create-checkout-session'),
    path('webhook/', views.stripe_webhook,name='webhook'),
    path('subcribtion_details/<str:user_id>', views.subcribtion_details,name='subcribtion_details'),
    path('cancel_subcribtion/<str:user_id>', views.cancel_subcribtion,name='cancel_subcribtion'),
    path('get_file/<str:email>/<str:file_name>', views.get_file, name='get_file'),
    path('get_sharable_file/<str:email>/<str:file_name>', views.get_sharable_file, name='get_sharable_file'),
    path('update_file_visibility/<str:email>/<str:file_name>/<str:value>', views.update_file_visibility, name='update_file_visibility'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()
