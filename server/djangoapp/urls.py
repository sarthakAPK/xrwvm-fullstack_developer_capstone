from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # path for get_cars
    path(route='get_cars', view=views.get_cars, name='getcars'),
    
    # path for login
    path(route='login', view=views.login_user, name='login'),

    # Uncomment and implement these as needed:
    
    # path for registration
    # path(route='register', view=views.registration, name='register'),
    
    # path for logout
    # path(route='logout', view=views.logout_request, name='logout'),
    
    # path for dealer reviews view
    # path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),
    
    # path for add a review view
    # path(route='add_review/<int:dealer_id>', view=views.add_review, name='add_review'),
    
    # path for get dealerships
    # path(route='', view=views.get_dealerships, name='index'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
