from django import forms
from .models import Machine, Maintenance, Complaint, Reference

class FactoryNumberForm(forms.Form):
    factory_number = forms.CharField(label='Заводской номер', max_length=100)


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = "__all__"
        widgets = {
            'shipment_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = "__all__"
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        role = user.userprofile.role

        if role == 'pr':
            pass  
        elif role == 'mn':
            self.fields['machine'].queryset = Machine.objects.filter(service_company=user)
        elif role == 'ex':
            self.fields['machine'].queryset = Machine.objects.filter(client=user)
        else:  
            self.fields['machine'].queryset = Machine.objects.none()
            
              
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = "__all__"
        widgets = {
            'claim_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        role = user.userprofile.role

        if role == 'pr':
            pass  
        elif role == 'mn':
            self.fields['machine'].queryset = Machine.objects.filter(service_company=user)
        elif role == 'ex':
            self.fields['machine'].queryset = Machine.objects.filter(client=user)
        else:  
            self.fields['machine'].queryset = Machine.objects.none()
            
            

class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ['entity_name', 'name', 'description']

