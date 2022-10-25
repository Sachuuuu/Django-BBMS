from django.contrib import admin
from .models import Teams,Games,Player,Coach,userRecords,teamRecords

# Register your models here.
admin.site.register(Teams)
admin.site.register(Games)
admin.site.register(Player)
admin.site.register(Coach)
admin.site.register(userRecords)
admin.site.register(teamRecords)