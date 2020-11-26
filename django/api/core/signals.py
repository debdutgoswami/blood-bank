from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Address
from .fields import PointField
from .utils import get_coordinates


@receiver(pre_save, sender=Address)
def get_coordinates_from_instance(sender, **kwargs):
    address_obj: Address = kwargs.get("instance")
    address_str = (
        address_obj.address_line_1
        + " "
        + address_obj.address_line_2
        + " "
        + address_obj.city
        + " "
        + address_obj.state
        + " "
        + address_obj.country
    )
    res = get_coordinates(address_str)
    address_obj.coordinate = PointField().to_internal_value(
        {
            "latitude": res.get('lat'),
            "longitude": res.get('lon'),
        }
    )
