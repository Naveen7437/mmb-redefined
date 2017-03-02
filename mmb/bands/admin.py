from django.contrib import admin

from .models import Band, BandMember, BandVacancy, BandFollowers, BandVacancyApplication, BandMemberInstrument


class BandAdmin(admin.ModelAdmin):
    model = Band
    list_display = ['name', 'active']


class BandMemberAdmin(admin.ModelAdmin):
    model = BandMember
    list_display = ['member', 'band', 'active', 'access']


class BandVacancyAdmin(admin.ModelAdmin):
    model = BandVacancy
    list_display = ['band', 'instrument', 'active']


class BandVacancyApplicationAdmin(admin.ModelAdmin):
    model = BandVacancyApplication
    list_display = ['band_vacancy', 'applicant', 'active']

admin.site.register(Band, BandAdmin)
admin.site.register(BandMember, BandMemberAdmin)
admin.site.register(BandFollowers)
admin.site.register(BandMemberInstrument)
admin.site.register(BandVacancy, BandVacancyAdmin)
admin.site.register(BandVacancyApplication, BandVacancyApplicationAdmin)


