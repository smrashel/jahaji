import io

from django.db.models import Count, Sum, Avg, FloatField
from django.db.models.functions import Cast
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

##
from django.views.generic import View
from django.utils import timezone
import datetime

from .models import *
from .forms import *
from .decorators import *


# Create your views here.

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect.')

    context = {}
    return render(request, 'crewdatabd/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    shipping_staff_point = ShippingStaff.objects.values('added_by').annotate(name=Count('full_name'), position=Count('position'), mobile=Count('contact_number'), address=Count('home_address'), district=Count('district'))

    ship_count = Vessel.objects.count()
    staff_count = ShippingStaff.objects.aggregate(staff_count=Count('id', distinct=True), association_count=Count('affiliated_association', distinct=True))
    shipping_staff = ShippingStaff.objects.aggregate(staff_count=Count('full_name'),
                                                     avg_family_members=Avg('family_members'),
                                                     avg_m_income=Avg('monthly_salary'),
                                                     avg_f_income=Avg('avg_family_m_income'),
                                                     dst_position=Count('position', distinct=True))
    company_count = Companie.objects.aggregate(member_count=Count('id', distinct=True),
                                                  association_count=Count('owners_association', distinct=True))
    vessel_staffs = VesselType.objects.values('vessel_type').annotate(vessel_count=Count('vessel__ship_type'),
                                                                      staff_count=Count(
                                                                          'vessel__shippingstaff__full_name'))
    association = Association.objects.aggregate(acount=Count('association_name'))
    owners_associations = Association.objects.values('zone').annotate(member=Count('companie__company_name'))
    labors_associations = Association.objects.values('zone').annotate(member=Count('shippingstaff__full_name'))
    ghat = Ghat.objects.aggregate(ghat_count=Count('ghat_name'), district_count=Count('district', distinct=True))
    ghat_labor = GhatLabor.objects.aggregate(labor_count=Count('labor_name'), avg_family_members=Avg('family_members'), avg_d_income=Avg('avg_daily_income'), avg_f_income=Avg('avg_family_income_m'))

    context = {'company_count': company_count, 'ship_count': ship_count,
               'association': association, 'ghat': ghat, 'ghat_labor': ghat_labor, 'staff_count': staff_count,
               'shipping_staff': shipping_staff, 'vessel_staffs': vessel_staffs, 'owners_associations': owners_associations,
               'labors_associations': labors_associations}
    return render(request, 'crewdatabd/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'vessel', 'ghat'])
def load_thanas(request):
    district_id = request.GET.get('district')
    thanas = Thana.objects.filter(district=district_id).order_by('thana_name')
    context = {'thanas': thanas}
    return render(request, 'crewdatabd/thana.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'ghat'])
def load_ghat_thanas(request):
    district_id = request.GET.get('district')
    thanas = Thana.objects.filter(district=district_id).order_by('thana_name')

    return render(request, 'crewdatabd/thana.html', {'thanas': thanas})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'ghat'])
def load_ghats(request):
    thana_id = request.GET.get('thana')
    ghats = Ghat.objects.filter(thana=thana_id).order_by('ghat_name')
    return render(request, 'crewdatabd/ghat_select_options.html', {'ghats': ghats})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'vessel'])
def load_vessels(request):
    company_id = request.GET.get('company')
    vessels = Vessel.objects.filter(company=company_id).order_by('ship_name')
    return render(request, 'crewdatabd/ship_select_options.html', {'vessels': vessels})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'jahaji', 'viewer'])
