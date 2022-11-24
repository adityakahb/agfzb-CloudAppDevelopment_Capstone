from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake, CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page


def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request


def login_request(request):
    context = {}
    defaultUrl = 'djangoapp/index.html'
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['userpassword']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, defaultUrl, context)
    else:
        return render(request, defaultUrl, context)

# Create a `logout_request` view to handle sign out request


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request


def registration(request):
    return render(request, 'djangoapp/registration.html', {})


def registration_request(request):
    username = request.POST['username']
    password = request.POST['userpassword']
    firstname = request.POST['userfirstname']
    lastname = request.POST['userlastname']
    isUserAvailable = False

    try:
        User.objects.get(username=username)
        isUserAvailable = True
    except:
        isUserAvailable = False

    if isUserAvailable:
        return render(request, 'djangoapp/registration.html', {})
    else:
        user = User.objects.create_user(
            username=username, first_name=firstname, last_name=lastname, password=password)
        login(request, user)
        return redirect("/djangoapp/")


# Update the `get_dealerships` view to render the index page with a list of dealerships

def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/8ce6fac2-d8dd-421f-b11e-f066c1336a48/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        return render(request, 'djangoapp/index.html', {"dealerships": dealerships})


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealerId):
    context = {}
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/8ce6fac2-d8dd-421f-b11e-f066c1336a48/dealership-package/get-dealership"
        urlReviews = "https://eu-gb.functions.appdomain.cloud/api/v1/web/8ce6fac2-d8dd-421f-b11e-f066c1336a48/dealership-package/get-review"
        context["dealer_info"] = get_dealer_by_id(url, dealerId)
        context["dealer_reviews"] = get_dealer_reviews_from_cf(
            urlReviews, dealerId)
        print(context)

        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealerId):
    # User must be logged in before posting a review
    if request.user.is_authenticated:
        # GET request renders the page with the form for filling out a review
        if request.method == "GET":
            url = f"https://5b93346d.us-south.apigw.appdomain.cloud/dealerships/dealer-get?dealerId={dealerId}"
            # Get dealer details from the API
            context = {
                "cars": CarModel.objects.all(),
                "dealer": get_dealer_by_id(url, dealerId=dealerId),
            }
            return render(request, 'djangoapp/add_review.html', context)
    else:
        # If user isn't logged in, redirect to login page
        print("User must be authenticated before posting a review. Please log in.")
        return redirect("/djangoapp/login")
