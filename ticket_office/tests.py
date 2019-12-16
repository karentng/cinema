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

    def test_list_room(self):
        Room.objects.create(name='Room test', capacity=30)
        room_count = Room.objects.count()
        response = self.client.get('/rooms/')
        self.assertEqual(len(response.data), room_count)

    def test_update_room(self):
        room = Room.objects.create(name='test room', capacity=30)
        response = self.client.patch(
            '/rooms/{}/'.format(room.id),
            {
                'name': 'updated test room',
                'capacity': 30
            },
            format='json',
        )
        updated = Room.objects.get(id=room.id)
        self.assertEqual(updated.name, "updated test room")


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

    def test_list_movie(self):
        Movie.objects.create(title='Movie test', duration=30)
        movie_count = Movie.objects.count()
        response = self.client.get('/movies/')
        self.assertEqual(len(response.data), movie_count)

    def test_update_movie(self):
        movie = Movie.objects.create(title='test movie', duration=90)
        self.client.patch(
            '/movies/{}/'.format(movie.id),
            {
                'title': 'updated test title',
                'duration': 30
            },
            format='json',
        )
        updated = Movie.objects.get(id=movie.id)
        self.assertEqual(updated.title, "updated test title")


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

    def test_list_showtime(self):
        room = Room.objects.create(name='room test', capacity=30)
        movie = Movie.objects.create(title='title test', duration=90)
        start = dt.datetime.strptime('2020-06-29 08:15', '%Y-%m-%d %H:%M')
        end = start + dt.timedelta(minutes=movie.duration)
        Showtime.objects.create(room=room, movie=movie, start_date=start, end_date=end,
                                           available=room.capacity)
        showtime_count = Showtime.objects.count()
        response = self.client.get('/showtimes/')
        self.assertEqual(len(response.data), showtime_count)

    def test_update_showtime(self):
        room = Room.objects.create(name='room test', capacity=30)
        movie = Movie.objects.create(title='title test', duration=90)
        start = dt.datetime.strptime('2020-06-29 08:15', '%Y-%m-%d %H:%M')
        start2 = dt.datetime.strptime('2020-08-29 08:15', '%Y-%m-%d %H:%M')
        end = start + dt.timedelta(minutes=movie.duration)
        showtime = Showtime.objects.create(room=room, movie=movie, start_date=start, end_date=end,
                                           available=room.capacity)
        self.client.patch(
            '/showtimes/{}/'.format(showtime.id),
            {
                'room': room.id,
                'movie': movie.id,
                'start_date': start2,
                'end_date': end,
                'available': 30
            },
            format='json',
        )
        updated = Showtime.objects.get(id=showtime.id)
        self.assertEqual(updated.start_date,
                         dt.datetime.strptime('2020-08-29 08:15', '%Y-%m-%d %H:%M'))


class TicketTestCase(APITestCase):

    def test_create_ticket(self):
        initial_ticket_count = Ticket.objects.count()
        room = Room.objects.create(name='room test', capacity=30)
        movie = Movie.objects.create(title='title test', duration=90)
        start = dt.datetime.strptime('2020-06-29 08:15', '%Y-%m-%d %H:%M')
        end = start + dt.timedelta(minutes=movie.duration)
        showtime = Showtime.objects.create(room=room, movie=movie, start_date=start, end_date=end,
                                           available=room.capacity)
        ticket_attrs = {'showtime': showtime.id, 'num_seats': 1}
        response = self.client.post('/tickets/', ticket_attrs, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), initial_ticket_count + 1)
        self.assertEqual(response.data['showtime'], str(showtime))
        self.assertEqual(response.data['num_seats'], ticket_attrs['num_seats'])

    def test_delete_ticket(self):
        room = Room.objects.create(name='room test', capacity=30)
        movie = Movie.objects.create(title='title test', duration=90)
        start = dt.datetime.strptime('2020-06-29 08:15', '%Y-%m-%d %H:%M')
        end = start + dt.timedelta(minutes=movie.duration)
        showtime = Showtime.objects.create(room=room, movie=movie, start_date=start, end_date=end,
                                           available=room.capacity)
        ticket = Ticket.objects.create(showtime=showtime, num_seats=1)
        initial_ticket_count = Ticket.objects.count()
        self.client.delete('/tickets/{}/'.format(ticket.id))
        self.assertEqual(Ticket.objects.count(), initial_ticket_count - 1)

    def test_list_ticket(self):
        room = Room.objects.create(name='room test', capacity=30)
        movie = Movie.objects.create(title='title test', duration=90)
        start = dt.datetime.strptime('2020-06-29 08:15', '%Y-%m-%d %H:%M')
        end = start + dt.timedelta(minutes=movie.duration)
        showtime = Showtime.objects.create(room=room, movie=movie, start_date=start, end_date=end,
                                           available=room.capacity)
        ticket_attrs = {'showtime': showtime.id, 'num_seats': 1}
        response = self.client.post('/tickets/', ticket_attrs, format='json')
        tickets_count = Ticket.objects.count()
        response = self.client.get('/tickets/')
        self.assertEqual(len(response.data), tickets_count)

    def test_update_ticket(self):
        room = Room.objects.create(name='room test', capacity=30)
        movie = Movie.objects.create(title='title test', duration=90)
        start = dt.datetime.strptime('2020-06-29 08:15', '%Y-%m-%d %H:%M')
        end = start + dt.timedelta(minutes=movie.duration)
        showtime = Showtime.objects.create(room=room, movie=movie, start_date=start, end_date=end,
                                           available=room.capacity)
        ticket = Ticket.objects.create(showtime=showtime, num_seats=1)
        self.client.patch(
            '/tickets/{}/'.format(ticket.id),
            {
                'showtime': showtime.id,
                'num_seats': 2
            },
            format='json',
        )
        updated = Ticket.objects.get(id=ticket.id)
        self.assertEqual(updated.num_seats, 2)