def companies(request):
    # companies = Companie.objects.all()
    companies = Companie.objects.annotate(no_of_vessel=Count('vessel'))

    context = {'companies': companies}
    return render(request, 'crewdatabd/companies.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'jahaji', 'viewer'])
def companyShips(request, pk):
    company = get_object_or_404(Companie, id=pk)
    ships = Vessel.objects.filter(company=pk)
    context = {'company': company, 'ships': ships}
    return render(request, 'crewdatabd/company_ships.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'jahaji'])
def createCompany(request):
    form = CompanieForm()
    heading = 'Create Company'

    if request.method == 'POST':
        form = CompanieForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.added_by = request.user
            fs.save()

            form.save_m2m()

            company = form.cleaned_data.get('company_name')
            messages.success(request, 'Company  was created for ' + company + '.')
            return redirect('companies')

    context = {'form': form, 'heading': heading}
    return render(request, 'crewdatabd/company.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'jahaji'])
def updateCompany(request, pk):
    company = get_object_or_404(Companie, id=pk)
    form = CompanieForm(instance=company)
    heading = 'Update Company'

    if request.method == 'POST':
        form = CompanieForm(request.POST, instance=company)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.updated_by = request.user
            fs.updated_date = timezone.now()
            fs.save()

            form.save_m2m()
            company = form.cleaned_data.get('company_name')
            messages.success(request, 'Company was updated for ' + company + '.')
            return redirect('companies')

    context = {'form': form, 'heading': heading}
    return render(request, 'crewdatabd/company.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'jahaji'])
def deleteCompany(request, pk):
    company = get_object_or_404(Companie, id=pk)
    item = company.company_name
    heading = 'Delete Company'

    if request.method == 'POST':
        company.delete()
        messages.success(request, 'Deleted Company was ' + item + '.')
        return redirect('companies')

    context = {'company': company, 'heading': heading}
    return render(request, 'crewdatabd/company_delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'viewer'])
def associations(request):
    # associations = Association.objects.all()
    associations = Association.objects.annotate(no_of_member=Count('companie'))
    context = {'associations': associations}
    return render(request, 'crewdatabd/associations.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'viewer'])
def associationCompanies(request, pk):
    association = get_object_or_404(Association, id=pk)
    companies = Companie.objects.filter(owners_association=pk)
    context = {'association': association, 'companies': companies}
    return render(request, 'crewdatabd/association_companies.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def createAssociation(request):
    form = AssociationForm()
    heading = 'Create Association'

    if request.method == 'POST':
        form = AssociationForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.added_by = request.user
            fs.save()

            form.save_m2m()
            association = form.cleaned_data.get('association_name')
            messages.success(request, 'Association  was created for ' + association + '.')
            return redirect('associations')

    context = {'form': form, 'heading': heading}
    return render(request, 'crewdatabd/form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def updateAssociation(request, pk):
    association = get_object_or_404(Association, id=pk)
    form = AssociationForm(instance=association)
    heading = 'Update Association'

    if request.method == 'POST':
        form = AssociationForm(request.POST, instance=association)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.updated_by = request.user
            fs.updated_date = timezone.now()
            fs.save()

            form.save_m2m()
            association = form.cleaned_data.get('association_name')
            messages.success(request, 'Association was updated for ' + association + '.')
            return redirect('associations')

    context = {'form': form, 'heading': heading}
    return render(request, 'crewdatabd/form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def deleteAssociation(request, pk):
    association = get_object_or_404(Association, id=pk)
    item = association.association_name
    heading = 'Delete Association'

    if request.method == 'POST':
        association.delete()
        messages.success(request, 'Deleted Association was ' + item + '.')
        return redirect('associations')

    context = {'association': association, 'heading': heading}
    return render(request, 'crewdatabd/association_delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'vessel', 'jahaji', 'viewer'])
def ship(request):
    ships = Vessel.objects.all()
    context = {'ships': ships}
    return render(request, 'crewdatabd/ships.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['user', 'admin', 'vessel', 'jahaji'])
def createShip(request):

    form = ShipForm()
    heading = 'Create Ship'

    if request.method == 'POST':
        form = ShipForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.added_by = request.user
            fs.save()

            form.save_m2m()
            ship = form.cleaned_data.get('ship_name')
            messages.success(request, 'Ship  was created for ' + ship + '.')
            return redirect('ships')

    context = {'form': form, 'heading': heading}
    return render(request, 'crewdatabd/ship.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'vessel', 'jahaji'])
def updateShip(request, pk):
    ship = get_object_or_404(Vessel, id=pk)
    form = ShipForm(instance=ship)
    heading = 'Update Ship'

    if request.method == 'POST':
        form = ShipForm(request.POST, instance=ship)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.updated_by = request.user
            fs.updated_date = timezone.now()
            fs.save()

            form.save_m2m()
            ship = form.cleaned_data.get('ship_name')
            messages.success(request, 'Ship  was updated for ' + ship + '.')
            return redirect('ships')

    context = {'form': form, 'heading': heading}
    return render(request, 'crewdatabd/ship.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'vessel', 'jahaji'])
def deleteShip(request, pk):
    ship = get_object_or_404(Vessel, id=pk)
    heading = 'Delete Ship'
    item = ship.ship_name

    if request.method == 'POST':
        ship.delete()
        messages.success(request, 'Deleted Ship was ' + item + '.')
        return redirect('ships')

    context = {'ship': ship, 'heading': heading}
    return render(request, 'crewdatabd/ship_delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'vessel', 'viewer'])
def seafarers(request):
    seafarers = ShippingStaff.objects.all()
    context = {'seafarers': seafarers}
    return render(request, 'crewdatabd/seafarers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'vessel'])
def seafarer_stats(request):
    start_date = datetime.date.today()
    end_date = datetime.date.today() + datetime.timedelta(days=1)
    if request.method == 'POST':
        start_date = request.POST.get('start_date', False)
        end_date = request.POST.get('end_date', False)

        shipping_staff_points = ShippingStaff.objects.filter(added_date__gte=start_date, added_date__lte=end_date).values('added_by__username').annotate(full_points=Count('full_name')*20,
        ach_points=(Count('full_name')*1+Count('position')*1+Count('contact_number')*1+Count('home_address')*2+Count('district')*0
        +Count('thana')*1+Count('nid_number')*2+Count('monthly_salary')*2+Count('family_members')*1+Count('avg_family_m_income')*2
        +Count('birth_date')*1+Count('education_level')*2+Count('mobile_type')*1+Count('mobile_money_account')*1+Count('bank_account')*1
        +Count('blood_group')*1)).annotate(achv_payment=(Cast('ach_points', FloatField()))*.5)

        context = {'shipping_staff_points': shipping_staff_points}
        return render(request, 'crewdatabd/seafarer_stats.html', context)

    shipping_staff_points = ShippingStaff.objects.filter(added_date__gte=start_date, added_date__lte=end_date).values('added_by__username').annotate(full_points=Count('full_name')*20,
    ach_points=(Count('full_name')*1+Count('position')*1+Count('contact_number')*1+Count('home_address')*2+Count('district')*0
    +Count('thana')*1+Count('nid_number')*2+Count('monthly_salary')*2+Count('family_members')*1+Count('avg_family_m_income')*2
    +Count('birth_date')*1+Count('education_level')*2+Count('mobile_type')*1+Count('mobile_money_account')*1+Count('bank_account')*1
    +Count('blood_group')*1)).annotate(achv_payment=(Cast('ach_points', FloatField()))*.5)

    context = {'shipping_staff_points': shipping_staff_points}
    return render(request, 'crewdatabd/seafarer_stats.html', context)
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'vessel', 'viewer'])
def shipStaffs(request, pk):
    ship = get_object_or_404(Vessel, id=pk)
    seafarers = ShippingStaff.objects.filter(vessel=pk)
    context = {'ship': ship, 'seafarers': seafarers}
    return render(request, 'crewdatabd/ship_staffs.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'vessel'])
def createShippingStaff(request):

    form = ShippingStaffForm()
    heading = 'Create Shipping Staff'

    if request.method == 'POST':
        form = ShippingStaffForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.added_by = request.user
            fs.save()

            form.save_m2m()
            seafarer = form.cleaned_data.get('full_name')
            messages.success(request, 'Shipping Staff  was created for ' + seafarer + '.')
            return redirect('seafarers')

    context = {'form': form, 'heading': heading}
    return render(request, 'crewdatabd/seafarer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'vessel'])
def readShippingStaff(request, pk):
    seafarer = get_object_or_404(ShippingStaff, id=pk)
    heading = 'Shipping Staff'

    context = {'seafarer': seafarer, 'heading': heading}
    return render(request, 'crewdatabd/seafarer_details.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'vessel'])
def updateShippingStaff(request, pk):
    seafarer = get_object_or_404(ShippingStaff, id=pk)
    form = ShippingStaffForm(instance=seafarer)
    heading = 'Update Shipping Staff'

    if request.method == 'POST':
        form = ShippingStaffForm(request.POST, instance=seafarer)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.updated_by = request.user
            fs.updated_date = timezone.now()
            fs.save()

            form.save_m2m()
            seafarer = form.cleaned_data.get('full_name')
            messages.success(request, 'Shipping Staff  was updated for ' + seafarer + '.')
            return redirect('seafarers')

    context = {'form': form, 'heading': heading}
    return render(request, 'crewdatabd/seafarer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'vessel'])
def deleteShippingStaff(request, pk):
    seafarer = get_object_or_404(ShippingStaff, id=pk)
    heading = 'Delete Shipping Staff'
    item = seafarer.full_name

    if request.method == 'POST':
        seafarer.delete()
        messages.success(request, 'Deleted Shipping Staff was ' + item + '.')
        return redirect('seafarers')

    context = {'seafarer': seafarer, 'heading': heading}
    return render(request, 'crewdatabd/seafarer_delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'jahaji', 'viewer'])
def ghats(request):
    ghats = Ghat.objects.all()
    context = {'ghats': ghats}
    return render(request, 'crewdatabd/ghats.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'jahaji'])
def createGhat(request):

    form = GhatForm()
    heading = 'Create Ghat'

    if request.method == 'POST':
        form = GhatForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.added_by = request.user
            fs.save()

            form.save_m2m()
            ghat = form.cleaned_data.get('ghat_name')
            messages.success(request, 'Ghat  was created for ' + ghat + '.')
            return redirect('ghats')

    context = {'form': form, 'heading': heading}
    return render(request, 'crewdatabd/ghat.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'jahaji'])
def updateGhat(request, pk):
    ghat = get_object_or_404(Ghat, id=pk)
    form = GhatForm(instance=ghat)
    heading = 'Update Ghat'

    if request.method == 'POST':
        form = GhatForm(request.POST, instance=ghat)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.updated_by = request.user
            fs.updated_date = timezone.now()
            fs.save()

            form.save_m2m()
            ghat = form.cleaned_data.get('ghat_name')
            messages.success(request, 'Ghat  was updated for ' + ghat + '.')
            return redirect('ghats')

    context = {'form': form, 'heading': heading}
    return render(request, 'crewdatabd/ghat.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'jahaji'])
def deleteGhat(request, pk):
    ghat = get_object_or_404(Ghat, id=pk)
    heading = 'Delete Ghat'
    item = ghat.ghat_name

    if request.method == 'POST':
        ghat.delete()
        messages.success(request, 'Deleted Ghat was ' + item + '.')
        return redirect('ghats')

    context = {'ghat': ghat, 'heading': heading}
    return render(request, 'crewdatabd/ghat_delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'ghat', 'viewer'])
def ghat_labors(request):
    ghat_labors = GhatLabor.objects.all()
    context = {'ghat_labors': ghat_labors}
    return render(request, 'crewdatabd/ghat_labors.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'ghat', 'viewer'])
def ghatLabors(request, pk):
    ghat = get_object_or_404(Ghat, id=pk)
    ghat_labors = GhatLabor.objects.filter(ghat_name=pk)
    context = {'ghat': ghat, 'ghat_labors': ghat_labors}
    return render(request, 'crewdatabd/ghat_single_labors.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'ghat'])
def labor_stats(request):
    start_date = datetime.date.today()
    end_date = datetime.date.today() + datetime.timedelta(days=1)
    if request.method == 'POST':
        start_date = request.POST.get('start_date', False)
        end_date = request.POST.get('end_date', False)

        labor_points = GhatLabor.objects.filter(added_date__gte=start_date, added_date__lte=end_date).values('added_by__username').annotate(full_points=Count('labor_name')*20,
        ach_points=(Count('labor_name')*1+Count('labor_position')*1+Count('labor_contact')*1+Count('labor_address')*2+Count('address_district')*1
        +Count('address_thana')*1+Count('family_members')*1+Count('avg_family_income_m')*1+Count('avg_daily_income')*2+Count('avg_working_day_m')*1
        +Count('education_level')*2+Count('birth_date')*1+Count('nid_number')*2+Count('mobile_type')*1+Count('mobile_money_account')*1+Count('bank_account')*1
        +Count('blood_group')*1)).annotate(achv_payment=(Cast('ach_points', FloatField()))*.5)

        context = {'labor_points': labor_points}
        return render(request, 'crewdatabd/labor_stats.html', context)

    labor_points = GhatLabor.objects.filter(added_date__gte=start_date, added_date__lte=end_date).values('added_by__username').annotate(full_points=Count('labor_name')*20,
    ach_points=(Count('labor_name')*1+Count('labor_position')*1+Count('labor_contact')*1+Count('labor_address')*2+Count('address_district')*1
    +Count('address_thana')*1+Count('family_members')*1+Count('avg_family_income_m')*1+Count('avg_daily_income')*2+Count('avg_working_day_m')*1
    +Count('education_level')*2+Count('birth_date')*1+Count('nid_number')*2+Count('mobile_type')*1+Count('mobile_money_account')*1+Count('bank_account')*1
    +Count('blood_group')*1)).annotate(achv_payment=(Cast('ach_points', FloatField()))*.5)

    context = {'labor_points': labor_points}
    return render(request, 'crewdatabd/labor_stats.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'ghat'])
def createGhatLabor(request):

    form = GhatLaborForm()
    heading = 'Create Ghat Labor'

    if request.method == 'POST':
        form = GhatLaborForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.added_by = request.user
            fs.save()

            form.save_m2m()
            labor = form.cleaned_data.get('labor_name')
            messages.success(request, 'Ghat  was created for ' + labor + '.')
            return redirect('ghat_labors')

    context = {'form': form, 'heading': heading}
    return render(request, 'crewdatabd/labor.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'ghat'])
def readGhatLabor(request, pk):
    labor = get_object_or_404(GhatLabor, id=pk)
    heading = 'Labor Details'

    context = {'labor': labor, 'heading': heading}
    return render(request, 'crewdatabd/labor_details.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'ghat'])
def updateGhatLabor(request, pk):
    ghat_labor = get_object_or_404(GhatLabor, id=pk)
    form = GhatLaborForm(instance=ghat_labor)
    heading = 'Update Ghat Labor'

    if request.method == 'POST':
        form = GhatLaborForm(request.POST, instance=ghat_labor)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.updated_by = request.user
            fs.updated_date = timezone.now()
            fs.save()

            form.save_m2m()
            ghat_labor = form.cleaned_data.get('labor_name')
            messages.success(request, 'Ghat Labor was updated for ' + ghat_labor + '.')
            return redirect('ghat_labors')

    context = {'form': form, 'heading': heading}
    return render(request, 'crewdatabd/form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'ghat'])
def deleteGhatLabor(request, pk):
    ghat_labor = get_object_or_404(GhatLabor, id=pk)
    heading = 'Delete Ghat Labor'
    item = ghat_labor.labor_name

    if request.method == 'POST':
        ghat_labor.delete()
        messages.success(request, 'Deleted Ghat Labor was ' + item + '.')
        return redirect('ghat_labors')

    context = {'ghat_labor': ghat_labor, 'heading': heading}
    return render(request, 'crewdatabd/ghat_labor_delete.html', context)

