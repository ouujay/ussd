from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Session

def ussd_callback(request):
    session_id = request.POST.get("sessionId", "")
    phone_number = request.POST.get("phoneNumber", "")
    text = request.POST.get("text", "")

    response = ""

    if text == "":
        response = "CON What would you want to check \n1. My Account \n2. My phone number"
    elif text == "1":
        response = "CON Choose account info to view\n1. Account number\n2. Account balance"
    elif text == "1*1":
        response = "END Your account number is ACC1001"
    elif text == "1*2":
        response = "END Your balance is ₦10,000"
    elif text == "2":
        response = f"END This is your phone number: {phone_number}"
    else:
        response = "END Invalid input"

    return HttpResponse(response, content_type="text/plain")
