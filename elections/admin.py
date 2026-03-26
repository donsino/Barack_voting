from django.contrib import admin
from .models import CorpsMember,Election,Position,Candidate,vote


# Register your models here.

admin.site.register(CorpsMember)
admin.site.register(Election)
admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(vote)