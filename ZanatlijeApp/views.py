import os
from itertools import chain
import datetime
from django.core.files.base import ContentFile, File
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.contrib.messages.storage import session
from django.http import HttpResponse, HttpRequest, request
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.dateparse import parse_date
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

    username = request.session['username']

    context = {
        'users': total_not_approved,
        'Odobri': odobri_button,
        'Odbij': odbij_button,
        'korisnik': username
    }

    return render(request, 'adminOdobravanjePrototip.html', context)


def admin(request):
    date_input = request.POST.get("Date")
    banuj_button = request.POST.get("Banuj")
    obrisi_button = request.POST.get("Obrisi")
    dodaj_button = request.POST.get("Dodaj")
    ukloni_button = request.POST.get("Ukloni")
    username = request.session['username']
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
        'Ukloni': ukloni_button,
        'korisnik': username,
    }

    return render(request, 'adminPrototip.html', context)


class UserBackend:

    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticateZanatlija(self, username=None, password=None):
        # print(username)
        try:
            # Try to find a user matching your username
            user = Zanatlija.objects.get(username=username)

            # print(user.username)
            #  Check the password is the reverse of the username
            if password == user.sifra:
                # Yes? return the Django user object
                return user
            else:
                # No? return None - triggers default login failed
                return None
        except Zanatlija.DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None

    def authenticateKorisnik(self, username=None, password=None):
        # print(username)
        try:
            # Try to find a user matching your username
            user = Korisnik.objects.get(username=username)

            # print(user.username)
            #  Check the password is the reverse of the username
            if password == user.sifra:
                # Yes? return the Django user object
                return user
            else:
                # No? return None - triggers default login failed
                return None
        except Korisnik.DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None

    # Required for your backend to work properly - unchanged in most scenarios

    def get_user(self, user_id):
        try:
            return Korisnik.objects.get(pk=user_id)
        except Korisnik.DoesNotExist:
            return None


def login_req(request: HttpRequest):
    str = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == '' or password == '':
            str = 'Molimo vas unesite sva polja!'

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
            if user.status == 'N':
                str = 'Registracija vam jos uvek nije odobrena!'

        if str != '':
            return render(request, 'loginPrototip.html', context={'str': str})
        # user = Zanatlija.objects.get(username=username)
        # print(user.sifra)
        user = UserBackend.authenticateZanatlija(self=UserBackend(), username=username, password=password)
        if user is None:
            user = UserBackend.authenticateKorisnik(self=UserBackend(), username=username, password=password)
        # print(user)

        if user is None:
            str = 'Nismo pronasli vas nalog'
            return render(request, 'loginPrototip.html', context={'str': str})

        context = {
            'username': user.username,
            'ime': user.ime,
            'prezime': user.prezime,
            'mail': user.email,
            'tel': user.telefon,
            'opis': user.opis,
            'korisnik': user.username,
            'str': str
        }

        request.session.create()
        request.session['username'] = user.username
        return redirect('myprofile', korisnik=user.username)

    return render(request, 'loginPrototip.html', context={'str': str})


def reister_req(request: HttpRequest):
    str = ''
    username = request.POST.get('username')
    if username == '':
        str = 'Molimo vas unesite sva polja!'
    password = request.POST.get('password')
    if password == '':
        str = 'Molimo vas unesite sva polja!'
    passwordRepeat = request.POST.get('passwordRepeat')
    if passwordRepeat == '':
        str = 'Molimo vas unesite sva polja!'
    if password != '' and passwordRepeat != '':
        if password != passwordRepeat:
            str = 'Ne poklapaju se sifre'
    name = request.POST.get('name')
    if name == '':
        str = 'Molimo vas unesite sva polja!'
    lastname = request.POST.get('lastName')
    if lastname == '':
        str = 'Molimo vas unesite sva polja!'
    pol = request.POST.get('pol')
    # print(lastname)
    grad = request.POST.get('sellist')
    if grad == '':
        str = 'Molimo vas unesite sva polja!'
    mail = request.POST.get('meil')
    if mail == '':
        str = 'Molimo vas unesite sva polja!'
    phone = request.POST.get('tel')
    if phone == '':
        str = 'Molimo vas unesite sva polja!'
    desc = request.POST.get('opis')
    if desc == '':
        str = 'Molimo vas unesite sva polja!'
    slika = request.POST.get('formFile')
    if slika == '':
        str = 'Molimo vas unesite sva polja!'
    zanati = request.POST.getlist('options-outlined')
    zanat = ''
    for z in zanati:
        zanat += z + '-'
    zanat = zanat[:-1]
    firma = request.POST.get('imeFirme')
    adresa = request.POST.get('adresaLokala')

    context = {
        'context': str
    }

    if username is None or password is None or passwordRepeat is None or name is None or lastname is None or pol is None or grad is None or mail is None or phone is None or desc is None:
        print('DA')
        return render(request, 'signupPrototip.html', context)

    if zanat == '':
        # print('DA')
        user = Korisnik.objects.create(username=username, sifra=password, ime=name, prezime=lastname, pol=pol,
                                       grad=grad, email=mail, telefon=phone, opis=desc, slika=slika, status="N")
        user.save()
    else:
        user = Zanatlija.objects.create(username=username, sifra=password, ime=name, prezime=lastname, pol=pol,
                                        grad=grad, email=mail, telefon=phone, opis=desc, slika=slika, zanati=zanat,
                                        ime_firme=firma, adresa_lokala=adresa, status="N")
        user.save()

    return render(request, 'signupPrototip.html', context)


