**Zadatak:** Issue Tracker

## Opis
Web aplikacija za praćenje greška i problema u softverskom kodu.

Ciljani sadržaj:
- [ ] Stvaranje, ažuriranje i praćenje stanja grešaka i drugih problema u kodu.
- [ ] Dodjeljivanje razina prioriteta greškama i problemima i praćenje njihovog stanja dok se rade.
- [ ] Suradnja više programera na istom problemu.
- [ ] Pružanje detaljnih izvješća o stanju grešaka i problema, kao i napretku razvojnih zadataka.

**Ime studenta:** Tin Švagelj

## Nedostatci

- Kada je `User` pobrisan, `autor` `Issue`a postane null.
  - Trebala bi se stvoriti zamjenska struktura u slučaju da se `User` pojavljuje kao autor kako bi se ispravno prikazali podatci o autoru i nakon uklanjanja korisničkog računa.
    - Na ostalim mjestima gdje se referencira `User` to nije potrebno.
    - Za druge reference nije potrebno.
