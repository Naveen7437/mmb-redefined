from django.db import models


class Genre(models.Model):
    genre = models.CharField(max_length=30)

    def __str__(self):
        return '{}'.format(self.genre)


class Instrument(models.Model):
    instrument = models.CharField(max_length=30)
    instrumentalist = models.CharField(max_length=33)
    # level = models.CharField(choices=SKILL_LEVEL, default='Beginner')

    def __str__(self):
        return '{}'.format(self.instrument)
