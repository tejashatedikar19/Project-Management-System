from django.shortcuts import render, redirect
from django.conf import settings
import openpyxl
from django.http import HttpResponse
from io import BytesIO

from authentication.models import Coordinator, Group

def dashboard(request):
    if request.user.is_anonymous:
        return redirect('login')
    return render(request, 'dashboard.html', {'ps_date': settings.PS_SUBMISSION, 'midsem_date': settings.MIDSEM_SUBMISSION, 'endsem_date': settings.ENDSEM_SUBMISSION})

def setDeadline(request):
    if request.user.is_anonymous:
        return redirect('login')

    if request.method == 'POST':
        if request.POST.get('ps_submission'):
            settings.PS_SUBMISSION = request.POST.get('ps_submission')
            print(settings.PS_SUBMISSION)
        elif request.POST.get('midsem'):
            settings.MIDSEM_SUBMISSION = request.POST.get('midsem')
            print(settings.MIDSEM_SUBMISSION)
        elif request.POST.get('endsem'):
            settings.ENDSEM_SUBMISSION = request.POST.get('endsem')
            print(settings.ENDSEM_SUBMISSION)
    return redirect('dashboard')

def downloadReport(request):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Report"

    headers = ["Group Number", "Department", "Division", "Roll Numbers", "Project Title", "Project Domain", "Problem Statement Submission", "Mid-Semester Submission", "End-Semester Submission"]
    sheet.append(headers)

    coordinator = Coordinator.objects.get(email=request.user.username)
    data = Group.objects.filter(dept=coordinator.dept)

    for group in data:
        submitted_PS = "Yes" if group.submitted_PS else "No"
        midsem_conducted = "Yes" if group.midsem_conducted else "No"
        endsem_conducted = "Yes" if group.endsem_conducted else "No"
        row = [group.group_id, group.dept, group.div, f'{group.roll}, {group.memRoll1}, {group.memRoll2}, {group.memRoll3}', group.pname, group.domain, submitted_PS, midsem_conducted, endsem_conducted]
        sheet.append(row)

    # Saving the workbook to an in-memory file
    file_stream = BytesIO()
    workbook.save(file_stream)
    file_stream.seek(0)

    # Returning the file as an HTTP response with download headers
    response = HttpResponse(
        file_stream,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="report.xlsx"'

    return response
