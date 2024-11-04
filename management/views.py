from django.shortcuts import render, redirect
from .models import Barangay, Gender, Respondent, QuestionQuestionnaire, QuestionOptions, Questionnaire, \
    BrgyLeaderAttendance, TimeMark
import json
from django.core.serializers import serialize, deserialize
from datetime import datetime, timedelta
from datetime import date
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
import pdfkit
from django.http import JsonResponse, HttpResponse


def homepage(request):
    barangays = Barangay.objects.all()
    genders = Gender.objects.all()
    respondents = Respondent.objects.all()
    print(len(respondents))

    # questionnaires = Questionnaire.objects.all()
    # questionnaire_dict = {}
    # for questionnaire in questionnaires:
    #     for option in questionnaire.selected_options.all():
    #         if option not in questionnaire_dict:
    #             questionnaire_dict[option] = [option]
    #         else:
    #             questionnaire_dict[option].append(option)
    #
    # lista = []
    # labeler = []
    # coun = []
    # for label, options in questionnaire_dict.items():
    #     lis = []
    #     for option in options:
    #         lis.append(option)
    #
    #     count = round(((len(lis) + 1) / len(respondents)) * 100)
    #     coun.append(len(lis) + 1)
    #     lista.append(count)
    #     labeler.append(label)
    #
    # results = zip(labeler, lista, coun)
    #
    # for label, percentage, count in results:
    #     option_obj = QuestionOptions.objects.get(name=label)
    #     option_obj.percentage = percentage
    #     option_obj.counts = count
    #     option_obj.save()

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
        # 'questionnaire_dict': questionnaire_dict,
        # 'lista': lista,
        # 'labeler': labeler,
        # 'results': results,
    })


def analytics(request):
    respondents = Respondent.objects.all()
    options_obj = QuestionOptions.objects.all().order_by('-percentage')
    respondents_number = len(respondents)
    questionnaires = Questionnaire.objects.all()
    questionnaire_dict = {}
    for questionnaire in questionnaires:
        for option in questionnaire.selected_options.all():
            if option not in questionnaire_dict:
                questionnaire_dict[option] = [option]
            else:
                questionnaire_dict[option].append(option)

    lista = []
    labeler = []
    coun = []
    for label, options in questionnaire_dict.items():
        lis = []
        for option in options:
            lis.append(option)

        count = round(((len(lis) + 1) / len(respondents)) * 100)
        coun.append(len(lis) + 1)
        lista.append(count)
        labeler.append(label)

    results = zip(labeler, lista, coun)

    for label, percentage, count in results:
        option_obj = QuestionOptions.objects.get(name=label)
        option_obj.percentage = percentage
        option_obj.counts = count
        option_obj.save()

    question_option_dict = {}
    for option in options_obj:
        question = option.question.name
        if question not in question_option_dict:
            question_option_dict[question] = [option]
        else:
            question_option_dict[question].append(option)

    brgy_leader_attendance_dict = {}
    for obj in BrgyLeaderAttendance.objects.all():
        meeting_date = obj.date
        if meeting_date not in brgy_leader_attendance_dict:
            brgy_leader_attendance_dict[meeting_date] = [obj]
        else:
            brgy_leader_attendance_dict[meeting_date].append(obj)

    leader_attendant_brgy = [leader.brgy for leader in BrgyLeaderAttendance.objects.all()]
    absent_brgys = []
    for real_brgy in Barangay.objects.all():
        if real_brgy not in leader_attendant_brgy:
            absent_brgys.append(real_brgy)
    print(absent_brgys)
    # Commented because the data has been derived

    respondents_brgy_dict = {}
    for respondent in respondents:
        respondent_brgy = respondent.brgy.brgy_name
        if respondent_brgy not in respondents_brgy_dict:
            respondents_brgy_dict[respondent_brgy] = [respondent]
        else:
            respondents_brgy_dict[respondent_brgy].append(respondent)

    for brgy, responds in respondents_brgy_dict.items():
        yesterdate_str = '2024-10-24'
        yesterdate = datetime.strptime(yesterdate_str, '%Y-%m-%d')
        derived_brgy_obj = Barangay.objects.get(brgy_name=brgy)

        brgy_leader_attendance_obj, created_leader_attendance = BrgyLeaderAttendance.objects.get_or_create(
            brgy=derived_brgy_obj,
            date=yesterdate,
        )

        count_processor = []
        for res in responds:
            count_processor.append(res)
            brgy_leader_attendance_obj.individuals.add(res)
        count = len(count_processor)
        brgy_leader_attendance_obj.count = count
        brgy_leader_attendance_obj.percentage = (count / respondents_number) * 100
        brgy_leader_attendance_obj.save()

    return render(request, 'dashboard.html', {
        'questionnaire_dict': questionnaire_dict,
        'lista': lista,
        'labeler': labeler,
        'results': results,
        'question_option_dict': question_option_dict,
        'respondents_number': respondents_number,
        'brgy_leader_attendance_dict': brgy_leader_attendance_dict,
        'absent_brgys': absent_brgys,
    })


