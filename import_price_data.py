import decimal
import traceback

from django.utils.dateparse import parse_datetime

from api.models import HomePrice

from tablib import Dataset


def import_data():
    with open('price_data.csv', 'r') as fp:
        csv_data = Dataset().load(fp)

        for _csv_data in csv_data.dict:
            try:

                HomePrice.objects.create(
                    date_time=parse_datetime(_csv_data['date']),
                    price=round(decimal.Decimal(_csv_data['price']), 2) if _csv_data['price'] else 0.00,
                    bedrooms=_csv_data['bedrooms'],
                    bathrooms=_csv_data['bathrooms'],
                    sqft_living=_csv_data['sqft_living'],
                    sqft_lot=_csv_data['sqft_lot'],
                    floors=_csv_data['floors'],
                    waterfront=_csv_data['waterfront'],
                    view=_csv_data['view'],
                    condition=_csv_data['condition'],
                    sqft_above=_csv_data['sqft_above'],
                    sqft_basement=_csv_data['sqft_basement'],
                    yr_built=_csv_data['yr_built'],
                    yr_renovated=_csv_data['yr_renovated'],
                    street=_csv_data['street'],
                    city=_csv_data['city'],
                    statezip=_csv_data['statezip'],
                    country=_csv_data['country']
                )

            except Exception as e:
                print(_csv_data)
                print(str(e))
                print(traceback.format_exc())
                HomePrice.objects.all().delete()
                return 'Error ----'

    return 'Data Imported Successfully'
