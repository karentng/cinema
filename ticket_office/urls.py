from django.urls import include, path
from rest_framework import routers
from ticket_office import views

router = routers.DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'movies', views.MovieViewSet)
router.register(r'showtimes', views.ShowtimeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tickets', views.TicketListView.as_view()),
    path('tickets/sale', views.TicketSaleView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]