from django.shortcuts import render,redirect
from django.http import HttpResponse,FileResponse
from .forms import LoginForm, surgeryForm, calendarForm
from django.conf import settings
from django.contrib.auth import login, authenticate
import os
from django.forms import formset_factory
from docx import Document
from datetime import datetime
import random
import string

def index(request):
    return render(request, "invoicePage/index.html")

def login(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        email = loginForm.cleaned_data.get('email')
        password = loginForm.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        userID = user.ID
        return redirect('home', userID = userID)
    else:
        loginForm = LoginForm()
    return render(request, "invoicePage/login.html", {"loginForm": loginForm})

def register(request):
    return render(request, "invoicePage/register.html")

from datetime import datetime

def makeInvoice(request):
    allData = []
    CalendarFormSet = formset_factory(calendarForm, extra=0)  # Set extra to 0
    calendar_formset = CalendarFormSet()  # Instantiate formset
    surgery_form = surgeryForm()  # Instantiate surgery form

    if request.method == 'POST':
        surgery_form = surgeryForm(request.POST)
        calendar_formset = CalendarFormSet(request.POST, request.FILES)  # Re-instantiate formset with POST data
        if calendar_formset.is_valid() and surgery_form.is_valid():  # Ensure all forms are valid
            for form in calendar_formset:
                cleaned_data = form.cleaned_data  # Get cleaned data from each form
                allData.append(cleaned_data)
                print(allData[-1])

            # Get the target month from the first date
            if allData:
                first_date = allData[0]['datesChosen']
                target_month = first_date.strftime('%B %Y')
            else:
                target_month = "Unknown Month"

            # Debug print to check what is in cleaned_data
            print("Surgery form cleaned data:", surgery_form.cleaned_data)

            # Create invoice using the cleaned data
            filename = createInvoice(allData, surgery_form.cleaned_data['surgeryChosen'], target_month)  # Update to match field name
            return render(request, "invoicePage/makeInvoice.html", {"calendarFormSet": calendar_formset, "surgeryForm": surgery_form, "filename": filename})
        else:
            print("Formset or surgery form is not valid")
    return render(request, "invoicePage/makeInvoice.html", {"calendarFormSet": calendar_formset, "surgeryForm": surgery_form})


def download_invoice(request, filename):
    file_path = os.path.join(settings.BASE_DIR, filename)
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    return response


def createInvoice(entries, gp_choice, target_month):
    gpName = ["Pondtail Surgery", "Shirley Medical Centre", "Bishopford Road Surgery", "Thornton Road Medical Centre"]
    gpPay = [72.5, 85, 95, 110]

    gpIndex = -1

    for i in range(len(gpName)):
        if gpName[i] == gp_choice:
            gpIndex = i
            gpPay1 = gpPay[i]
            break

    if gpIndex == -1:
        raise ValueError("Invalid surgery choice. Please provide a valid GP pay.")

    document = Document()
    document.add_heading('Invoice', 0)

    today = datetime.today()
    formatted_date = today.strftime("%d/%m/%Y")
    
    topLeft = document.add_paragraph("DATE\n")
    topLeft.add_run(formatted_date)
    topLeft.add_run("\nInvoice for ")
    topLeft.add_run(target_month)

    companyName = 'Sadiber LTD'
    firstLine = '23 Church Hill'
    postCode = 'CR8 3QP'
    phoneNumber = '07872614143'
    email = 'drsophiakhawaja@gmail.com'
    accountNo = '14459418'
    sortCode = '09-01-29'

    topRight = document.add_paragraph(companyName)
    topRight.add_run("\n")
    topRight.add_run(firstLine)
    topRight.add_run("\n")
    topRight.add_run(postCode)
    topRight.add_run("\n")
    topRight.add_run(phoneNumber)
    topRight.add_run("\n")
    topRight.add_run(email)
    topRight.add_run("\n")
    topRight.add_run(accountNo)
    topRight.add_run("\n")
    topRight.add_run(sortCode)
    topRight.alignment = 2

    bottomLeft = document.add_paragraph("INVOICE TO")
    bottomLeft.add_run("\n")
    bottomLeft.add_run(gp_choice)
    bottomLeft.add_run("\n")

    table1 = document.add_table(rows=1, cols=3, style='Medium Grid 1 Accent 1')

    column = table1.rows[0].cells
    column[0].text = 'Date'
    column[1].text = 'No. of Hours'
    column[2].text = 'Amount'

    total = 0
    for entry in entries:
        row = table1.add_row().cells
        date_str = entry['datesChosen'].strftime('%d/%m/%Y')
        hours = entry['hoursPerDay']
        amount = hours * gpPay1
        row[0].text = date_str
        row[1].text = str(hours)
        row[2].text = f"£{amount:.2f}"
        total += amount

    totalRow = table1.add_row().cells
    totalRow[2].text = f"Total: £{total:.2f}"

    # Generate a filename for the invoice with local time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Invoice_{current_time}.docx"
    document.save(filename)
    return filename

