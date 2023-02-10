from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    cars = Car.objects.all()
    return render(request, "index.html", {'cars':cars})

def customer_signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        city = request.POST['city']

        if password1 != password2:
            return redirect("/customer_signup")

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password1,is_customer=True)
        user.save()
        try:
            location = Location.objects.get(city=city.lower())
        except:
            location = None
        if location is not None:
            customer = Customer(user=user, phone=phone, location=location, type="Customer")
        else:
            location = Location(city=city.lower())
            location.save()
            location = Location.objects.get(city=city.lower())
            customer = Customer(user=user, phone=phone, location=location, type="Customer")
        customer.save()
        alert = True
        return render(request, "customer_signup.html", {'alert':alert})
    return render(request, "customer_signup.html")

def customer_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = Customer.objects.get(user=user)
                if user1.type == "Customer":
                    login(request, user)
                    return redirect("/customer_dashboard")
                else:
                    messages.error(request,"User doesn't exist")
                    return redirect("customer_login")

            else:
                messages.error(request,'username or password not correct')
                return redirect('customer_login')
    return render(request, "customer_login.html")

def car_agency_signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        city = request.POST['city']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return redirect('/car_agency_signup')

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password1, is_car_agency=True)
        user.save()
        try:
            location = Location.objects.get(city = city.lower())
        except:
            location = None
        if location is not None:
            car_agency = CarAgency(car_agency=user, phone=phone, location=location, type="Car Dealer")
        else:
            location = Location(city = city.lower())
            location.save()
            location = Location.objects.get(city = city.lower())
            car_agency = CarAgency(car_agency = user, phone=phone, location=location, type="Car Dealer")
        car_agency.save()
        return render(request, "car_agency_login.html")
    return render(request, "car_agency_signup.html")

def car_agency_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = CarAgency.objects.get(car_agency=user)
                if user1.type == "Car Dealer":
                    login(request, user)
                    return redirect("/car_agency_dashboard")
                else:
                    messages.error(request,'username or password not correct')
                    return redirect('car_agency_login')
    return render(request, "car_agency_login.html")

def signout(request):
    logout(request)
    return redirect('/')

def add_car(request):
    if request.method == "POST":
        car_model = request.POST['car_model']
        car_number = request.POST['car_number']
        
        image = request.FILES['image']
        capacity = request.POST['capacity']
        rent = request.POST['rent']
        car_agency = CarAgency.objects.get(car_agency=request.user)
        city = car_agency.location
        try:
            location = Location.objects.get(city=city)
        except:
            location = None
        if location is not None:
            car = Car(model=car_model, number=car_number, car_agency=car_agency, location=location, capacity=capacity, image=image, rent=rent)
        else:
            location = Location(city=city)
            car = Car(model=car_model, number=car_number, car_agency=car_agency, location=location, capacity=capacity, image=image, rent=rent)
        car.save()
        alert = True
        return render(request, "add_car.html", {'alert':alert})
    return render(request, "add_car.html")

def all_cars(request):
    dealer = CarAgency.objects.filter(car_agency=request.user).first()
    cars = Car.objects.filter(car_agency=dealer)
    return render(request, "all_cars.html", {'cars':cars})

def edit_car(request, myid):
    car = Car.objects.filter(id=myid)[0]
    if request.method == "POST":
        car_model = request.POST['car_model']
        car_number = request.POST['car_number']
        capacity = request.POST['capacity']
        rent = request.POST['rent']

        car.model = car_model
        car.number = car_number
        car.capacity = capacity
        car.rent = rent
        car.save()

        try:
            image = request.FILES['image']
            car.image = image
            car.save()
        except:
            pass
        alert = True
        return render(request, "edit_car.html", {'alert':alert})
    return render(request, "edit_car.html", {'car':car})

def delete_car(request, myid):
    if not request.user.is_authenticated:
        return redirect("/car_agency_login")
    car = Car.objects.filter(id=myid)
    car.delete()
    return redirect("/all_cars")

def customer_homepage(request):
    return render(request, "customer_homepage.html")

def search_results(request):
    city = request.POST['city']
    city = city.lower()
    vehicles_list = []
    location = Location.objects.filter(city = city)
    for a in location:
        cars = Car.objects.filter(location=a)
        for car in cars:
            if car.is_available == True:
                vehicle_dictionary = {'model':car.model,'number':car.number, 'id':car.id, 'image':car.image.url, 'city':car.location.city,'capacity':car.capacity}
                vehicles_list.append(vehicle_dictionary)
    request.session['vehicles_list'] = vehicles_list
    request.session['location'] = city
    return render(request, "search_results.html")

def car_rent(request):
    id = request.POST['id']
    car = Car.objects.get(id=id)
    cost_per_day = int(car.rent)
    return render(request, 'car_rent.html', {'car':car, 'cost_per_day':cost_per_day})

def booking_details(request):
    car_id = request.POST['id']
    username = request.user
    user = User.objects.get(username=username)
    days = request.POST['days']
    date = request.POST['date']
    car = Car.objects.get(id=car_id)
    if car.is_available:
        car_agency = car.car_agency
        rent = (int(car.rent))*(int(days))
        car_agency.earnings += rent
        car_agency.save()
        try:
            booking = Booking(car=car, car_agency=car_agency, user=user, rent=rent, days=days, date=date)
            booking.save()
        except:
            booking = Booking.objects.get(car=car, car_agency=car_agency, user=user, rent=rent, days=days, date=date)
        car.is_available = False
        car.save()
        return render(request, "booking_details.html", {'booking':booking})
    return render(request, "booking_details.html")

def booked_history(request):
    view_booked = []
    user = User.objects.get(username=request.user)
    try:
        bookings = Booking.objects.filter(user=user)
    except:
        bookings = None
    if bookings is not None:
        for booking in bookings:
            
                booking_dictionary = {'id':booking.id, 'rent':booking.rent, 'car':booking.car, 'days':booking.days, 'date':booking.date, 'car_agency':booking.car_agency, 'is_complete':booking.is_complete}
                view_booked.append(booking_dictionary)
    return render(request, "booked_history.html", {'view_booked':view_booked})

def delete_booking(request, myid):
    booking = Booking.objects.filter(id=myid)
    booking.delete()
    return redirect("/booked_history")

def view_booked(request):
    username = request.user
    user = User.objects.get(username=username)
    car_agency = CarAgency.objects.get(car_agency=user)
    bookings = Booking.objects.filter(car_agency=car_agency)
    view_booked = []
    for booking in bookings:
        if booking.is_complete == False:
            view_booked.append(booking)
    return render(request, "booked_view.html", {'view_booked':view_booked})

def complete_booking(request):
    booking_id = request.POST['id']
    booking = Booking.objects.get(id=booking_id)
    car = booking.car
    booking.is_complete = True
    booking.save()
    car.is_available = True
    car.save()
    return HttpResponseRedirect('/view_booked/')

def earnings(request):
    username = request.user
    user = User.objects.get(username=username)
    car_agency = CarAgency.objects.get(car_agency=user)
    bookings = Booking.objects.filter(car_agency=car_agency)
    view_booked = []
    for booking in bookings:
        view_booked.append(booking)
    return render(request, "earnings.html", {'amount':car_agency.earnings, 'view_booked':view_booked})