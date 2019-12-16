import datetime as dt

from rest_framework import status
from rest_framework.test import APITestCase

from ticket_office.models import Room, Movie, Showtime, Ticket


class RoomTestCase(APITestCase):

    def test_create_room(self):
        initial_room_count = Room.objects.count()
        room_attrs = {'name': 'New Room', 'capacity': 150}
        response = self.client.post('/rooms/', room_attrs, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), initial_room_count + 1)

        for attr, expected_value in room_attrs.items():
            self.assertEqual(response.data[attr], expected_value)

    def test_delete_room(self):
        room_attrs = {'name': 'Room test', 'capacity': 50}
        self.client.post('/rooms/', room_attrs, format='json')
        initial_room_count = Room.objects.count()
        room_id = Room.objects.first().id
        self.client.delete('/rooms/{}/'.format(room_id))
        self.assertEqual(Room.objects.count(), initial_room_count - 1)


class MovieTestCase(APITestCase):

    def test_create_movie(self):
        initial_movie_count = Movie.objects.count()
        movie_attrs = {'title': 'New Movie', 'duration': 90}
        response = self.client.post('/movies/', movie_attrs, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), initial_movie_count + 1)

        for attr, expected_value in movie_attrs.items():
            self.assertEqual(response.data[attr], expected_value)

    def test_delete_movie(self):
        movie = Movie.objects.create(title='Movie test', duration=30)
        initial_movie_count = Movie.objects.count()
        self.client.delete('/movies/{}/'.format(movie.id))
        self.assertEqual(Movie.objects.count(), initial_movie_count - 1)


class ShowtimeTestCase(APITestCase):

    def test_create_showtime(self):
        initial_showtime_count = Showtime.objects.count()
        room = Room.objects.create(name='room test', capacity=30)
        movie = Movie.objects.create(title='title test', duration=90)
        start = dt.datetime.strptime('2020-06-29 08:15', '%Y-%m-%d %H:%M')
        end = start + dt.timedelta(minutes=movie.duration)

        showtime_attrs = {'room': room.id,
                          'movie': movie.id,
                          'start_date': str(start),
                          'available': room.capacity,
                          'end_date': str(end)}
        response = self.client.post('/showtimes/', showtime_attrs, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Showtime.objects.count(), initial_showtime_count + 1)
        self.assertEqual(response.data['room'], room.name)
        self.assertEqual(response.data['movie'], movie.title)
        self.assertEqual(dt.datetime.strptime(response.data['start_date'], '%Y-%m-%dT%H:%M:%S'),
                         dt.datetime.strptime(showtime_attrs['start_date'], '%Y-%m-%d %H:%M:%S'))
        # testing custom fields
        self.assertEqual(Showtime.objects.get(id=response.data['id']).available, room.capacity)
        self.assertEqual(Showtime.objects.get(id=response.data['id']).end_date,
                         dt.datetime.strptime(showtime_attrs['end_date'], '%Y-%m-%d %H:%M:%S'))

    def test_delete_showtime(self):
        room = Room.objects.create(name='room test', capacity=30)
        movie = Movie.objects.create(title='title test', duration=90)
        start = dt.datetime.strptime('2020-06-29 08:15', '%Y-%m-%d %H:%M')
        end = start + dt.timedelta(minutes=movie.duration)
        showtime = Showtime.objects.create(room=room, movie=movie, start_date=start, end_date=end,
                                           available=room.capacity)
        initial_showtime_count = Showtime.objects.count()
        self.client.delete('/showtimes/{}/'.format(showtime.id))
        self.assertEqual(Showtime.objects.count(), initial_showtime_count - 1)


class TicketCreateTestCase(APITestCase):

    def test_create_ticket(self):
        initial_ticket_count = Ticket.objects.count()
        room = Room.objects.create(name='room test', capacity=30)
        movie = Movie.objects.create(title='title test', duration=90)
        start = dt.datetime.strptime('2018-06-29 08:15', '%Y-%m-%d %H:%M')
        end = start + dt.timedelta(minutes=movie.duration)
        showtime = Showtime.objects.create(room=room, movie=movie, start_date=start, available=room.capacity,
                                           end_date=end)
        ticket_attrs = {'showtime': showtime.id, 'num_seats': 1}
        response = self.client.post('/tickets/', ticket_attrs, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), initial_ticket_count + 1)

        for attr, expected_value in ticket_attrs.items():
            self.assertEqual(response.data[attr], expected_value)

        self.assertEqual(Showtime.objects.get(id=showtime).available, showtime.availability-1)
