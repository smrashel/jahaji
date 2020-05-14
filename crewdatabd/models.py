from django.db import models
from django.conf import settings

# Create your models here.
from django.db.models import SET_NULL


class District(models.Model):
    district_name = models.CharField('District', max_length=200)

    def __str__(self):
        return self.district_name


class Thana(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    thana_name = models.CharField('Thana', max_length=200)

    def __str__(self):
        return self.thana_name


class Association(models.Model):
    CENTRAL = 'central'
    REGIONAL = 'regional'
    OWNER = "Owner's Association"
    LABOR = "Labor's Association"

    ASSOCIATION_TYPE_CHOICES = [
        (OWNER, "Owner's Association"),
        (LABOR, "Labor's Association"),
    ]
    ZONE_TYPE_CHOICES = [
        (CENTRAL, 'Central'),
        (REGIONAL, 'Regional'),
    ]
    association_name = models.CharField('Association Name', max_length=200)
    association_type = models.CharField('Association Type', max_length=200, choices=ASSOCIATION_TYPE_CHOICES)
    zone = models.CharField('Zone', max_length=200, choices=ZONE_TYPE_CHOICES, null=True, blank=True)
    association_address = models.CharField('Address', max_length=200, null=True, blank=True)
    registration_number = models.CharField('Registration Number', unique=True, max_length=200, null=True, blank=True)
    contact_person_1 = models.CharField('Contact Person-1', max_length=200, null=True, blank=True)
    position_1 = models.CharField('Position-1', max_length=200, null=True, blank=True)
    contact_number_1 = models.CharField('Contact No-1', unique=True, max_length=200, null=True, blank=True)
    contact_person_2 = models.CharField('Contact Person-2', max_length=200, null=True, blank=True)
    position_2 = models.CharField('Position-2', max_length=200, null=True, blank=True)
    contact_number_2 = models.CharField('Contact No-2', unique=True, max_length=200, null=True, blank=True)
    association_email = models.EmailField('Email', max_length=200, null=True, blank=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.association_name


class Companie(models.Model):
    company_name = models.CharField('Company Name', max_length=200)
    owner_name = models.CharField('Owner Name', max_length=200, null=True, blank=True)
    owner_contact = models.CharField('Owner Contact', unique=True, max_length=200, null=True, blank=True)
    owners_association = models.ManyToManyField(Association,
                                                limit_choices_to={'association_type': "Owner's Association"},
                                                null=True, blank=True)
    manager_name = models.CharField('Manager Name', max_length=200, null=True, blank=True)
    manager_contact = models.CharField('Manager Contact', unique=True, max_length=200, null=True, blank=True)
    company_address = models.CharField('Address', max_length=200, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    thana = models.ForeignKey(Thana, on_delete=models.SET_NULL, null=True, blank=True)
    company_email = models.EmailField('Email', max_length=200, null=True, blank=True)
    charter_company = models.CharField('Charter Company', max_length=200, null=True, blank=True)
    cc_contact_person = models.CharField('CC Contact Person', max_length=200, null=True, blank=True)
    cc_contact_no = models.CharField('CC Contact No', max_length=200, null=True, blank=True)
    cc_address = models.CharField('CC Address', max_length=200, null=True, blank=True)
    cc_email = models.EmailField('CC Email', max_length=200, null=True, blank=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.company_name


class VesselType(models.Model):
    vessel_type = models.CharField('Ship Type', max_length=200)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.vessel_type


class GoodsType(models.Model):
    goods_type = models.CharField('Goods Type', max_length=200)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.goods_type


class Vessel(models.Model):
    company = models.ForeignKey(Companie, on_delete=models.CASCADE)
    ship_name = models.CharField('Ship Name', max_length=200)
    registration_number = models.CharField('Registration Number', unique=True, max_length=200, null=True, blank=True)
    ship_type = models.ForeignKey(VesselType, on_delete=models.CASCADE)
    ship_capacity = models.CharField('Ship Capacity', max_length=200, null=True, blank=True)
    goods_type = models.ForeignKey(GoodsType, on_delete=models.SET_NULL, blank=True, null=True)
    max_draft = models.CharField('Max Draft (Feet)', max_length=200, null=True, blank=True)
    route_name = models.CharField('Route Name', max_length=200, null=True, blank=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.ship_name


class Position(models.Model):
    position = models.CharField('Position', unique=True, max_length=200)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.position


class EducationLevel(models.Model):
    education_level = models.CharField('Education Level', unique=True, max_length=200)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.education_level


class MobileMoneyAccount(models.Model):
    account = models.CharField('Account', unique=True, max_length=200)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.account


class ShippingStaff(models.Model):
    APOSITIVE = 'A+'
    ANEGATIVE = 'A-'
    ABPOSITIVE = 'AB+'
    ABNEGATIVE = 'AB-'
    BPOSITIVE = 'B+'
    BNEGATIVE = 'B-'
    OPOSITIVE = 'O+'
    ONEGATIVE = 'O-'

    TOUCH = 'touch'
    BUTTON = 'button'
    BLOOD_GROUP_CHOICES = [
        (APOSITIVE, 'A Positive'),
        (ANEGATIVE, 'A Negative'),
        (ABPOSITIVE, 'AB Positive'),
        (ABNEGATIVE, 'AB Negative'),
        (BPOSITIVE, 'B Positive'),
        (BNEGATIVE, 'B Negative'),
        (OPOSITIVE, 'O Positive'),
        (ONEGATIVE, 'O Negative'),
    ]

    MOBILE_TYPE_CHOICES = [
        (TOUCH, 'Touch'),
        (BUTTON, 'Button'),
    ]
    company = models.ForeignKey(Companie, on_delete=models.CASCADE)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    full_name = models.CharField('Full Name', max_length=200)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    contact_number = models.CharField('Contact Number', unique=True, max_length=200, null=True, blank=True)
    home_address = models.CharField('Address', max_length=200, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    thana = models.ForeignKey(Thana, on_delete=models.CASCADE, null=True, blank=True)
    family_members = models.CharField('Family Members', max_length=200, null=True, blank=True)
    monthly_salary = models.IntegerField('Monthly Salary', null=True, blank=True)
    avg_family_m_income = models.IntegerField('AVG Family Income/Month', null=True, blank=True)
    birth_date = models.DateField('Date of Birth', null=True, blank=True)
    nid_number = models.CharField('NID Number', unique=True, null=True, max_length=200, blank=True)
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, null=True, blank=True)
    professional_certificate = models.CharField('Professional Certificate', max_length=200, null=True, blank=True)
    mobile_type = models.CharField('Mobile Type', max_length=200, choices=MOBILE_TYPE_CHOICES, null=True, blank=True)
    bank_account = models.BooleanField('Bank Account', null=True, blank=True)
    mobile_money_account = models.ForeignKey(MobileMoneyAccount, on_delete=models.CASCADE, null=True, blank=True)
    blood_group = models.CharField('Blood Group', max_length=200, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    affiliated_association = models.ManyToManyField(Association,
                                                    limit_choices_to={'association_type': "Labor's Association"},
                                                    null=True, blank=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Ghat(models.Model):
    ghat_name = models.CharField('Ghat Name', max_length=200)
    leaseholder_name = models.CharField('Leaseholder Name', max_length=200)
    leaseholder_contact = models.CharField('Leaseholder Contact', unique=True, max_length=200)
    manager_name = models.CharField('Manager Name', max_length=200, null=True, blank=True)
    manager_contact = models.CharField('Manager Contact', unique=True, max_length=200, null=True, blank=True)
    labor_leader_name = models.CharField('Labor Sordar Name', max_length=200, null=True, blank=True)
    labor_leader_contact = models.CharField('Labor Sordar Contact', unique=True, max_length=200, null=True, blank=True)
    river_name = models.CharField('River Name', max_length=200, null=True, blank=True)
    ghat_address = models.CharField('Address', max_length=200, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    thana = models.ForeignKey(Thana, on_delete=models.CASCADE)
    ghat_coordinate = models.CharField('Ghat Latitude and Longitude', max_length=200, null=True, blank=True)
    ghat_email = models.EmailField('Email', max_length=200, null=True, blank=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.ghat_name


class GhatLabor(models.Model):
    APOSITIVE = 'A+'
    ANEGATIVE = 'A-'
    ABPOSITIVE = 'AB+'
    ABNEGATIVE = 'AB-'
    BPOSITIVE = 'B+'
    BNEGATIVE = 'B-'
    OPOSITIVE = 'O+'
    ONEGATIVE = 'O-'

    TOUCH = 'touch'
    BUTTON = 'button'

    LABOR = 'Labor'
    BOATMAN = 'Boatman'
    OTHER = 'Other'

    BLOOD_GROUP_CHOICES = [
        (APOSITIVE, 'A Positive'),
        (ANEGATIVE, 'A Negative'),
        (ABPOSITIVE, 'AB Positive'),
        (ABNEGATIVE, 'AB Negative'),
        (BPOSITIVE, 'B Positive'),
        (BNEGATIVE, 'B Negative'),
        (OPOSITIVE, 'O Positive'),
        (ONEGATIVE, 'O Negative'),
    ]

    MOBILE_TYPE_CHOICES = [
        (TOUCH, 'Touch'),
        (BUTTON, 'Button'),
    ]

    GHAT_LABOR_POSITION = [
        (LABOR, 'Labor'),
        (BOATMAN, 'Boatman'),
        (OTHER, 'Other')
    ]
    ghat_district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='+')
    ghat_thana = models.ForeignKey(Thana, on_delete=models.CASCADE, related_name='+')
    ghat_name = models.ForeignKey(Ghat, on_delete=models.CASCADE)
    labor_name = models.CharField('Labor Name', max_length=200)
    labor_position = models.CharField('Labor Position', max_length=200, choices=GHAT_LABOR_POSITION)
    labor_contact = models.CharField('Labor Contact', unique=True, max_length=200, null=True, blank=True)
    labor_address = models.CharField('Address', max_length=200, null=True, blank=True)
    address_district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    address_thana = models.ForeignKey(Thana, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    family_members = models.CharField('Family Members', max_length=200, null=True, blank=True)
    avg_daily_income = models.IntegerField('AVG Daily Income', null=True, blank=True)
    avg_working_day_m = models.IntegerField('AVG Working Day/Month', null=True, blank=True)
    avg_family_income_m = models.IntegerField('AVG Family Income/Month', null=True, blank=True)
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, null=True, blank=True)
    birth_date = models.DateField('Date of Birth', null=True, blank=True)
    nid_number = models.CharField('NID Number', unique=True, null=True, max_length=200, blank=True)
    mobile_type = models.CharField('Mobile Type', max_length=200, choices=MOBILE_TYPE_CHOICES, null=True, blank=True)
    bank_account = models.BooleanField('Bank Account', null=True, blank=True)
    mobile_money_account = models.ForeignKey(MobileMoneyAccount, on_delete=models.CASCADE, null=True, blank=True)
    blood_group = models.CharField('Blood Group', max_length=200, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.labor_name
