
from .models import Reference
from rest_framework import viewsets
from .forms import FactoryNumberForm, MachineForm, MaintenanceForm, ComplaintForm, ReferenceForm
from .models import Machine, Maintenance, Complaint, Reference
from .serializers import MachineSerializer, MaintenanceSerializer, ComplaintSerializer, ReferenceSerializer
from django.http import HttpResponseForbidden
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404, redirect
from django.views import View
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy



class WelcomeView(View):
    def get(self, request):
        form = FactoryNumberForm(request.GET)
        machine = None
        error_message = None

        if form.is_bound and form.is_valid():
            factory_number = form.cleaned_data.get('factory_number')
        #if factory_number:
            try:
                machine = Machine.objects.get(factory_number=factory_number)
            except Machine.DoesNotExist:
                error_message = "Машина не найдена."
            except Exception as e:
                error_message = f"Ошибка поиска: {e}"
        return render(request, 'welcome.html', {
            'form': form,
            'error_message': error_message,
            'machine': machine,
        })
        

class MachineListView(LoginRequiredMixin,ListView):
    model = Machine
    template_name = 'service/machine_list.html' 
    context_object_name = 'machines' 

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('service:request_signup') 
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['references'] = Reference.objects.all()
        return context 
    
    def get_queryset(self):
        user = self.request.user
        if user.userprofile.role in ("ex", 'mn', 'pr'):
            client_machines = Machine.objects.filter(client=user)
            service_company_machines = Machine.objects.filter(service_company=user)
            return client_machines | service_company_machines 
        return Machine.objects.all()


class MaintenanceListView(LoginRequiredMixin, ListView):
    model = Maintenance
    template_name = 'service/maintenance_list.html' 
    context_object_name = 'maintenances' 

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('service:request_signup') 
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
          
        if user.userprofile.role == 'pr':
            return Maintenance.objects.all().distinct()

        if user.userprofile.role in ("ex", 'mn', 'pr'):
            references = Reference.objects.filter(user=user)

            if user.userprofile.role == 'mn':
                return Maintenance.objects.filter(
                    Q(machine__client_ref__in=references) | 
                    Q(service_company=user)  
                ).distinct()

            return Maintenance.objects.filter(
                Q(machine__client_ref__in=references)            
            ).distinct()

        return Maintenance.objects.none 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allowed_roles'] = ["mn", "pr"] 
        return context

    def post(self, request, *args, **kwargs):
        maintenance_id = request.POST.get('maintenance_id')
        if maintenance_id:
            return redirect('service:edit_maintenance', pk=maintenance_id)
        return redirect('service:maintenance_list')


class ComplaintListView(LoginRequiredMixin,ListView):
    model = Complaint
    template_name = 'service/complaint_list.html' 
    context_object_name = 'complaints'  

    def get_queryset(self):
        return Complaint.objects.all().order_by('claim_date')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('service:request_signup') 
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user         
        if user.userprofile.role == 'pr':
            return Complaint.objects.all().distinct()
        if user.userprofile.role in ("ex", 'mn', 'pr'):
            references = Reference.objects.filter(user=user)
            if user.userprofile.role == 'mn':
                return Complaint.objects.filter(
                    Q(machine__client_ref__in=references) | 
                    Q(service_company=user)  
                ).distinct()
            return Complaint.objects.filter(
                Q(machine__client_ref__in=references)            
            ).distinct()
        return Complaint.objects.none 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allowed_roles'] = ["mn", "pr"] 
        return context
    
    def post(self, request, *args, **kwargs):
        complaint_id = request.POST.get('complaint_id')
        if complaint_id:
            return redirect('service:edit_complaint', pk=complaint_id)
        return redirect('service:complaint_list')


class RequestSignupView(TemplateView):
    template_name = 'service/request_signup.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    
class MachineDetailView(DetailView):
    model = Machine
    template_name = 'service/machine_detail.html'
    context_object_name = 'machine'

    def get(self, request, *args, **kwargs):
        machine = self.get_object()
        return render(request, self.template_name, {'machine': machine})
    
    
