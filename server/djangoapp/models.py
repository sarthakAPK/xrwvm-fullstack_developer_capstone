from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    founded_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(now().year)],
        null=True,
        blank=True
    )
    headquarters = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('TRUCK', 'Truck'),
        ('VAN', 'Van'),
        ('HATCHBACK', 'Hatchback'),
    ]

    # Required fields
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(help_text="ID referencing a dealer in Cloudant database")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(now().year + 1)  # Current year + 1 for upcoming models
        ]
    )
    
    # Additional useful fields
    engine = models.CharField(max_length=50, blank=True)
    trim_level = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    mileage = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
        