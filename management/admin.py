from django.contrib import admin
from .models import Barangay
from .models import Gender
from .models import Respondent
from .models import Survey
from .models import QuestionQuestionnaire
from .models import QuestionOptions
from .models import Questionnaire
from .models import TimeMark
from .models import BrgyLeaderAttendance


class TimeMarkAdmin(admin.ModelAdmin):
    list_name = ('name',)


class BrgyLeaderAttendanceAdmin(admin.ModelAdmin):
    list_name = ('brgy',)




class GenderAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RespondentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('respondent',)


class QuestionQuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('name',)


class QuestionOptionsAdmin(admin.ModelAdmin):
    list_display = ('question',)


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('respondent',)


class BarangayAdmin(admin.ModelAdmin):
    list_display = ('brgy_name',)


admin.site.register(TimeMark, TimeMarkAdmin)
admin.site.register(BrgyLeaderAttendance, BrgyLeaderAttendanceAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(Respondent, RespondentAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(QuestionQuestionnaire, QuestionQuestionnaireAdmin)
admin.site.register(QuestionOptions, QuestionOptionsAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Barangay, BarangayAdmin)
