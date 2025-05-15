from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate  # Uncomment if you have this function
from .restapis import get_request, analyze_review_sentiments  # Import required functions
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

def get_dealerships(request, state="All"):
    """Get dealerships - all by default or filtered by state"""
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200, "dealers":dealerships})

def get_dealer_details(request, dealer_id):
    """Get details for a specific dealer"""
    if dealer_id:
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200, "dealer":dealership})
    else:
        return JsonResponse({"status":400, "message":"Bad Request"})

def get_dealer_reviews(request, dealer_id):
    """Get reviews for a specific dealer with sentiment analysis"""
    if dealer_id:
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200, "reviews":reviews})
    else:
        return JsonResponse({"status":400, "message":"Bad Request"})

@csrf_exempt  # Add this decorator to allow POST requests
def add_review(request):
    """Handle POST requests to add new reviews"""
    if request.user.is_authenticated:  # Better authentication check
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            
            # Call post_review function with the data
            response = post_review(data)
            print("Review post response:", response)  # Debug logging
            
            return JsonResponse({
                "status": 200,
                "message": "Review posted successfully",
                "response": response
            })
        except json.JSONDecodeError:
            return JsonResponse({
                "status": 400,
                "message": "Invalid JSON data"
            }, status=400)
        except Exception as e:
            print("Error posting review:", str(e))
            return JsonResponse({
                "status": 400,
                "message": "Error posting review"
            }, status=400)
    else:
        return JsonResponse({
            "status": 403,
            "message": "Unauthorized - Please log in"
        }, status=403)
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
