import os
import re
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
    status = request.session['status']
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
        'korisnik': username,
        'status': status
    }

    return render(request, 'adminOdobravanjePrototip.html', context)


def admin(request):
    date_input = request.POST.get("Date")
    banuj_button = request.POST.get("Banuj")
    obrisi_button = request.POST.get("Obrisi")
    dodaj_button = request.POST.get("Dodaj")
    ukloni_button = request.POST.get("Ukloni")
    admin_button = request.POST.get("Admin")

    username = request.session['username']
    status = request.session['status']
    if (banuj_button or obrisi_button or dodaj_button or ukloni_button or admin_button) and request.method == 'POST':
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

        if request.POST.get('Admin'):
            user = None

            if user is None:
                try:
                    Korisnik.objects.filter(username=username).update(status="E")
                except Korisnik.DoesNotExist:
                    user = None
            if user is None:
                try:
                    Zanatlija.objects.filter(username=username).update(status="E")
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
        'Admin': admin_button,
        'korisnik': username,
        'status': status
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

        if user is not None:
            if user.datum_ban != None:
                str = 'Ne mozete da pristupite nalogu jer ste banovani!'

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
        request.session['status'] = user.status
        return redirect('myprofile', korisnik=user.username)

    return render(request, 'loginPrototip.html', context={'str': str})


def register_req(request: HttpRequest):
    error = ''
    user = None

    if request.method == 'POST':
        username = request.POST.get('username')
        if username == '':
            error = 'Molimo vas unesite sva polja!'
        if len(username) > 20:
            error = 'Predugacak username (<21)!'
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
            error = 'Korisnik sa unetim korisnickim imenom vec postoji u bazi!'
        user = None
        password = request.POST.get('password')
        if password == '':
            error = 'Molimo vas unesite sva polja!'
        if len(password) > 20:
            error = 'Predugacka lozinka (<21)!'
        passwordRepeat = request.POST.get('passwordRepeat')
        if passwordRepeat == '':
            error = 'Molimo vas unesite sva polja!'
        if password != '' and passwordRepeat != '':
            if password != passwordRepeat:
                error = 'Ne poklapaju se sifre'
        name = request.POST.get('name')
        if name == '':
            error = 'Molimo vas unesite sva polja!'
        if name != '' and not re.match(r"^[a-zA-Z]+$", name):
            error = 'Molimo vas unesite ispravno ime!'
        lastname = request.POST.get('lastName')
        if lastname == '':
            error = 'Molimo vas unesite sva polja!'
        if lastname != '' and not re.match(r"^[a-zA-Z]+$", lastname):
            error = 'Molimo vas unesite ispravno prezime!'
        pol = request.POST.get('pol')
        grad = request.POST.get('sellist')
        if grad == '':
            error = 'Molimo vas unesite sva polja!'
        mail = request.POST.get('meil')
        if mail == '':
            error = 'Molimo vas unesite sva polja!'
        if mail != '' and re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", mail) is None:
            error = 'Molimo unesite ispravnu mail adresu!'
        if user is None:
            try:
                user = Korisnik.objects.get(email=mail)
            except Korisnik.DoesNotExist:
                user = None
        if user is None:
            try:
                user = Zanatlija.objects.get(email=mail)
            except Zanatlija.DoesNotExist:
                user = None
        if user is not None:
            error = 'Korisnik sa unetim mejlom vec postoji u bazi!'
        user = None
        phone = request.POST.get('tel')
        if phone == '':
            error = 'Molimo vas unesite sva polja!'
        if phone != '' and re.match(
                r"^(\+\d{3}[\s\-\/]?\d{2}[\s\-\/]?\d{3}[\s\-\/]?\d{3,4})$|^((?:(?!\+))\d{3}[\s\-\/]?\d{3}[\s\-\/]?\d{3,4})$",
                phone) is None:
            error = 'Molimo vas unesite ispravan broj telefona!'
        desc = request.POST.get('opis')
        if desc == '':
            error = 'Molimo vas unesite sva polja!'

        if 'formFile' in request.FILES:
            slika = request.FILES['formFile']
        else:
            slika = 'default.jpg'

        #slika_ime = request.POST.get('formFile')

        zanati = request.POST.getlist('options-outlined')
        zanat = ''
        for z in zanati:
            zanat += z + '-'
        zanat = zanat[:-1]
        firma = request.POST.get('imeFirme')
        adresa = request.POST.get('adresaLokala')

        context = {
            'context': error
        }

        if error != '':
            return render(request, 'signupPrototip.html', context)

        if zanat == '':
            if slika != 'default.jpg':
                slika_ime = str(username) + '.' + str(slika).split(".")[1]
                slika_path = '../../media/korisnici_img/' + str(slika_ime)
                user = Korisnik.objects.create(username=username, sifra=password, ime=name, prezime=lastname, pol=pol,
                                               grad=grad, email=mail, telefon=phone, opis=desc, status="N",
                                               put_do_slike=slika_path)
                user.slika.save(slika_ime, slika)
                user.save()
            else:
                slika_ime = 'default.jpg'
                slika_path = '/static/slike/default.jpg'
                user = Korisnik.objects.create(username=username, sifra=password, ime=name, prezime=lastname, pol=pol,
                                               grad=grad, email=mail, telefon=phone, opis=desc, slika=None, status="N",
                                               put_do_slike=slika_path)
                user.save()
            if slika_ime is None:
                slika_ime = 'default.jpg'
                slika_path = '/static/slike/default.jpg'
            else:
                # begin = '../../media/'
                slika_path = '../../media/zanatlije_img/' + str(slika_ime)
            # print('DA')
        else:
            if slika != 'default.jpg':
                slika_ime = str(username) + '.' + str(slika).split(".")[1]
                slika_path = '../../media/zanatlije_img/' + str(slika_ime)
                user = Zanatlija.objects.create(username=username, sifra=password, ime=name, prezime=lastname, pol=pol,
                                               grad=grad, email=mail, telefon=phone, opis=desc, status="N",
                                               put_do_slike=slika_path, zanati=zanat, ime_firme=firma, adresa_lokala=adresa)
                user.slika.save(slika_ime, slika)
                user.save()
            else:
                slika_ime = 'default.jpg'
                slika_path = '/static/slike/default.jpg'
                user = Zanatlija.objects.create(username=username, sifra=password, ime=name, prezime=lastname, pol=pol,
                                               grad=grad, email=mail, telefon=phone, opis=desc, slika=None, status="N",
                                               put_do_slike=slika_path, zanati=zanat, ime_firme=firma, adresa_lokala=adresa)
                user.save()

        error = 'Registracija je uspesna. Sacekajte da vam administrator/moderator odobri registraciju!'
        context = {
            'context': error
        }
        return render(request, 'signupPrototip.html', context)

    context = {
        'context': error
    }

    return render(request, 'signupPrototip.html', context)


