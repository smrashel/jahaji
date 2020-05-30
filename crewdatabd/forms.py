from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime
from django import forms
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AssociationForm(ModelForm):
    class Meta:
        model = Association
        widgets = {
            'association_name': forms.TextInput(attrs={'class': 'form-control'}),
            'association_type': forms.Select(attrs={'class': 'form-control'}),
            'zone': forms.Select(attrs={'class': 'form-control'}),
            'association_address': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person_1': forms.TextInput(attrs={'class': 'form-control'}),
            'position_1': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number_1': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person_2': forms.TextInput(attrs={'class': 'form-control'}),
            'position_2': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number_2': forms.TextInput(attrs={'class': 'form-control'}),
            'association_email': forms.TextInput(attrs={'class': 'form-control'}),
            'association_website': forms.TextInput(attrs={'class': 'form-control'}),
        }
        exclude = ['added_by', 'updated_by', 'updated_date']


class CompanieForm(ModelForm):
    class Meta:
        model = Companie
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'owner_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'owners_association': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'manager_name': forms.TextInput(attrs={'class': 'form-control'}),
            'manager_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'thana': forms.Select(attrs={'class': 'form-control'}),
            'company_email': forms.TextInput(attrs={'class': 'form-control'}),
            'charter_company': forms.TextInput(attrs={'class': 'form-control'}),
            'cc_contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'cc_contact_no': forms.TextInput(attrs={'class': 'form-control'}),
            'cc_address': forms.TextInput(attrs={'class': 'form-control'}),
            'cc_email': forms.TextInput(attrs={'class': 'form-control'}),
        }
        exclude = ['added_by', 'updated_by', 'updated_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['thana'].queryset = Thana.objects.none()

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['thana'].queryset = Thana.objects.filter(district=district_id).order_by('thana_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Thana queryset
        elif self.instance.pk:
            self.fields['thana'].queryset = self.instance.district.thana_set.order_by('thana_name')


class ShipForm(ModelForm):
    class Meta:
        model = Vessel
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),
            'ship_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ship_type': forms.Select(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'ship_capacity': forms.TextInput(attrs={'class': 'form-control'}),
            'goods_type': forms.Select(attrs={'class': 'form-control'}),
            'max_draft': forms.TextInput(attrs={'class': 'form-control'}),
            'ship_length': forms.TextInput(attrs={'class': 'form-control'}),
            'year_built': forms.TextInput(attrs={'class': 'form-control'}),
            'route_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        exclude = ['added_by', 'updated_by', 'updated_date']


class ShippingStaffForm(ModelForm):
    class Meta:
        model = ShippingStaff
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),
            'vessel': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'staff_class': forms.Select(attrs={'class': 'form-control'}),
            'joining_year': forms.TextInput(attrs={'class': 'form-control'}),
            'home_address': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'thana': forms.Select(attrs={'class': 'form-control'}),
            'monthly_salary': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.TextInput(attrs={'class': 'form-control jq-datepicker'}),
            'education_level': forms.Select(attrs={'class': 'form-control'}),
            'family_members': forms.TextInput(attrs={'class': 'form-control'}),
            'avg_family_m_income': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_type': forms.Select(attrs={'class': 'form-control'}),
            'mobile_money_account': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'nid_number': forms.TextInput(attrs={'class': 'form-control'}),
            'affiliated_association': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        exclude = ['added_by', 'updated_by', 'updated_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['thana'].queryset = Thana.objects.none()

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['thana'].queryset = Thana.objects.filter(district=district_id).order_by('thana_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Thana queryset
        elif self.instance.pk:
            self.fields['thana'].queryset = self.instance.district.thana_set.order_by('thana_name')

        if 'company' in self.data:
            try:
                company_id = int(self.data.get('company'))
                self.fields['vessel'].queryset = Vessel.objects.filter(company=company_id).order_by('ship_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Thana queryset
        elif self.instance.pk:
            self.fields['vessel'].queryset = self.instance.company.vessel_set.order_by('ship_name')


class GhatForm(ModelForm):
    class Meta:
        model = Ghat
        widgets = {
            'ghat_name': forms.TextInput(attrs={'class': 'form-control'}),
            'leaseholder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'leaseholder_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'manager_name': forms.TextInput(attrs={'class': 'form-control'}),
            'manager_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'labor_leader_name': forms.TextInput(attrs={'class': 'form-control'}),
            'labor_leader_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'river_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ghat_address': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'thana': forms.Select(attrs={'class': 'form-control'}),
            'ghat_coordinate': forms.TextInput(attrs={'class': 'form-control'}),
            'ghat_email': forms.TextInput(attrs={'class': 'form-control'}),
        }
        exclude = ['added_by', 'updated_by', 'updated_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['thana'].queryset = Thana.objects.none()

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['thana'].queryset = Thana.objects.filter(district=district_id).order_by('thana_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Thana queryset
        elif self.instance.pk:
            self.fields['thana'].queryset = self.instance.district.thana_set.order_by('thana_name')


class GhatLaborForm(ModelForm):
    class Meta:
        model = GhatLabor
        widgets = {
            'ghat_district': forms.Select(attrs={'class': 'form-control'}),
            'ghat_thana': forms.Select(attrs={'class': 'form-control'}),
            'ghat_name': forms.Select(attrs={'class': 'form-control'}),
            'labor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'labor_position': forms.Select(attrs={'class': 'form-control'}),
            'labor_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'labor_address': forms.TextInput(attrs={'class': 'form-control'}),
            'address_district': forms.Select(attrs={'class': 'form-control'}),
            'address_thana': forms.Select(attrs={'class': 'form-control'}),
            'family_members': forms.TextInput(attrs={'class': 'form-control'}),
            'avg_daily_income': forms.TextInput(attrs={'class': 'form-control'}),
            'avg_working_day_m': forms.TextInput(attrs={'class': 'form-control'}),
            'avg_family_income_m': forms.TextInput(attrs={'class': 'form-control'}),
            'education_level': forms.Select(attrs={'class': 'form-control'}),
            'birth_date': forms.TextInput(attrs={'class': 'form-control'}),
            'nid_number': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_type': forms.Select(attrs={'class': 'form-control'}),
            'bank_account': forms.CheckboxInput(attrs={'class': ''}),
            'mobile_money_account': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'ghat_coordinate': forms.TextInput(attrs={'class': 'form-control'}),
            'ghat_email': forms.TextInput(attrs={'class': 'form-control'}),
        }
        exclude = ['added_by', 'updated_by', 'updated_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ghat_thana'].queryset = Thana.objects.none()
        self.fields['address_thana'].queryset = Thana.objects.none()

        if 'ghat_district' in self.data:
            try:
                district_id = int(self.data.get('ghat_district'))
                self.fields['ghat_thana'].queryset = Thana.objects.filter(district=district_id).order_by('thana_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Thana queryset
        elif self.instance.pk:
            self.fields['ghat_thana'].queryset = self.instance.ghat_district.thana_set.order_by('thana_name')

        if 'address_district' in self.data:
            try:
                district_id = int(self.data.get('address_district'))
                self.fields['address_thana'].queryset = Thana.objects.filter(district=district_id).order_by('thana_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Thana queryset
        elif self.instance.pk:
            self.fields['address_thana'].queryset = self.instance.address_district.thana_set.order_by('thana_name')


class ExternalStakeholderForm(ModelForm):
    class Meta:
        model = ExternalStakeholder
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'org_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'sector': forms.Select(attrs={'class': 'form-control'}),
            'contact_1': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_2': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),
            'social_url': forms.TextInput(attrs={'class': 'form-control'}),
        }
        exclude = ['added_by', 'updated_by', 'updated_date']