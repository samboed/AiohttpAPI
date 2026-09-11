from src.app.serializer.validate import generate_validator
from src.app.views.patterns import BaseItemView, BaseGroupView
from src.db.models.ads import Advertisement


class AdvertisementItemView(BaseItemView):
    model = Advertisement
    validator = generate_validator(Advertisement)
    owner_attr_name = 'owner_id'


class AdvertisementGroupView(BaseGroupView):
    model = Advertisement
    validator = generate_validator(Advertisement)
    owner_attr_name = 'owner_id'
