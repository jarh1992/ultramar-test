"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include
#from .views import HomeView

from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from logistic import views
from user_app import views as uv
from user_app.views import UserView

urlpatterns = [
    re_path(r'^panel/', views.PanelView.as_view(), name='panel'),
    re_path(r'^signup/$', uv.CustomUserCreationView.as_view(), name='signup'),
    re_path(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^$', RedirectView.as_view(url='login', permanent=False)),
    path('user', UserView.as_view(), name='user'),
    #path('apicon', views.ApiView.as_view(), name='apicon'),
    path('password_change/',
        auth_views.PasswordChangeView.as_view(template_name='pages/user_man/profile.html'),
        name='password_change'),
    path('password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='pages/user_man/profile.html'),
        name='password_change_done'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#urlpatterns = [
#    path("", HomeView.as_view(), name="HomeView"),
#]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)    
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
