from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register(r'bookings',views.BookingViewSet,basename='bookings')

urlpatterns=[
    path('',include(router.urls)),
    path('events/<slug:slug>/book/',views.BookingViewSet.as_view({'post':'create'}))
]

