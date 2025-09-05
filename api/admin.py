from django.contrib import admin
from .models import *
# Register your models here.\

admin.site.register(EmailWhitelist)
admin.site.register(User)
admin.site.register(Assessment)
admin.site.register(Section)
admin.site.register(Question)
admin.site.register(Student)
