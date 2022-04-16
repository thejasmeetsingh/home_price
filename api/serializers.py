import decimal

from rest_framework import serializers

from api.models import HomePrice


class HomePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePrice
        fields = (
            'date_time',
            'price',
            'bedrooms',
            'bathrooms',
            'sqft_living',
            'sqft_lot',
            'floors',
            'waterfront',
            'view',
            'condition',
            'sqft_above',
            'sqft_basement',
            'yr_built',
            'yr_renovated',
            'street',
            'city',
            'statezip',
            'country',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('predict_price'):
            data['price'] = (((data['bedrooms'] * data['bathrooms'] * (
                (data['sqft_living'] / data['sqft_lot']) if data['sqft_lot'] else 0.0) * data[
                                   'floors']) + data['waterfront'] + data['view']) * data['condition'] * (
                                     data['sqft_above'] + data['sqft_basement']) - 10 * (
                                     2022 - max(data['yr_built'], data['yr_renovated']))) * 100
            data['price'] = str(round(decimal.Decimal(data['price']), 2))
        return data
