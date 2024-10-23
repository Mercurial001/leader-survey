from django.shortcuts import render, redirect
from .models import Barangay, Gender, Respondent, QuestionQuestionnaire, QuestionOptions, Questionnaire
import json
from django.core.serializers import serialize, deserialize
from datetime import datetime, timedelta
from datetime import date
from django.http import HttpResponseRedirect


def homepage(request):
    barangays = Barangay.objects.all()
    genders = Gender.objects.all()

    if request.method == 'POST':
        respondent_name = request.POST.get('respondent-name')
        respondent_brgy = request.POST.get('respondent-brgy')
        respondent_gender = request.POST.get('respondent-gender')
        respondent_birthday = request.POST.get('respondent-birthday')
        respondent_contact_number = request.POST.get('respondent-contact-number')
        respondents_facebook_account = request.POST.get('respondent-facebook-account')

        brgy = Barangay.objects.get(id=respondent_brgy)
        gender = Gender.objects.get(id=respondent_gender)
        birthdate = datetime.strptime(respondent_birthday, '%Y-%m-%d').date()

        respondent, created = Respondent.objects.get_or_create(
            name=respondent_name,
            brgy=brgy,
            gender=gender,
            birthdate=birthdate,
        )
        respondent.contact_number = f'{str(respondent_contact_number)}'
        respondent.facebook_account = respondents_facebook_account
        respondent.save()

        return redirect('survey', respondent_id=respondent.id)

    return render(request, 'base.html', {
        'barangays': barangays,
        'genders': genders,
    })


def survey_page(request, respondent_id):
    respondent = Respondent.objects.get(id=respondent_id)
    options = QuestionOptions.objects.all()
    question_option_dict = {}
    for option in options:
        question = option.question.name
        if question not in question_option_dict:
            question_option_dict[question] = [option]
        else:
            question_option_dict[question].append(option)

    if request.method == 'POST':
        options_selected = request.POST.getlist('options')
        print(options_selected)
        for option in options_selected:
            option_obj = QuestionOptions.objects.get(id=option)
            questionnaire, created = Questionnaire.objects.get_or_create(
                respondent=respondent,
                question=option_obj.question
            )
            questionnaire.selected_options.add(option_obj)
            questionnaire.save()
    return render(request, 'survey.html', {
        'respondent': respondent,
        'question_option_dict': question_option_dict,
    })


def qualitative_survey_view(request, respondent_id):
    respondent = Respondent.objects.get(id=respondent_id)
    return render(request, 'qualitative_survey.html', {
        'respondent': respondent,
    })


def load_barangay_json(request):
    with open('Barangay.json', 'r', encoding='utf-8') as f:
        for obj in deserialize('json', f):
            obj.save()

    return redirect('homepage')


def question_add_option(request, question_id):
    question = QuestionQuestionnaire.objects.get(id=question_id)
    options = QuestionOptions.objects.filter(question=question)

    if request.method == 'POST':
        option_name = request.POST.get('option-name')

        option, created = QuestionOptions.objects.get_or_create(
            question=question,
            name=option_name,
        )
        option.save()

        http_referrer = request.META.get('HTTP_REFERER')
        if http_referrer:
            return HttpResponseRedirect(http_referrer)
        else:
            return redirect('homepage')

    return render(request, 'question-option-add.html', {
        'question': question,
        'options': options
    })
