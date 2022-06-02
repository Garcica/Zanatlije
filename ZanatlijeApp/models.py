from django.db import models
from PIL import Image


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Caskanje(models.Model):
    idcaskanje = models.AutoField(db_column='idCaskanje', primary_key=True)  # Field name made lowercase.
    idkorisnik = models.ForeignKey('Korisnik', models.DO_NOTHING, db_column='idKorisnik')  # Field name made lowercase.
    idzanatlija = models.ForeignKey('Zanatlija', models.DO_NOTHING,
                                    db_column='idZanatlija')  # Field name made lowercase.
    smer = models.CharField(max_length=1)
    datum_vreme = models.DateTimeField()
    poruka = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'caskanje'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Komentari(models.Model):
    idkomentari = models.AutoField(db_column='idKomentari', primary_key=True)  # Field name made lowercase.
    idkorisnik = models.ForeignKey('Korisnik', models.DO_NOTHING, db_column='idKorisnik')  # Field name made lowercase.
    idzanatlija = models.ForeignKey('Zanatlija', models.DO_NOTHING,
                                    db_column='idZanatlija')  # Field name made lowercase.
    smer = models.CharField(max_length=1)
    komentar = models.CharField(max_length=255)
    datum_vreme = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'komentari'


class Korisnik(models.Model):
    idkorisnik = models.AutoField(db_column='idKorisnik', primary_key=True)  # Field name made lowercase.
    ime = models.CharField(max_length=45)
    prezime = models.CharField(max_length=45)
    username = models.CharField(unique=True, max_length=45)
    pol = models.CharField(max_length=1)
    sifra = models.CharField(max_length=45)
    grad = models.CharField(max_length=45)
    email = models.CharField(unique=True, max_length=45)
    telefon = models.CharField(max_length=45)
    opis = models.CharField(db_column='Opis', max_length=255, blank=True, null=True)  # Field name made lowercase.
    slika = models.ImageField(upload_to='korisnici_img', blank=True, null=True)
    status = models.CharField(max_length=1)
    datum_ban = models.DateField(blank=True, null=True)
    ocena = models.IntegerField(blank=True, null=True)
    br_ocena = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'korisnik'


class Saradnja(models.Model):
    idsaradnja = models.AutoField(db_column='idSaradnja', primary_key=True)  # Field name made lowercase.
    idkorisnik = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='idKorisnik')  # Field name made lowercase.
    idzanatlija = models.ForeignKey('Zanatlija', models.DO_NOTHING,
                                    db_column='idZanatlija')  # Field name made lowercase.
    datum = models.DateField()
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'saradnja'


class Zanatlija(models.Model):
    idzanatlija = models.AutoField(db_column='idZanatlija', primary_key=True)  # Field name made lowercase.
    ime = models.CharField(max_length=45)
    prezime = models.CharField(max_length=45)
    username = models.CharField(unique=True, max_length=45)
    pol = models.CharField(max_length=1)
    sifra = models.CharField(max_length=45)
    grad = models.CharField(max_length=45)
    email = models.CharField(unique=True, max_length=45)
    telefon = models.CharField(max_length=45)
    opis = models.CharField(max_length=255, blank=True, null=True)
    slika = models.ImageField(upload_to='zanatlije_img', blank=True, null=True)
    zanati = models.CharField(max_length=255)
    ime_firme = models.CharField(max_length=45)
    adresa_lokala = models.CharField(max_length=45)
    status = models.CharField(max_length=1)
    datum_ban = models.DateField(blank=True, null=True)
    ocena = models.IntegerField(blank=True, null=True)
    br_ocena = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zanatlija'
