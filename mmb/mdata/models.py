from django.db import models


class Genre(models.Model):
    genre = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return '{}'.format(self.genre)


class Instrument(models.Model):
    instrument = models.CharField(max_length=30)
    instrumentalist = models.CharField(max_length=33)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    # level = models.CharField(choices=SKILL_LEVEL, default='Beginner')

    def __str__(self):
        return '{}'.format(self.instrument)
