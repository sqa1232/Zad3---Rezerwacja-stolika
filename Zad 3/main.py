from abc import ABC, abstractmethod

class Transakcja(ABC):
    def __init__(self, identyfikator, kwota):
        self._identyfikator = identyfikator
        self._kwota = kwota

    @abstractmethod
    def realizuj(self):
        pass

class PlatnoscKarta(Transakcja):
    def __init__(self, identyfikator, kwota, numer_karty):
        super().__init__(identyfikator, kwota)
        self._numer_karty = numer_karty

    def realizuj(self):
        print(f"[TERMINAL] Zrealizowano platnosc karta o numerze {self._numer_karty} na kwote {self._kwota} zl.")

class PlatnoscGotowka(Transakcja):
    def __init__(self, identyfikator, kwota):
        super().__init__(identyfikator, kwota)

    def realizuj(self):
        print(f"[KASA] Zrealizowano platnosc gotowka na kwote {self._kwota} zl.")

class Klient:
    def __init__(self, identyfikator, imie, telefon):
        self._identyfikator = identyfikator
        self._imie = imie
        self._telefon = telefon

    def pobierz_imie(self):
        return self._imie

class Stolik:
    def __init__(self, numer, liczba_miejsc):
        self._numer = numer
        self._liczba_miejsc = liczba_miejsc
        self._czy_zajety = False

    def pobierz_numer(self):
        return self._numer

    def czy_jest_wolny(self):
        return not self._czy_zajety

    def zarezerwuj(self):
        if self._czy_zajety:
            return False
        self._czy_zajety = True
        return True

    def zwolnij(self):
        self._czy_zajety = False

class Rezerwacja:
    def __init__(self, identyfikator, klient, stolik, godzina):
        self._identyfikator = identyfikator
        self._klient = klient
        self._stolik = stolik
        self._godzina = godzina

    def pobierz_stolik(self):
        return self._stolik

    def wyswietl_szczegoly(self):
        print(f"  -> Rezerwacja {self._identyfikator}: Stolik {self._stolik.pobierz_numer()} dla {self._klient.pobierz_imie()} na godzine {self._godzina}.")

class Restauracja:
    def __init__(self, nazwa):
        self._nazwa = nazwa
        self._stoliki = []
        self._rezerwacje = []

    def dodaj_stolik(self, stolik):
        self._stoliki.append(stolik)

    def stworz_rezerwacje(self, identyfikator_rezerwacji, klient, numer_stolika, godzina):
        wybrany_stolik = None
        for stolik in self._stoliki:
            if stolik.pobierz_numer() == numer_stolika:
                wybrany_stolik = stolik
                break

        if wybrany_stolik and wybrany_stolik.czy_jest_wolny():
            wybrany_stolik.zarezerwuj()
            nowa_rezerwacja = Rezerwacja(identyfikator_rezerwacji, klient, wybrany_stolik, godzina)
            self._rezerwacje.append(nowa_rezerwacja)
            return True
        return False

    def wyswietl_rezerwacje(self):
        print(f"\n--- Aktualne rezerwacje w restauracji {self._nazwa} ---")
        if not self._rezerwacje:
            print("  Brak aktywnych rezerwacji.")
        for rezerwacja in self._rezerwacje:
            rezerwacja.wyswietl_szczegoly()

    def wyswietl_stoliki(self):
        print(f"\n--- Stan stolikow ---")
        for stolik in self._stoliki:
            status = "WOLNY" if stolik.czy_jest_wolny() else "ZAJETY"
            print(f"  Stolik nr {stolik.pobierz_numer()} (Miejsca: {stolik._liczba_miejsc}) - Status: {status}")


if __name__ == "__main__":
    moja_restauracja = Restauracja("Smaczny Zakatek")

    moja_restauracja.dodaj_stolik(Stolik(1, 4))
    moja_restauracja.dodaj_stolik(Stolik(2, 2))
    moja_restauracja.dodaj_stolik(Stolik(3, 6))

    licznik_rezerwacji = 1

    while True:
        print("\n==============================")
        print("  SYSTEM RESTAURACJI - MENU")
        print("==============================")
        print("1. Pokaz stan stolikow")
        print("2. Dodaj nowa rezerwacje")
        print("3. Pokaz wszystkie rezerwacje")
        print("4. Rozlicz płatność")
        print("5. Wyjdz z programu")
        
        wybor = input("Wybierz opcje (1-5): ")

        if wybor == "1":
            moja_restauracja.wyswietl_stoliki()

        elif wybor == "2":
            print("\n--- KREATOR REZERWACJI ---")
            imie = input("Podaj imie i nazwisko klienta: ")
            telefon = input("Podaj telefon: ")
            
            moja_restauracja.wyswietl_stoliki()
            try:
                nr_stolika = int(input("Wybierz numer stolika: "))
                godzina = input("Podaj godzine (np. 18:00): ")
                
                klient = Klient(f"K{licznik_rezerwacji}", imie, telefon)
                id_rez = f"R{licznik_rezerwacji}"
                
                if moja_restauracja.stworz_rezerwacje(id_rez, klient, nr_stolika, godzina):
                    print(f"\n[SUKCES] Zapisano rezerwacje o ID: {id_rez}!")
                    licznik_rezerwacji += 1
                else:
                    print("\n[BŁĄD] Ten stolik jest juz zajety lub nie istnieje!")
            except ValueError:
                print("\n[BŁĄD] Numer stolika musi byc liczba!")

        elif wybor == "3":
            moja_restauracja.wyswietl_rezerwacje()

        elif wybor == "4":
            print("\n--- SYMULATOR PŁATNOŚCI (POLIMORFIZM) ---")
            try:
                kwota = float(input("Podaj kwota do zaplaty (np. 120.50): "))
                print("Wybierz forme platnosci:")
                print("1. Karta")
                print("2. Gotowka")
                typ_platnosci = input("Wybor: ")
                
                if typ_platnosci == "1":
                    nr_karty = input("Podaj numer karty: ")
                    transakcja = PlatnoscKarta(f"P{licznik_rezerwacji}", kwota, nr_karty)
                elif typ_platnosci == "2":
                    transakcja = PlatnoscGotowka(f"P{licznik_rezerwacji}", kwota)
                else:
                    print("Niepoprawny wybor płatnosci.")
                    continue
                
                print()
                transakcja.realizuj()
            except ValueError:
                print("\n[BŁĄD] Wprowadzono niepoprawna kwote!")

        elif wybor == "5":
            print("\nZamykanie systemu. Do widzenia!")
            break
        else:
            print("\nNiepoprawna opcja! Wybierz cyfre od 1 do 5.")