def analysis_results_pdf(request):
    respondents = Respondent.objects.all()
    options_obj = QuestionOptions.objects.all().order_by('-percentage')
    respondents_number = len(respondents)
    questionnaires = Questionnaire.objects.all()
    questionnaire_dict = {}
    for questionnaire in questionnaires:
        for option in questionnaire.selected_options.all():
            if option not in questionnaire_dict:
                questionnaire_dict[option] = [option]
            else:
                questionnaire_dict[option].append(option)

    lista = []
    labeler = []
    coun = []
    for label, options in questionnaire_dict.items():
        lis = []
        for option in options:
            lis.append(option)

        count = round(((len(lis) + 1) / len(respondents)) * 100)
        coun.append(len(lis) + 1)
        lista.append(count)
        labeler.append(label)

    results = zip(labeler, lista, coun)

    for label, percentage, count in results:
        option_obj = QuestionOptions.objects.get(name=label)
        option_obj.percentage = percentage
        option_obj.counts = count
        option_obj.save()

    question_option_dict = {}
    for option in options_obj:
        question = option.question.name
        if question not in question_option_dict:
            question_option_dict[question] = [option]
        else:
            question_option_dict[question].append(option)

    brgy_leader_attendance_dict = {}
    for obj in BrgyLeaderAttendance.objects.all():
        meeting_date = obj.date
        if meeting_date not in brgy_leader_attendance_dict:
            brgy_leader_attendance_dict[meeting_date] = [obj]
        else:
            brgy_leader_attendance_dict[meeting_date].append(obj)

    leader_attendant_brgy = [leader.brgy for leader in BrgyLeaderAttendance.objects.all()]
    absent_brgys = []
    for real_brgy in Barangay.objects.all():
        if real_brgy not in leader_attendant_brgy:
            absent_brgys.append(real_brgy)

    # Commented because the data has been derived

    respondents_brgy_dict = {}
    for respondent in respondents:
        respondent_brgy = respondent.brgy.brgy_name
        if respondent_brgy not in respondents_brgy_dict:
            respondents_brgy_dict[respondent_brgy] = [respondent]
        else:
            respondents_brgy_dict[respondent_brgy].append(respondent)

    for brgy, responds in respondents_brgy_dict.items():
        yesterdate_str = '2024-10-24'
        yesterdate = datetime.strptime(yesterdate_str, '%Y-%m-%d')
        derived_brgy_obj = Barangay.objects.get(brgy_name=brgy)

        brgy_leader_attendance_obj, created_leader_attendance = BrgyLeaderAttendance.objects.get_or_create(
            brgy=derived_brgy_obj,
            date=yesterdate,
        )

        count_processor = []
        for res in responds:
            count_processor.append(res)
            brgy_leader_attendance_obj.individuals.add(res)
        count = len(count_processor)
        brgy_leader_attendance_obj.count = count
        brgy_leader_attendance_obj.percentage = (count / respondents_number) * 100
        brgy_leader_attendance_obj.save()

    html = render_to_string('analysis_results_pdf.html', {
        'questionnaire_dict': questionnaire_dict,
        'lista': lista,
        'labeler': labeler,
        'results': results,
        'question_option_dict': question_option_dict,
        'respondents_number': respondents_number,
        'brgy_leader_attendance_dict': brgy_leader_attendance_dict,
        'absent_brgys': absent_brgys,
    })

    options = {
        'margin-top': '0',
        'margin-right': '0',
        'margin-bottom': '0',
        'margin-left': '0',
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'quiet': '',
        'print-media-type': '',
        'disable-smart-shrinking': '',
        'no-outline': '',
    }

    config = pdfkit.configuration(wkhtmltopdf='C:/Users/kate/wkhtmltopdf/bin/wkhtmltopdf.exe')

    pdf = pdfkit.from_string(html, False, options=options, configuration=config)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="leader-monthly-meeting-report.pdf"'
    return response


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

        messages.success(request, "Successfully added tally!")
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
