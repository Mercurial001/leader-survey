from django.db import models


class Barangay(models.Model):
    brgy_name = models.CharField(max_length=255)
    brgy_voter_population = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.brgy_name

    class Meta:
        ordering = ['brgy_name']


class Gender(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Respondent(models.Model):
    name = models.CharField(max_length=255)
    brgy = models.ForeignKey(Barangay, related_name='survey_brgy', on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, related_name='respondent_gender', on_delete=models.PROTECT)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    facebook_account = models.CharField(max_length=400, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Survey(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE, related_name='survey_respondent')
    question_1 = models.TextField(null=True, blank=True)
    question_2 = models.TextField(null=True, blank=True)
    question_3 = models.TextField(null=True, blank=True)


class QuestionQuestionnaire(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class QuestionOptions(models.Model):
    question = models.ForeignKey(
        QuestionQuestionnaire,
        on_delete=models.CASCADE,
        related_name='questionnaire_question'
    )
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Questionnaire(models.Model):
    respondent = models.ForeignKey(
        Respondent,
        on_delete=models.CASCADE, related_name='questionnaire_respondent')
    question = models.ForeignKey(
        QuestionQuestionnaire,
        related_name='real_questionnaire_question',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    selected_option = models.ForeignKey(
        QuestionOptions,
        related_name='selected_question_option',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    selected_options = models.ManyToManyField(
        QuestionOptions,
        blank=True
    )
