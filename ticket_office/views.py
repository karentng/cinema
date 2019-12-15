from rest_framework import viewsets, generics, views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ticket_office.serializers import *


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        room_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            # Clearing cache to frees up space
            from django.core.cache import cache
            cache.delete('room_data_{}'.format(room_id))
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        if response.status_code == 200:
            from django.core.cache import cache
            room = response.data
            cache.set('room_data_{}'.format(room['id']), {
                'name': room['name'],
                'capacity': room['capacity']
            })
        return response


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        """
        Deletes a movie by id and frees up space in cache

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        movie_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('movie_data_{}'.format(movie_id))
        return response

    def update(self, request, *args, **kwargs):
        """
        Updates the information loaded from the movie and set that value in cache

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            movie = response.data
            cache.set('movie_data_{}'.format(movie['id']), {
                'name': movie['title'],
                'capacity': movie['duration']
            })
        return response


class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.all().order_by('start_date')
    serializer_class = ShowtimeSerializer


class ShowtimeUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        """
        Delete a showtime by id. Frees up cache space

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        showtime_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('showtime_data_{}'.format(showtime_id))
        return response

    def update(self, request, *args, **kwargs):
        """
        Update a showtime loaded by id and set up the information in cache

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            showtime = response.data
            cache.set('showtime_data_{}'.format(showtime['id']), {
                'room': showtime['room'],
                'movie': showtime['movie'],
                'start_date': showtime['start_date']
            })
        return response


class TicketView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        """
        Method to sell a ticket. This will discount the number of seats sold from the availability in the showtime

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        num_tickets = int(request.data.get('num_seats'))
        showtime = Showtime.objects.get(id=request.data.get('showtime'))
        available = showtime.available

        if available - num_tickets >= 0:
            showtime.available = available - num_tickets
            showtime.save()
        else:
            raise ValidationError({'num_seats': 'Not enough Availability'})

        return super().create(request, *args, **kwargs)


class RoomsPlayingView(views.APIView):
    """
    List Movie rooms and their showtimes
    """
    def get(self, request):
        """
        Build the object to get the rooms and showtimes

        :param request:
        :return:
        """
        rooms = Room.objects.all()
        start = request.query_params.get('start', dt.datetime.now())
        end = request.query_params.get('end')
        results = []
        for room in rooms:
            qstart = Showtime.objects.filter(room=room.id, start_date__gte=start)
            query = Showtime.objects.filter(room=room.id, start_date__gte=start, start_date__lte=end) if end else qstart
            results.append({'name': room.name,
                            'capacity': room.capacity,
                            'showtimes': query})

        serializer = RoomsPlayingSerializer({'rooms': results})
        return Response(serializer.data)


class MoviesPlayingView(views.APIView):
    """
    List Movies and their showtimes
    """
    def get(self, request):
        """
        Build the object to get the rooms and showtimes

        :param request:
        :return:
        """
        movies = Movie.objects.all()
        start = request.query_params.get('start', dt.datetime.now())
        end = request.query_params.get('end')
        results = []
        for movie in movies:
            qstart = Showtime.objects.filter(movie=movie.id, start_date__gte=start)
            query = Showtime.objects.filter(movie=movie.id, start_date__gte=start, start_date__lte=end) if end else qstart
            results.append({'title': movie.title,
                            'duration': movie.duration,
                            'showtimes': query})

        serializer = MoviesPlayingSerializer({'movies': results})
        return Response(serializer.data)
