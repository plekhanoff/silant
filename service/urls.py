from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views
from .views import add_machine, add_maintenance, add_complaint
from .views import ReferenceCreateView, ReferenceListView, ReferenceUpdateView
from .views import EditMaintenanceView
from django.contrib.auth.views import LogoutView

app_name = 'service' 


schema_view = get_schema_view(
    openapi.Info(
        title="Сервис Силант API",
        default_version='v1',
        description="Документация API для сервиса Силант",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@silant.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.WelcomeView.as_view(), name='welcome'),
    path('logout/', LogoutView.as_view(next_page='welcome'), name='logout'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('machines/', views.MachineListView.as_view(), name='machine_list'),
    path('maintenance/',views. MaintenanceListView.as_view(), name='maintenance_list'),
    path('complaints/',views. ComplaintListView.as_view(), name='complaint_list'),
    path('request_signup/',views. RequestSignupView.as_view(), name='request_signup'),
    path('machine/<int:pk>/',views. MachineDetailView.as_view(), name='machine_detail'),
    path('machines/add/', add_machine, name='add_machine'),
    path('maintenance/add/', add_maintenance, name='add_maintenance'),
    path('complaints/add/', add_complaint, name='add_complaint'),
    path('machine/<int:pk>/edit/', views.EditMachineView.as_view(), name='edit_machine'),
    path('maintenance/<int:pk>/edit/', EditMaintenanceView.as_view(), name='edit_maintenance'),
    path('complaint/<int:pk>/edit/', views.EditComplaintView.as_view(), name='edit_complaint'),
    path('references/add/', ReferenceCreateView.as_view(), name='reference_add'),
    path('references/', ReferenceListView.as_view(), name='reference_list'),
    path('references/<int:pk>/edit/', ReferenceUpdateView.as_view(), name='reference_edit'),

]