def profile(request: HttpRequest, korisnik):
    username = request.session['username']
    status = request.session['status']
    logged_in_as = False
    # username = korisnik
    user = None
    if user is None:
        try:
            user = Korisnik.objects.get(username=username)
            logged_in_as = False
        except Korisnik.DoesNotExist:
            user = None
    if user is None:
        try:
            user = Zanatlija.objects.get(username=username)
            logged_in_as = True
        except Zanatlija.DoesNotExist:
            user = None
    # print(user.username)
    # print(user.slika.url)
    if user.slika is None or user.slika == b'':
        slika_path = '/static/slike/default.jpg'
    else:
        begin = '../../media/'
        slika_path = begin + str(user.slika).strip('b').strip('\'')

    if logged_in_as:
        zanati = user.zanati
        ime_firme = user.ime_firme
        adresa_firme = user.adresa_lokala
        grad = user.grad
    else:
        zanati = None
        ime_firme = None
        adresa_firme = None
        grad = None

    context = {
        'username': user.username,
        'ime': user.ime,
        'prezime': user.prezime,
        'mail': user.email,
        'tel': user.telefon,
        'opis': user.opis,
        'korisnik': user.username,
        'slika': user.put_do_slike,
        'logged_in_as': logged_in_as,
        'zanati': zanati,
        'ime_firme': ime_firme,
        'adresa_firme': adresa_firme,
        'grad': grad,
        'status': status
    }
    return render(request, 'myPrototip.html', context)


def someones_profile(request: HttpRequest, neki_profil):
    korisnik = request.session['username']
    status = request.session['status']
    username = neki_profil
    logged_in_as = False
    user = None
    if user is None:
        try:
            user = Korisnik.objects.get(username=username)
            logged_in_as = False
        except Korisnik.DoesNotExist:
            user = None
    if user is None:
        try:
            user = Zanatlija.objects.get(username=username)
            logged_in_as = True
        except Zanatlija.DoesNotExist:
            user = None

    if user.slika is None or user.slika == b'':
        slika_path = '/static/slike/default.jpg'
    else:
        begin = '../../media/'
        slika_path = begin + str(user.slika).strip('b').strip('\'')

    if logged_in_as:
        zanati = user.zanati
        ime_firme = user.ime_firme
        adresa_firme = user.adresa_lokala
        grad = user.grad
    else:
        zanati = None
        ime_firme = None
        adresa_firme = None
        grad = None

    context = {
        'username': user.username,
        'ime': user.ime,
        'prezime': user.prezime,
        'mail': user.email,
        'tel': user.telefon,
        'opis': user.opis,
        'neki_profil': user.username,
        'korisnik': korisnik,
        'slika': user.put_do_slike,
        'logged_in_as': logged_in_as,
        'zanati': zanati,
        'ime_firme': ime_firme,
        'adresa_firme': adresa_firme,
        'grad': grad,
        'status': status
    }
    return render(request, 'someones_profile.html', context)


