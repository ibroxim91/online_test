from django.contrib import admin
from main.models import *

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','duration']
    readonly_fields = ['quiz_count']


class AnswerAdmin(admin.TabularInline):
    model = Variant

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['category','title']
    inlines = [ AnswerAdmin ]

class HistoryAdmin(admin.TabularInline):
    model = History

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['category','user',"start_date","end"]
    inlines = [ HistoryAdmin ]