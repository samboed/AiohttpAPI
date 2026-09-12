from src.app.serializer.validate import AdvertisementValidator
from src.app.utils.view.patterns import BaseItemView, BaseGroupView
from src.db.models.ads import Advertisement


class AdvertisementItemView(BaseItemView):
    model = Advertisement
    validator = AdvertisementValidator
    owner_attr_name = 'owner_id'


class AdvertisementGroupView(BaseGroupView):
    model = Advertisement
    validator = AdvertisementValidator
    owner_attr_name = 'owner_id'