def edit(request: HttpRequest):
    username = request.session['username']
    status = request.session['status']
    user = None
    error = ''
    type = False
    naziv_firme = None
    adresa_firme = None
    grad = None
    prev_mail = None
    if user is None:
        try:
            user = Korisnik.objects.get(username=username)
            type = False
            prev_mail = user.email
        except Korisnik.DoesNotExist:
            user = None
    if user is None:
        try:
            user = Zanatlija.objects.get(username=username)
            type = True
            naziv_firme = user.ime_firme
            adresa_firme = user.adresa_lokala
            grad = user.grad
            prev_mail = user.email
        except Zanatlija.DoesNotExist:
            user = None

    if user.slika is None or user.slika == b'':
        slika_path = '/static/slike/default.jpg'
    else:
        begin = '../../media/'
        slika_path = begin + str(user.slika).strip('b').strip('\'')

    checkUser = None
    dobar = True

    if request.method == 'POST':
        if not type:
            imeprezime = request.POST.get('imeprezime')
            if imeprezime != '':
                ime = str(imeprezime).split(' ')[0]
                prezime = str(imeprezime).split(' ')[1]
                Korisnik.objects.filter(username__exact=username).update(ime=ime, prezime=prezime)
            else:
                error = 'Molimo vas unesite sva polja!'
            mail = request.POST.get('mail')
            if mail == '':
                # Korisnik.objects.filter(username__exact=username).update(email=mail)
                # else:
                error = 'Molimo vas unesite sva polja!'
                dobar = False

            if mail != '' and re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", mail) is None:
                error = 'Molimo unesite ispravnu mail adresu!'
                dobar = False
            if checkUser is None:
                try:
                    checkUser = Korisnik.objects.get(email=mail)
                except Korisnik.DoesNotExist:
                    checkUser = None
            if checkUser is None:
                try:
                    checkUser = Zanatlija.objects.get(email=mail)
                except Zanatlija.DoesNotExist:
                    checkUser = None
            if checkUser is not None and checkUser.email != prev_mail:
                error = 'Korisnik sa unetim mejlom vec postoji u bazi!'
                dobar = False

            checkUser = None

            if dobar:
                Korisnik.objects.filter(username__exact=username).update(email=mail)

            dobar = True

            tel = request.POST.get('tel')
            if tel == '':
                # Korisnik.objects.filter(username__exact=username).update(telefon=tel)
                # else:
                error = 'Molimo vas unesite sva polja!'
                dobar = False
            if tel != '' and re.match(
                    r"^(\+\d{3}[\s\-\/]?\d{2}[\s\-\/]?\d{3}[\s\-\/]?\d{3,4})$|^((?:(?!\+))\d{3}[\s\-\/]?\d{3}[\s\-\/]?\d{3,4})$",
                    tel) is None:
                error = 'Molimo vas unesite ispravan broj telefona!'
                dobar = False

            if dobar:
                Korisnik.objects.filter(username__exact=username).update(telefon=tel)

            dobar = True

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
                'slika': slika_path,
                'status': status
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
            if mail == '':
                # Korisnik.objects.filter(username__exact=username).update(email=mail)
                # else:
                error = 'Molimo vas unesite sva polja!'
                dobar = False

            if mail != '' and re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", mail) is None:
                error = 'Molimo unesite ispravnu mail adresu!'
                dobar = False
            if checkUser is None:
                try:
                    checkUser = Korisnik.objects.get(email=mail)
                except Korisnik.DoesNotExist:
                    checkUser = None
            if checkUser is None:
                try:
                    checkUser = Zanatlija.objects.get(email=mail)
                except Zanatlija.DoesNotExist:
                    checkUser = None
            if checkUser is not None and checkUser.email != prev_mail:
                error = 'Korisnik sa unetim mejlom vec postoji u bazi!'
                dobar = False

            checkUser = None

            if dobar:
                Zanatlija.objects.filter(username__exact=username).update(email=mail)

            dobar = True

            tel = request.POST.get('tel')
            if tel == '':
                # Korisnik.objects.filter(username__exact=username).update(telefon=tel)
                # else:
                error = 'Molimo vas unesite sva polja!'
                dobar = False
            if tel != '' and re.match(
                    r"^(\+\d{3}[\s\-\/]?\d{2}[\s\-\/]?\d{3}[\s\-\/]?\d{3,4})$|^((?:(?!\+))\d{3}[\s\-\/]?\d{3}[\s\-\/]?\d{3,4})$",
                    tel) is None:
                error = 'Molimo vas unesite ispravan broj telefona!'
                dobar = False

            if dobar:
                Zanatlija.objects.filter(username__exact=username).update(telefon=tel)

            dobar = True
            opis = request.POST.get('opis')
            if opis != '':
                Zanatlija.objects.filter(username__exact=username).update(opis=opis)
            else:
                error = 'Molimo vas unesite sva polja!'

            naziv_firme = request.POST.get('naziv_firme')
            if naziv_firme != '':
                Zanatlija.objects.filter(username__exact=username).update(ime_firme=naziv_firme)

            adresa_firme = request.POST.get('adresa_firme')
            if adresa_firme != '':
                Zanatlija.objects.filter(username__exact=username).update(adresa_lokala=adresa_firme)

            grad = request.POST.get('grad')
            if grad != '':
                Zanatlija.objects.filter(username__exact=username).update(grad=grad)
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
                'slika': slika_path,
                'naziv_firme': naziv_firme,
                'adresa_firme': adresa_firme,
                'grad': grad,
                'type': type,
                'status': status
            }

            # print(type)

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
        'slika': slika_path,
        'naziv_firme': naziv_firme,
        'adresa_firme': adresa_firme,
        'grad': grad,
        'type': type,
        'status': status
    }
    return render(request, 'editProfile.html', context)


