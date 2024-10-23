from django.contrib import admin
from .models import Barangay
from .models import Gender
from .models import Respondent
from .models import Survey
from .models import QuestionQuestionnaire
from .models import QuestionOptions
from .models import Questionnaire


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


admin.site.register(Gender, GenderAdmin)
admin.site.register(Respondent, RespondentAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(QuestionQuestionnaire, QuestionQuestionnaireAdmin)
admin.site.register(QuestionOptions, QuestionOptionsAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Barangay, BarangayAdmin)
