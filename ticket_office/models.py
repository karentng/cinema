from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField(default=0)


class Movie(models.Model):
    title = models.CharField(max_length=200)


class Showtime(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    time = models.TimeField()


class Customer(models.Model):
    name = models.CharField(max_length=200)


class Ticket(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    client = models.ForeignKey(Customer, on_delete=models.CASCADE)




