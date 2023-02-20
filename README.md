**Zadatak:** Issue Tracker

[Dokumentacija](https://gaseri.org/hr/nastava/materijali/python-modul-django/#petlje)

## Opis
Web aplikacija za praćenje greška i problema u softverskom kodu.

**Ime studenta:** Tin Švagelj

## Nedostatci

- Kada je `User` pobrisan, `autor` `Issue`a postane null.
  - Trebala bi se stvoriti zamjenska struktura u slučaju da se `User` pojavljuje kao autor kako bi se ispravno prikazali podatci o autoru i nakon uklanjanja korisničkog računa.
    - Na ostalim mjestima gdje se referencira `User` to nije potrebno.
    - Za druge reference nije potrebno.
