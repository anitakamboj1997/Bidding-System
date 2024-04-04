from django.urls import path
from .views import AddProductForBidding, PlaceBid, ListBidsOnProduct, ApproveBid

urlpatterns = [
    path('add-product/', AddProductForBidding.as_view(), name='add-product'),
    path('place-bid/', PlaceBid.as_view(), name='place-bid'),
    path('list-bids/<int:product_id>/', ListBidsOnProduct.as_view(), name='list-bids'),
    path('approve-bid/<int:bid_id>/', ApproveBid.as_view(), name='approve-bid'),
]