
from django.contrib import admin
from .models import Quiz, Question, Option, History

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(History)
