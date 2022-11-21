import datetime
from django.db import models
from django.utils.timezone import now

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

# Car Make model


class CarMake(models.Model):
    make_name = models.CharField(null=False, max_length=48)
    make_description = models.CharField(null=True, max_length=480)

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

# Car Model model


class CarModel(models.Model):
    model_make = models.ForeignKey(
        CarMake, null=True, on_delete=models.CASCADE)
    model_name = models.CharField(null=False, max_length=50)
    dealer_id = models.IntegerField(null=True)

    SEDAN = "Sedan"
    SUV = "SUV"
    COUPE = "Coupe"
    WAGON = "Wagon"
    PICKUP = "Pickup"
    MINIVAN = "Minivan"

    CAR_CHOICES = [(SEDAN, "Sedan"), (SUV, "SUV"), (COUPE, "Coupe"), (MINIVAN, "Minivan"),
                   (WAGON, "Wagon"), (PICKUP, "Pick-up truck")]
    model_type = models.CharField(
        null=False, max_length=15, choices=CAR_CHOICES, default=SEDAN)

    YEAR_CHOICES = []
    for r in range(2005, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r, r))

    model_year = models.IntegerField(
        ('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    def __str__(self):
        return self.model_name + ", " + str(self.model_year) + ", " + self.model_type


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