class EditMachineView(UpdateView,UserPassesTestMixin):
    model = Machine
    fields = ['model', 'engine_model', 'transmission_model', 'front_axle_model', 'rear_axle_model', 'shipment_date']
    template_name = 'service/edit_machine.html'
    success_url = reverse_lazy('service:machine_list')
    
    def test_func(self):
             # return self.request.user.is_authenticated and getattr(self.request.user, 'is_producer', False)           
             return self.request.user.is_authenticated and self.request.user.userprofile.role == 'pr'
    
    def edit_machine(request, pk):
        machine = get_object_or_404(Machine, pk=pk)
        if request.method == 'POST':
            form = MachineForm(request.POST, instance=machine)
            if form.is_valid():
                form.save()
                return redirect('service:machine_detail', pk=machine.pk)
        else:
            form = MachineForm(instance=machine)
        return render(request, 'service/edit_machine.html', {'form': form})
    
    
class EditMaintenanceView(UpdateView):
    model = Maintenance
    fields = "__all__"
    template_name = 'service/edit_maintenance.html'
    success_url = reverse_lazy('service:maintenance_list')

class EditComplaintView(UpdateView):
    model = Complaint
    fields = "__all__"
    template_name = 'service/edit_complaint.html'
    success_url = reverse_lazy('service:complaint_list')


class ReferenceCreateView(CreateView):
    model = Reference
    form_class = ReferenceForm
    template_name = 'service/reference_form.html'
    success_url = reverse_lazy('service:reference_list')
    
class ReferenceUpdateView(UpdateView):
    model = Reference
    form_class = ReferenceForm
    template_name = 'service/reference_form.html'
    success_url = reverse_lazy('service:reference_list')    

class ReferenceListView(ListView):
    model = Reference
    template_name = 'service/reference_list.html'
    context_object_name = 'references'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q') 
        if query:
            queryset = queryset.filter(Q(entity_name__icontains=query) | Q(name__icontains=query))
        return queryset


@login_required
def add_machine(request):
    try:
        role = request.user.userprofile.role
    except AttributeError:
        return HttpResponseForbidden('Профиль пользователя не найден.')

    if role != 'pr':
        return HttpResponseForbidden('Доступ разрешён только производителю.')

    if request.method == 'POST':
        form = MachineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service:machine_list') 
    else:
        form = MachineForm()
    return render(request, 'service/add_machine.html', {'form': form})


@login_required
def add_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, user=request.user)
        if form.is_valid():
            machine = form.cleaned_data['machine']
            role = request.user.userprofile.role
            access = False
            
            if role == 'pr':
                access = True 
            elif role == 'ex':
                access = (machine.client == request.user) 
            elif role == 'mn':
                access = (machine.service_company == request.user)  
            else:
                access = False 

            if not access:
                form.add_error('machine', 'Нет доступа к выбранной машине')
            else:
                form.save()
                return redirect('service:maintenance_list')
    else:
        form = MaintenanceForm(user=request.user)

    return render(request, 'service/add_maintenance.html', {'form': form})


@login_required
def add_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, user=request.user)
        if form.is_valid():
            machine = form.cleaned_data['machine']
            role = request.user.userprofile.role
            access = False
            if role == 'pr':
                access = True
            elif role == 'ex':
                access = (machine.client == request.user)
                access = False
            elif role == 'mn':
                access = (machine.service_company == request.user)
            else:
                access = False 
                   
            if not access:
                form.add_error('machine', 'Нет доступа к выбранной машине')
            else:
                form.save()
                return redirect('service:complaint_list')
    else:
        form = ComplaintForm(user=request.user)
    return render(request, 'service/add_complaint.html', {'form': form})


 
   
class MachineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Machine.objects.all().order_by('shipment_date') 
    serializer_class = MachineSerializer

class MaintenanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Maintenance.objects.all().order_by('maintenance_date') 
    serializer_class = MaintenanceSerializer

class ComplaintViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Complaint.objects.all().order_by('claim_date') 
    serializer_class = ComplaintSerializer
