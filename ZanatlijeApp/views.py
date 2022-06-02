import os.path
from itertools import chain
import datetime
from django.core.files.base import ContentFile, File
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.dateparse import parse_date

from ZanatlijeApp.forms import DateForm
from ZanatlijeApp.models import Korisnik, Zanatlija


def admin_odobravanje(request):
    odobri_button = request.POST.get("Odobri")
    odbij_button = request.POST.get("Odbij")

    if (odobri_button or odbij_button) and request.method == 'POST':
        if request.POST.get('Odobri'):
            username = request.POST.get("username", "")
            user = None
            if user is None:
                try:
                    Korisnik.objects.filter(username=username).update(status="A")
                except Korisnik.DoesNotExist:
                    user = None
            if user is None:
                try:
                    Zanatlija.objects.filter(username=username).update(status="A")
                except Zanatlija.DoesNotExist:
                    user = None

        elif request.POST.get('Odbij'):
            username = request.POST.get("username", "")
            user = None
            if user is None:
                try:
                    Korisnik.objects.get(username=username)
                except Korisnik.DoesNotExist:
                    user = None
            if user is None:
                try:
                    Zanatlija.objects.get(username=username)
                except Zanatlija.DoesNotExist:
                    user = None
            if user is not None:
                user.delete()

    try:
        users_not_approved = Korisnik.objects.filter(status="N")
    except Korisnik.DoesNotExist:
        users_not_approved = None
    try:
        workers_not_approved = Zanatlija.objects.filter(status="N")
    except Zanatlija.DoesNotExist:
        workers_not_approved = None

    if users_not_approved is not None and workers_not_approved is not None:
        total_not_approved = list(chain(users_not_approved, workers_not_approved))
    elif users_not_approved is not None and workers_not_approved is None:
        total_not_approved = list(users_not_approved)
    elif users_not_approved is None and workers_not_approved is not None:
        total_not_approved = list(workers_not_approved)
    else:
        total_not_approved = None

    context = {
        'users': total_not_approved,
        'Odobri': odobri_button,
        'Odbij': odbij_button
    }

    return render(request, 'adminOdobravanjePrototip.html', context)


def admin(request):
    date_input = request.POST.get("Date")
    banuj_button = request.POST.get("Banuj")
    obrisi_button = request.POST.get("Obrisi")
    dodaj_button = request.POST.get("Dodaj")
    ukloni_button = request.POST.get("Ukloni")

    if (banuj_button or obrisi_button or dodaj_button or ukloni_button) and request.method == 'POST':
        username = request.POST.get("username", "")


        if request.POST.get('Obrisi'):
            user = None
            if user is None:
                try:
                    user = Korisnik.objects.get(username=username)
                except Korisnik.DoesNotExist:
                    user = None
            if user is None:
                try:
                    user = Zanatlija.objects.get(username=username)
                except Zanatlija.DoesNotExist:
                    user = None
            if user is not None:
                user.delete()

        if request.POST.get('Dodaj'):
            user = None
            if user is None:
                try:
                    Korisnik.objects.filter(username=username).update(status="M")
                except Korisnik.DoesNotExist:
                    user = None
            if user is None:
                try:
                    Zanatlija.objects.filter(username=username).update(status="M")
                except Zanatlija.DoesNotExist:
                    user = None

        if request.POST.get('Ukloni'):
            user = None
            if user is None:
                try:
                    Korisnik.objects.filter(username=username).update(status="A")
                except Korisnik.DoesNotExist:
                    user = None
            if user is None:
                try:
                    Zanatlija.objects.filter(username=username).update(status="A")
                except Zanatlija.DoesNotExist:
                    user = None

        if request.POST.get('Banuj'):
            user = None
            dateStr = request.POST.get("Date", "")
            dateStrArr = dateStr.split("-")
            date = datetime.date(int(dateStrArr[0]), int(dateStrArr[1]), int(dateStrArr[2]))
            #return HttpResponse(date)
            if user is None:
                try:
                    Korisnik.objects.filter(username=username).update(datum_ban=date)
                except Korisnik.DoesNotExist:
                    user = None
            if user is None:
                try:
                    Zanatlija.objects.filter(username=username).update(datum_ban=date)
                except Zanatlija.DoesNotExist:
                    user = None
    try:
        users_regular = Korisnik.objects.filter(~Q(status="N"))
    except Korisnik.DoesNotExist:
        users_regular = None
    try:
        users_workers = Zanatlija.objects.filter(~Q(status="N"))
    except Zanatlija.DoesNotExist:
        users_workers = None

    if users_regular is not None and users_workers is not None:
        total = list(chain(users_regular, users_workers))
    elif users_regular is not None and users_workers is None:
        total = list(users_regular)
    elif users_regular is None and users_workers is not None:
        total = list(users_workers)
    else:
        total = None

    context = {
        'users': total,
        'Date': date_input,
        'Banuj': banuj_button,
        'Obrisi': obrisi_button,
        'Dodaj': dodaj_button,
        'Ukloni': ukloni_button
    }

    return render(request, 'adminPrototip.html', context)


def search(request):
    return render(request, 'searchPrototip.html')
