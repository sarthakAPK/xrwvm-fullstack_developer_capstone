from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate  # Uncomment if you have this function
# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

# Get an instance of a logger
logger = logging.getLogger(__name__)

def get_cars(request):
    count = CarMake.objects.count()
    print(count)
    if count == 0:
        from .populate import initiate
        initiate()  # This will auto-populate when first accessed
    
    # Uncomment if you need to populate initial data
    # if count == 0:
    #     initiate()
    
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name, 
            "CarMake": car_model.car_make.name,
            "Year": car_model.year,
            "Type": car_model.type,
            "DealerId": car_model.dealer_id
        })
    return JsonResponse({"CarModels": cars})

@csrf_exempt
def login_user(request):
    """Handles user login requests"""
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Uncomment and implement these as needed:

# def logout_request(request):
#     logout(request)
#     return redirect('djangoapp:index')

# @csrf_exempt
# def registration(request):
#     data = json.loads(request.body)
#     username = data['userName']
#     password = data['password']
#     first_name = data['firstName']
#     last_name = data['lastName']
#     email = data['email']
#     username_exist = False
#     try:
#         User.objects.get(username=username)
#         username_exist = True
#     except:
#         logger.debug("{} is new user".format(username))
#     if not username_exist:
#         user = User.objects.create_user(
#             username=username, first_name=first_name, last_name=last_name,
#             password=password, email=email
#         )
#         login(request, user)
#         data = {"userName": username, "status": "Authenticated"}
#         return JsonResponse(data)
#     else:
#         data = {"userName": username, "error": "Already Registered"}
#         return JsonResponse(data)

# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)

# def get_dealer_reviews(request, dealer_id):
#     if request.method == "GET":
#         context = {
#             "reviews": [],
#             "dealer_id": dealer_id
#         }
#         return render(request, 'djangoapp/dealer_details.html', context)

# def get_dealer_details(request, dealer_id):
#     if request.method == "GET":
#         context = {
#             "dealer": {},
#             "dealer_id": dealer_id
#         }
#         return render(request, 'djangoapp/dealer_details.html', context)

# def add_review(request):
#     if request.method == "POST":
#         if request.user.is_authenticated:
#             form = ReviewForm(request.POST)
#             if form.is_valid():
#                 review = form.save(commit=False)
#                 review.car_model = CarModel.objects.get(pk=request.POST['car'])
#                 review.dealership = dealer_id
#                 review.user = request.user
#                 review.save()
#                 return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
#     return redirect("djangoapp:index")
