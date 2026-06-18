# System Rezerwacji Stolików w Restauracji

## Opis
Aplikacja służy do zarządzania rezerwacjami miejsc w restauracji. System pozwala na dodawanie stolików, zapisywanie klientów oraz przypisywanie wolnych stolików do konkretnych osób na podaną godzinę. Program pozwala też na płacenie rachunków na różne sposoby.

---

## Lista klas

* **Restauracja**
    * **Odpowiedzialność:** Główna klasa w programie. Trzyma listy stolików oraz rezerwacji i pilnuje, żeby wszystko trafiało na swoje miejsc
    * **Właściwości:** `_nazwa`, `_stoliki`, `_rezerwacje`.
    * **Metody:** `dodaj_stolik()`, `stworz_rezerwacje()`, `wyswietl_rezerwacje()`.
* **Stolik**
    * **Odpowiedzialność:** Reprezentuje konkretny stolik na sali i pilnuje, czy ktoś przy nim siedzi.
    * **Właściwości:** `_numer`, `_liczba_miejsc`, `_czy_zajety`.
    * **Metody:** `czy_jest_wolny()`, `zarezerwuj()`, `zwolnij()`.
* **Klient**
    * **Odpowiedzialność:** Trzyma dane klienta, który robi rezerwację.
    * **Właściwości:** `_identyfikator`, `_imie`, `_telefon`.
    * **Metody:** `pobierz_imie()`.
* **Rezerwacja**
    * **Odpowiedzialność:** Łączy klienta z konkretnym stolikiem i godziną.
    * **Właściwości:** `_identyfikator`, `_klient`, `_stolik`, `_godzina`.
    * **Metody:** `wyswietl_szczegoly()`, `pobierz_stolik()`.
* **Transakcja**
    * **Odpowiedzialność:** Ogólny szablon dla płatności.
    * **Właściwości:** `_identyfikator`, `_kwota`.
    * **Metody:** `realizuj()`.
* **PlatnoscKarta**
    * **Odpowiedzialność:** Obsługuje płatności kartą przez terminal.
    * **Właściwości:** Wszystko z klasy Transakcja oraz `_numer_karty`.
    * **Metody:** `realizuj()`.
* **PlatnoscGotowka**
    * **Odpowiedzialność:** Obsługuje płatności gotówką przy kasie.
    * **Właściwości:** Przejęte z klasy Transakcja.
    * **Metody:** `realizuj()`.

---

## Opis relacji między klasami

Klasy łączą się ze sobą na podstawie schematów 

1. **Kolekcja / Agregacja  Klasa `Restauracja` trzyma w środku listy `self._stoliki` oraz `self._rezerwacje`. Stoliki to osobne obiekty i mogą istnieć nawet, jeśli zamkniemy restaurację.
2. **Przekazanie obiektu jako parametr metody  Metoda `dodaj_stolik(stolik)` dostaje z zewnątrz gotowy obiekt stolika i po prostu wrzuca go do listy w restauracji.
3. **Właściwość Klasa `Rezerwacja` zapisuje w swoich polach `self._klient` i `self._stolik` bezpośrednie linki do tych obiektów, żeby wiedzieć, kto i gdzie siedzi.
4. **Dziedziczenie Klasy `PlatnoscKarta` i `PlatnoscGotowka` dziedziczą po klasie `Transakcja`, bo każda z nich "jest rodzajem" transakcji.

---

## Cztery zasady OOP (4 Filary)

1. **Enkapsulacja (Prezentacja "Cztery zasady OOP", Slajd 3i 4)**
   * **Gdzie jest:** W klasie `Stolik`.
   * **Jak to działa:** Wszystkie zmienne mają na początku podkreślenie (np. `self._czy_zajety`), co oznacza, że są schowane. Zgodnie z analogią bankomatu ze slajdu 3 (gdzie używa się przycisków, a nie pcha ręce do sejfu), nikt z zewnątrz nie może ręcznie zmienić stanu stolika. Trzeba wywołać metodę `zarezerwuj()`, która najpierw sama sprawdza, czy stolik jest wolny, i dopiero wtedy bezpiecznie go zajmuje.

2. **Dziedziczenie (Prezentacja "Cztery zasady OOP", Slajd 5 i 6 / Prezentacja "Kompozycja vs dziedziczenie", Slajd 9)**
   * **Gdzie jest:** W klasach `PlatnoscKarta`, `PlatnoscGotowka` i `Transakcja`.
   * **Jak to działa:** Płatność kartą i gotówką to są rodzaje transakcji. Dzięki temu nie musiałem pisać dwa razy tych samych zmiennych (jak id i kwota) – podklasy dostały je automatycznie z klasy nadrzędnej `Transakcja` przez `super().__init__()`.

3. **Polimorfizm (Prezentacja "Cztery zasady OOP", Slajd 7)**
   * **Gdzie jest:** W głównej sekcji programu przy uruchamianiu płatności.
   * **Jak to działa:** Stworzyłem listę `lista_transakcji`, na którą wrzuciłem płatność kartą i płatność gotówką. Potem puściłem pętlę i na każdym obiekcie wywołałem to samo polecenie: `transakcja.realizuj()`. Dokładnie jak w przykładzie ze slajdu 7 (gdzie Pies i Kot mają metodę `daj_glos()`), program sam wie, kogo wywołuje – karta wypisze komunikat o terminalu, a gotówka o przyjęciu pieniędzy.

4. **Abstrakcja (Prezentacja "Cztery zasady OOP", Slajd 9 i 10)**
   * **Gdzie jest:** W klasie `Transakcja` i metodzie `realizuj()`.
   * **Jak to działa:** Zrobiłem z `Transakcji` klasę abstrakcyjną przy użyciu `abc.ABC` i `@abstractmethod`, dokładnie tak jak na wzorze. Przez to nie można stworzyć pustego obiektu `Transakcja()`. Klasa działa jak oficjalny kontrakt – zmusza podklasy (kartę i gotówkę) do tego, żeby każda z nich napisała swoją własną wersję metody `realizuj()`.

---

## Wykryte i poprawione błędy

Podczas pisania kodu udało mi się uniknąć typowych błędów z prezentacji:

* **Błąd 1:** Na początku mogłem zmienić stan stolika pisząc w programie `stolik._czy_zajety = True`. Poprawiłem to zgodnie z prezentacja i teraz program używa metody `stolik.zarezerwuj()`, która sama pilnuje reguł.
* **Błąd 2 :** Myślałem, żeby klasa `Stolik` dziedziczyła po klasie `Restauracja` (bo stolik jest w restauracji). Według prezentacji to błąd, bo stolik nie jest rodzajem restauracji. Poprawiłem to i teraz restauracja ma po prostu w środku listę ze stolikami.
* **Błąd 3:** Na początku planowałem stworzyć jedną wielką klasę `SystemRestauracji`, która obsługuje klientów, rezerwacje i kasę. Zgodnie z prezentacją podzieliłem system na mniejsze, osobne klasy, z których każda odpowiada za swoją część zadania.