def profile(request: HttpRequest, korisnik):
    username = request.session['username']
    # username = korisnik
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
    # print(user.username)
    # print(user.slika.url)
    begin = '../../media/'
    slika_path = begin + str(user.slika).strip('b').strip('\'')
    context = {
        'username': user.username,
        'ime': user.ime,
        'prezime': user.prezime,
        'mail': user.email,
        'tel': user.telefon,
        'opis': user.opis,
        'korisnik': user.username,
        'slika': slika_path
    }
    return render(request, 'myPrototip.html', context)


def someones_profile(request: HttpRequest, neki_profil):
    korisnik = request.session['username']
    username = neki_profil
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
    # print(user.username)
    # print(user.slika.url)
    begin = '../../media/'
    slika_path = begin + str(user.slika).strip('b').strip('\'')
    # print(slika_path)
    context = {
        'username': user.username,
        'ime': user.ime,
        'prezime': user.prezime,
        'mail': user.email,
        'tel': user.telefon,
        'opis': user.opis,
        'neki_profil': user.username,
        'korisnik': korisnik,
        'slika': slika_path
    }
    return render(request, 'someones_profile.html', context)


def edit(request: HttpRequest):
    username = request.session['username']
    user = None
    error = ''
    type = False
    if user is None:
        try:
            user = Korisnik.objects.get(username=username)
            type = False
        except Korisnik.DoesNotExist:
            user = None
    if user is None:
        try:
            user = Zanatlija.objects.get(username=username)
            type = True
        except Zanatlija.DoesNotExist:
            user = None

    begin = '../../media/'
    slika_path = begin + str(user.slika).strip('b').strip('\'')

    if request.method == 'POST':
        print("STIGAO POST REQUEST")
        if not type:
                imeprezime = request.POST.get('imeprezime')
                if imeprezime != '':
                    ime = str(imeprezime).split(' ')[0]
                    prezime = str(imeprezime).split(' ')[1]
                    Korisnik.objects.filter(username__exact=username).update(ime=ime, prezime=prezime)
                else:
                    error = 'Molimo vas unesite sva polja!'
                mail = request.POST.get('mail')
                if mail != '':
                    Korisnik.objects.filter(username__exact=username).update(email=mail)
                else:
                    error = 'Molimo vas unesite sva polja!'
                tel = request.POST.get('tel')
                if tel != '':
                    Korisnik.objects.filter(username__exact=username).update(telefon=tel)
                else:
                    error = 'Molimo vas unesite sva polja!'
                opis = request.POST.get('opis')
                if opis != '':
                    Korisnik.objects.filter(username__exact=username).update(opis=opis)
                else:
                    error = 'Molimo vas unesite sva polja!'

                context = {
                    'username': user.username,
                    'ime': user.ime,
                    'prezime': user.prezime,
                    'mail': user.email,
                    'tel': user.telefon,
                    'opis': user.opis,
                    'error': error,
                    'slika': slika_path
                }

                if error != '':
                    return render(request, 'editProfile.html', context)
                else:
                    return redirect('myprofile', korisnik=user.username)
        if type:
                imeprezime = request.POST.get('imeprezime')
                if imeprezime != '':
                    ime = str(imeprezime).split(' ')[0]
                    prezime = str(imeprezime).split(' ')[1]
                    Zanatlija.objects.filter(username__exact=username).update(ime=ime, prezime=prezime)
                else:
                    error = 'Molimo vas unesite sva polja!'
                mail = request.POST.get('mail')
                if mail != '':
                    Zanatlija.objects.filter(username__exact=username).update(email=mail)
                else:
                    error = 'Molimo vas unesite sva polja!'
                tel = request.POST.get('tel')
                if tel != '':
                    Zanatlija.objects.filter(username__exact=username).update(telefon=tel)
                else:
                    error = 'Molimo vas unesite sva polja!'
                opis = request.POST.get('opis')
                if opis != '':
                    Zanatlija.objects.filter(username__exact=username).update(opis=opis)
                else:
                    error = 'Molimo vas unesite sva polja!'

                context = {
                    'username': user.username,
                    'ime': user.ime,
                    'prezime': user.prezime,
                    'mail': user.email,
                    'tel': user.telefon,
                    'opis': user.opis,
                    'error': error,
                    'slika': slika_path
                }

                if error != '':
                    return render(request, 'editProfile.html', context)
                else:
                    return redirect('myprofile', korisnik=user.username)

    context = {
        'username': user.username,
        'ime': user.ime,
        'prezime': user.prezime,
        'mail': user.email,
        'tel': user.telefon,
        'opis': user.opis,
        'error': error,
        'slika': slika_path
    }
    return render(request, 'editProfile.html', context)


def logout_req(request):
    logout(request)
    return redirect('login')
