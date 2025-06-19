from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/service/', include('service.urls')),
    path('', RedirectView.as_view(url='/api/service/')),
    path('welcome/', TemplateView.as_view(template_name='welcome.html'), name='welcome'),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view(next_page='welcome'), name='logout'),
]
