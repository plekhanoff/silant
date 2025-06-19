from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('ex', 'Эксплуатант'),
        ('mn', 'Менеджер'),
        ('pr', 'Производитель'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    def __str__(self):
        return self.user.username
    
class Reference(models.Model):
    entity_name = models.CharField(max_length=100)  
    name = models.CharField(max_length=100)         
    description = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)                  

    def __str__(self):
        return f"{self.entity_name} - {self.name}"


class Machine(models.Model):
    factory_number = models.CharField(max_length=100, unique=True,null=True, blank=True)
    model = models.CharField(max_length=100,null=True, blank=True)
    engine_model = models.CharField(max_length=100,null=True, blank=True)
    engine_serial_number = models.CharField(max_length=100,null=True, blank=True) 
    transmission_model = models.CharField(max_length=100,null=True, blank=True)
    transmission_serial_number = models.CharField(max_length=100,null=True, blank=True) 
    front_axle_model = models.CharField(max_length=100,null=True, blank=True)
    front_axle_serial_number = models.CharField(max_length=100,null=True, blank=True)  
    rear_axle_model = models.CharField(max_length=100,null=True, blank=True)
    rear_axle_serial_number = models.CharField(max_length=100,null=True, blank=True)  
    supply_contract_number = models.CharField(max_length=100,null=True, blank=True)  
    shipment_date = models.DateField(null=True, blank=True) 
    consignee = models.CharField(max_length=100)  
    delivery_address = models.CharField(max_length=255)  
    equipment = models.TextField() 
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='machines')  
    service_company = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='service_machines') 
    engine_model_ref = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.SET_NULL, related_name='engine_models')
    transmission_model_ref = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.SET_NULL, related_name='transmission_models')
    model_ref = models.ForeignKey(Reference, null=True, blank=True,on_delete=models.SET_NULL, related_name='models')
    front_axle_model_ref = models.ForeignKey(Reference, null=True, blank=True,on_delete=models.SET_NULL, related_name='front_axle_models')
    rear_axle_model_ref = models.ForeignKey(Reference, null=True, blank=True,on_delete=models.SET_NULL, related_name='rear_axle_models')
    service_company_ref = models.ForeignKey(Reference, null=True, blank=True,on_delete=models.SET_NULL, related_name='service_company_machine')
    client_ref = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.SET_NULL, related_name='client')

    def __str__(self):
        return f"{self.factory_number} - {self.model}"


class Maintenance(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE) 
    maintenance_date = models.DateField(null=True, blank=True)  
    operating_hours = models.FloatField(default=0) 
    order_number = models.CharField(max_length=100) 
    order_date = models.DateField(null=True, blank=True) 
    service_company = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='maintenance_services')  
    maintenance_type_ref = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.SET_NULL, related_name='maintenance_types')
    service_company_ref = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.SET_NULL, related_name='service_company_maintenance')
    organization_ref = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.SET_NULL, related_name='organizations_maintenance')
    description_ref = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.SET_NULL, related_name='descriptions_maintenance')
     

    def __str__(self):
        type_name = self.maintenance_type_ref.name if self.maintenance_type_ref else "?"
        return f"{type_name} - {self.machine.factory_number} ({self.maintenance_date})"


class Complaint(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE) 
    failure_node = models.CharField(max_length=100)  
    recovery_method = models.CharField(max_length=100)  
    claim_date = models.DateField(null=True, blank=True) 
    operating_hours = models.FloatField(default=0)  
    failure_description = models.TextField()  
    spare_parts_used = models.TextField(default='')
    recovery_date = models.DateField(null=True, blank=True) 
    downtime_hours = models.FloatField(default=0)  
    service_company = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='complaints')  
    failure_node_ref = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.SET_NULL, related_name='failure_node')
    recovery_method_ref = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.SET_NULL, related_name='recovery_method')
    service_company_ref = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.SET_NULL, related_name='service_company_complaint')
    description_ref = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.SET_NULL, related_name='descriptions_complaint')

    def save(self, *args, **kwargs):
        if self.recovery_date and self.claim_date:
            self.downtime_hours = (self.recovery_date - self.claim_date).days * 24  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Complaint for {self.machine.factory_number} on {self.claim_date}"
