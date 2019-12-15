import datetime as dt
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    duration = models.IntegerField(verbose_name="duration (minutes)", default=0)

    def __str__(self):
        return self.title


class Showtime(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    available = models.IntegerField()
    start_date = models.DateTimeField(default=dt.datetime.now())
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.room.name} {self.movie.title} {self.start_date}"


class Ticket(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    num_seats = models.IntegerField(verbose_name="Number of seats", default=1)

    def __str__(self):
        return f"{self.showtime.movie.title} {self.showtime.room.name} {self.showtime.start_date} {self.num_seats}"




