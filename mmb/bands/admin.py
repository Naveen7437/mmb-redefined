from django.contrib import admin

from .models import Band, BandMember, BandVacancy, BandFollowers, BandVacancyApplication

admin.site.register(Band)
admin.site.register(BandMember)
admin.site.register(BandFollowers)
admin.site.register(BandVacancy)
admin.site.register(BandVacancyApplication)
