from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("customer_signup/", views.customer_signup, name="customer_signup"),
    path("customer_login/", views.customer_login, name="customer_login"),
    path("car_agency_signup/", views.car_agency_signup, name="car_agency_signup"),
    path("car_agency_login/", views.car_agency_login, name="car_agency_login"),
    path("add_car/", views.add_car, name="add_car"),
    path("car_agency_dashboard/", views.all_cars, name="all_cars"),
    path("all_cars/", views.all_cars, name="all_cars"),
    path("edit_car/<int:myid>/", views.edit_car, name="edit_car"),
    path("delete_car/<int:myid>/", views.delete_car, name="delete_car"),
    path("customer_dashboard/", views.booked_history, name="customer_homepage"),
    path("search_results/", views.search_results, name="search_results"),
    path("car_rent/", views.car_rent, name="car_rent"),
    path("booking_details/", views.booking_details, name="booking_details"),
    path("booked_history/", views.booked_history, name="booked_history"),
    path("delete_booking/<int:myid>/", views.delete_booking, name="delete_booking"),
    path("view_booked/", views.view_booked, name="view_booked"),
    path("complete_booking/", views.complete_booking, name="complete_booking"),
    path("earnings/", views.earnings, name="earnings"),
    path("signout/", views.signout, name="signout")
]