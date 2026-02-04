from django.contrib import admin
from .models import KnowledgeBase,Conversation

# Register your models here.
admin.site.register(KnowledgeBase)

admin.site.register(Conversation)