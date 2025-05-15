from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # Authentication endpoints
    path(route='login', view=views.login_user, name='login'),
    # path(route='register', view=views.registration, name='register'),
    # path(route='logout', view=views.logout_request, name='logout'),

    # Car endpoints
    path(route='get_cars', view=views.get_cars, name='getcars'),

    # Dealership endpoints
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    
    # Dealer-specific endpoints
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),
    path(route='reviews/dealer<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_reviews'),
    path(route='add_review/<int:dealer_id>', view=views.add_review, name='add_review'),

    # Other endpoints
    # path(route='', view=views.get_dealerships, name='index'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
