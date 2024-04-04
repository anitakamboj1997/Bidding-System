# Import necessary modules
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Bid, ApprovedBid
from .serializers import ProductSerializer, BidSerializer
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import Http404

class AddProductForBidding(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class PlaceBid(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data.get('product')
            bid_amount = serializer.validated_data.get('bid_amount')
            try:
                product = Product.objects.get(pk=product_id.id)
            except Product.DoesNotExist:
                return Response({"error": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)

            if bid_amount < product.min_bid_price:
                return Response({"error": f"Bid amount is less than the minimum bid price ({product.min_bid_price})."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListBidsOnProduct(generics.ListAPIView):
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        queryset = Bid.objects.filter(product_id=product_id)
        if not queryset.exists():
            raise Http404("No records found")
        return queryset
    
    
class ApproveBid(generics.UpdateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]  

    def put(self, request, *args, **kwargs):
        bid_id = self.kwargs.get('bid_id')
        try:
            bid = Bid.objects.get(pk=bid_id)
        except Bid.DoesNotExist:
            return Response({"error": "Bid does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if ApprovedBid.objects.filter(bid_id=bid_id).exists():
            return Response({"error": "Bid has already been approved."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                ApprovedBid.objects.create(bid=bid, closed=True)
        except IntegrityError:
            return Response({"error": "Failed to approve bid."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Bid approved successfully and bidding process closed."}, status=status.HTTP_200_OK)
