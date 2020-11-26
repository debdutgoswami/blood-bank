from django.db import models
from django.contrib.gis.db import models as geo_models
from django.core.validators import RegexValidator

from .choices import Country, BloodGroup, Gender


# Create your models here.
class Address(models.Model):
    """
    Model to store address of donor
    """

    class COUNTRY(Country, models.TextChoices):
        pass

    address_line_1 = models.CharField("Line 1", max_length=40, blank=False)
    address_line_2 = models.CharField("Line 2", max_length=40, blank=True)
    city = models.CharField("City", max_length=40, blank=True)
    zipcode = models.CharField("Zipcode", max_length=6, blank=False)
    state = models.CharField("State", max_length=40, blank=False)
    country = models.CharField(
        "Country",
        max_length=2,
        choices=COUNTRY.choices,
        default=COUNTRY.India,
        blank=False,
    )
    ## coordinate
    coordinate = geo_models.PointField("Co-ordinates")


class Donor(models.Model):
    """
    Model to store details of donor
    """
    address = models.OneToOneField(Address, models.CASCADE)

    class SEX(Gender, models.TextChoices):
        pass

    class BLOODGROUP(BloodGroup, models.TextChoices):
        pass

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )

    name = models.CharField("Name", max_length=40, blank=False)
    email = models.EmailField("Email", max_length=40, blank=False)
    sex = models.CharField(max_length=1, choices=SEX.choices, blank=True)
    phone = models.CharField(
        "Phone Number", validators=[phone_regex], max_length=16, blank=True
    )
    bloodgroup = models.CharField(
        "Blood Group", choices=BLOODGROUP.choices, max_length=3, blank=False
    )
    age = models.PositiveSmallIntegerField("Age", blank=False)
    weight = models.PositiveSmallIntegerField("Weight", blank=True)


class RequestTicket(models.Model):
    address = models.OneToOneField(Address, models.CASCADE)

    SEX = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Others"),
    ]
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    name = models.CharField("Name", max_length=40, blank=False)
    sex = models.CharField(max_length=1, choices=SEX, blank=True)
    phone = models.CharField(
        "Phone Number", validators=[phone_regex], max_length=16, blank=True
    )
    bloodgroup = models.CharField("Blood Group", max_length=3, blank=False)
    age = models.PositiveSmallIntegerField("Age", blank=True)
    created_on = models.DateField("Created On", auto_now=True, blank=False)

    class Meta:
        ordering = ["created_on"]
