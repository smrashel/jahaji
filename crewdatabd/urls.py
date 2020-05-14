from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('associations/', views.associations, name="associations"),
    path('association_companies/<str:pk>/', views.associationCompanies, name="association_companies"),
    path('create_association/', views.createAssociation, name="create_association"),
    path('update_association/<str:pk>/', views.updateAssociation, name="update_association"),
    path('delete_association/<str:pk>/', views.deleteAssociation, name="delete_association"),

    path('load_thanas/', views.load_thanas, name='load_thanas'),
    path('load_ghat_thanas/', views.load_ghat_thanas, name='load_ghat_thanas'),
    path('load_ghats/', views.load_ghats, name='load_ghats'),
    path('load_vessels/', views.load_vessels, name='load_vessels'),

    path('companies/', views.companies, name="companies"),
    path('create_company/', views.createCompany, name="create_company"),
    path('update_company/<str:pk>/', views.updateCompany, name="update_company"),
    path('delete_company/<str:pk>/', views.deleteCompany, name="delete_company"),

    path('ships/', views.ship, name="ships"),
    path('company_ships/<str:pk>/', views.companyShips, name="company_ships"),
    path('create_ship/', views.createShip, name="create_ship"),
    path('update_ship/<str:pk>/', views.updateShip, name="update_ship"),
    path('delete_ship/<str:pk>/', views.deleteShip, name="delete_ship"),


    path('seafarers/', views.seafarers, name="seafarers"),
    path('seafarer_stats/', views.seafarer_stats, name="seafarer_stats"),
    path('ship_seafarers/<str:pk>/', views.shipStaffs, name="ship_staffs"),
    path('create_seafarer/', views.createShippingStaff, name="create_seafarer"),
    path('read_seafarer/<str:pk>/', views.readShippingStaff, name="read_seafarer"),
    path('update_seafarer/<str:pk>/', views.updateShippingStaff, name="update_seafarer"),
    path('delete_seafarer/<str:pk>/', views.deleteShippingStaff, name="delete_seafarer"),

    path('ghats/', views.ghats, name="ghats"),
    path('ghat_labor/<str:pk>/', views.ghatLabors, name="ghat_labor"),
    path('create_ghat/', views.createGhat, name="create_ghat"),
    path('update_ghat/<str:pk>/', views.updateGhat, name="update_ghat"),
    path('delete_ghat/<str:pk>/', views.deleteGhat, name="delete_ghat"),

    path('ghat_labors/', views.ghat_labors, name="ghat_labors"),
    path('create_labor/', views.createGhatLabor, name="create_labor"),
    path('read_labor/<str:pk>/', views.readGhatLabor, name="read_labor"),
    path('update_labor/<str:pk>/', views.updateGhatLabor, name="update_labor"),
    path('delete_labor/<str:pk>/', views.deleteGhatLabor, name="delete_labor"),
]
