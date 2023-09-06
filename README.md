**Zadatak:** Issue Tracker

- [GitHub](https://github.com/Caellian/UNIRI_DWA_django_project)
- [Dokumentacija](https://gaseri.org/hr/nastava/materijali/python-modul-django)
- [TODO](./NOTES.md)

## Opis
Web aplikacija za praćenje greška i problema u softverskom kodu.

**Ime studenta:** Tin Švagelj

## Poznati nedostatci

- Kada je `User` pobrisan, `autor` `Issue`a postane null.
  - Trebala bi se stvoriti zamjenska struktura u slučaju da se `User` pojavljuje kao autor kako bi se ispravno prikazali podatci o autoru i nakon uklanjanja korisničkog računa.
    - Na ostalim mjestima gdje se referencira `User` to nije potrebno.
    - Za druge tipove podataka nije potrebno.
