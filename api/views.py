import decimal

from django.db import transaction
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from api.models import User, HomePrice
from api.serializers import HomePriceSerializer


class TokenAPIView(APIView):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request):
        user = User.objects.filter(email__iexact=request.data['email']).first()
        if not user:
            user = User.objects.create(email=request.data['email'])

        token, _ = Token.objects.get_or_create(user_id=user.id)
        return Response({
            'token': token.key
        })


class HomePriceBaseView(GenericAPIView, ListModelMixin):
    queryset = HomePrice.objects.all()
    serializer_class = HomePriceSerializer


class BudgetHomeListView(HomePriceBaseView):
    def get_queryset(self):
        max_price = round(decimal.Decimal(self.request.query_params['maxPrice']), 2)
        min_price = round(decimal.Decimal(self.request.query_params['minPrice']), 2)
        return super().get_queryset().filter(price__lte=max_price, price__gte=min_price)

    def get(self, request, *args, **kwargs):
        if 'maxPrice' not in request.query_params:
            return Response({'Error': 'maxPrice field is required'})

        if 'maxPrice' in request.query_params and request.query_params['maxPrice'] == '':
            return Response({'Error': 'maxPrice field must not be blank'})

        if 'minPrice' not in request.query_params:
            return Response({'Error': 'minPrice field is required'})

        if 'minPrice' in request.query_params and request.query_params['minPrice'] == '':
            return Response({'Error': 'minPrice field must not be blank'})

        return self.list(request, *args, **kwargs)


class SqftHomeListView(HomePriceBaseView):
    def get_queryset(self):
        min_sqft = int(self.request.query_params['minSqft'])
        return super().get_queryset().filter(sqft_living__gt=min_sqft)

    def get(self, request, *args, **kwargs):
        if 'minSqft' not in request.query_params:
            return Response({'Error': 'minSqft field is required'})

        if 'minSqft' in request.query_params and request.query_params['minSqft'] == '':
            return Response({'Error': 'minSqft field must not be blank'})

        return self.list(request, *args, **kwargs)


class AgeHomeListView(HomePriceBaseView):
    def get_queryset(self):
        year = int(self.request.query_params['year'])
        return super().get_queryset().filter(Q(yr_built__gt=year) | Q(yr_renovated__gt=year))

    def get(self, request, *args, **kwargs):
        if not request.query_params.get('year'):
            return Response({'Error': 'year field is required'})

        if 'year' in request.query_params and request.query_params['year'] == '':
            return Response({'Error': 'year field must not be blank'})

        return self.list(request, *args, **kwargs)


class PredictPrice(HomePriceBaseView):
    def get_serializer_context(self):
        data = super().get_serializer_context()
        data.update({'predict_price': True})
        return data

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