def logout_req(request):
    logout(request)
    return redirect('login')


def self_delete_req(request):
    # obrisi_button = request.POST.get("ObrisiProfil")
    username = request.session['username']
    user = None

    # print(obrisi_button)

    # if obrisi_button and request.method == 'POST':
    # print("GOT A POST REQUEST FOR DELETE")
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

    user.delete()
    return redirect('login')


def moderator(request):
    date_input = request.POST.get("Date")
    banuj_button = request.POST.get("Banuj")
    obrisi_button = request.POST.get("Obrisi")
    username = request.session['username']
    status = request.session['status']
    if (banuj_button or obrisi_button) and request.method == 'POST':
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
        'korisnik': username,
        'status': status
    }

    return render(request, 'moderatorPanel.html', context)


def search(request):
    username = request.session['username']
    korisnik = username
    status = request.session['status']
    error = ''
    submited = False

    if request.method == "POST":
        submited = True
        zanati = request.POST.getlist('options-outlined')


        if len(zanati) == 0:
            error = 'Morate odabrati barem jedan zanat!'

        grad = request.POST.get('sellist')

        if grad is None:
            error = 'Morate odabrati grad!'

        if error != '':
            context = {
                'korisnik': korisnik,
                'status': status,
                'error': error,
                'submited': submited
            }
            return render(request, 'searchLoggedPrototip.html', context)

        zanat = ''
        for z in zanati:
            zanat += z + '-'
        zanat = zanat[:-1]

        zanati = zanat.split("-")

        total_zanatlije = []

        for z in zanati:
            zanatlije = Zanatlija.objects.filter(Q(zanati__contains=z) & Q(grad__exact=grad) & ~Q(status__exact="N"))

            if zanatlije is not None:
                total_zanatlije = list(chain(total_zanatlije, zanatlije))

        if len(total_zanatlije) > 0:
            zanatlije_no_duplicates_set = set(total_zanatlije)
        else:
            zanatlije_no_duplicates_set = None

        if zanatlije_no_duplicates_set is not None:
            zanatlije_no_duplicates = sorted(zanatlije_no_duplicates_set, key=lambda x: x.ocena, reverse=True)
        else:
            zanatlije_no_duplicates = None

        if zanatlije_no_duplicates is not None and len(zanatlije_no_duplicates) > 0:
            numOfRows = int(len(zanatlije_no_duplicates) / 4) + 1
            rowList = []
            for i in range(0, numOfRows):
                rowList.append(0)
        else:
            numOfRows = 0
            rowList = []

        context = {
            'korisnik': korisnik,
            'status': status,
            'error': error,
            'zanatlije': zanatlije_no_duplicates,
            'numOfRows': rowList,
            'submited': submited
        }

        return render(request, 'searchLoggedPrototip.html', context)


    context = {
        'korisnik': korisnik,
        'status': status,
        'error': error,
        'submited': submited
    }

    return render(request, 'searchLoggedPrototip.html', context)
