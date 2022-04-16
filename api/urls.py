from django.urls import path

from api import views

urlpatterns = [
    path('token/', views.TokenAPIView.as_view()),
    path('budget-homes/', views.BudgetHomeListView.as_view()),
    path('sqft-homes/', views.SqftHomeListView.as_view()),
    path('age-homes/', views.AgeHomeListView.as_view()),
    path('predict-price/', views.PredictPrice.as_view()),
]
