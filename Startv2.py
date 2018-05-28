
import os.path   # moduł udostępniający funkcję isfile()

plikestymacje = "estymacje.txt"   # plik z estymacjami i wydajnoscia lini
pliksap = "sap.txt"  # plik ze stanami wyeksporotwane z sapa
dodruku = "drukuj.txt"  # plik wyjsciowy po przetworzeniu


def jednaliniadruku(indeks, stan, esty, dorobic, potrzebah):
    # liczba znaków na kolejne pozycje w tabeli
    i = 12  # indeks
    z = 10  # zapas
    p = 17  # produkcje
    w = 10  # zapas w dniach
    k = 26  # konieczność produkcji
    linia = ""
    if indeks == "LINIA":
        linia = "\n" + ("LINIA  P" + str(stan)).center(75) + "\n" + "\n"
        linia += "|"
        linia += "Indeks:".center(i) + "|"
        linia += "Zapas:".center(z) + "|"
        linia += "Produkcja:(h)".center(p) + "|"
        linia += "Na Dni:".center(w) + "|"
        linia += "Konieczność Produkcji:".center(k) + "|"
        linia += "\n"
    else:
        dni = wystarczyna(esty, stan)
        linia = "| "
        linia += indeks.ljust(i-1)
        linia += "|" + str(stan).center(z)
        linia += "|" + (str(dorobic) + "(" + str(potrzebah) + "h)").rjust(p-2) + "  |"
        linia += str(round((stan / esty * 7), 1)).center(w) + "|"
        linia += prioryted(dni).center(k) + "|"
        linia += "\n"
    linia += ( i + z + p + w + k + 6 ) * "-"
    return linia


def prioryted(dni):
    linia = ""
    x = "*"
    if dni < 0:
        x += "!"
    for i in range(int(dni), 7):
        linia += x
    return linia



# tutaj ustawiamy kolejnośc wyświetlania, taka jak jest w pliku estymacje
def sort():
    sfile = plikestymacje  # nazwa pliku z estymecjami
    kolejnosc = []
    if os.path.isfile(sfile):  # czy istnieje plik słownika?
        with open(sfile, "r") as sTxt:  # otwórz plik do odczytu
            for line in sTxt:  # przeglądamy kolejne linie
                t = line.split(" ")  # rozbijamy linię kolumny
                indeks = str(t[1]).replace(" ", "").replace("\n", "")
                kolejnosc.append(indeks.upper())
    else:
        print("Nie ma pliku")
    return kolejnosc


def wydajnosc():
    sfile = plikestymacje  # nazwa pliku z estymecjami
    slownik = {}
    if os.path.isfile(sfile):  # czy istnieje plik słownika?
        with open(sfile, "r") as sTxt:  # otwórz plik do odczytu
            for line in sTxt:  # przeglądamy kolejne linie
                t = line.split(" ")  # rozbijamy linię kolumny
                indeks = str(t[1]).upper()
                estymacja = float(t[0].replace("\n", ""))
                slownik[indeks] = estymacja  # dodajemy do słownika indeks + estymacje
    else:
        print("Nie ma pliku")
    return slownik


def odczytajestymacje():
    sfile = plikestymacje  # nazwa pliku z estymecjami
    slownik = {}
    if os.path.isfile(sfile):  # czy istnieje plik słownika?
        with open(sfile, "r") as sTxt:  # otwórz plik do odczytu
            for line in sTxt:  # przeglądamy kolejne linie
                t = line.split(" ")  # rozbijamy linię kolumny
                indeks = str(t[1]).upper()
                estymacja = float(t[2].replace("\n", ""))
                slownik[indeks] = estymacja  # dodajemy do słownika indeks + estymacje
    else:
        print("Nie ma pliku")
    return slownik


# musze dodac ignorowanie pierwszej lini wejsciowej i zapis stanow z sap do pliku
def odczytajstany():
    sfile = pliksap  # nazwa pliku z estymecjami
    slownik = {}
    t = ""
    if os.path.isfile(sfile):  # czy istnieje plik słownika?
        with open(sfile, "r", encoding='CP1250') as sTxt:  # otwórz plik do odczytu
            for i, line in enumerate(sTxt):  # type: (int, object) # przeglądamy kolejne linie
                if i < 6:
                    t = line  # ignorujemy pierwsze 6 lini tekstu
                elif '|' in line:
                    t = line.split("|")  # rozbijamy linię kolumny
                    indeks = str(t[3]).replace("\n", "").upper().strip()
                    stan = float(t[9].replace("\n", "").strip().replace(",", ".")) \
                           + float(t[6].strip().replace(",", ".")) - float(t[5].strip().replace(",", "."))
                    # tu musimy odczytac to co zliczam na stanach
                    if indeks in slownik:
                        slownik[indeks] = slownik[indeks] + round(stan, 1)
                    else:
                        slownik[indeks] = round(stan, 1)  # dodajemy do słownika indeks + estymacje
    else:
        print("Nie ma pliku")
    return slownik


def wystarczyna(estymacja, stan):
    tydzien = stan / estymacja * 7
    return round(tydzien, 1)


def zapisz(kolejka, stan, esty, wydajnosc):
    sFile = dodruku
    file1 = open(sFile, "w")  # otwieramy plik do zapisu, istniejący plik zostanie nadpisany(!)
    linia = ""
    sumagodzin = 0
    for indeks in kolejka:
        if indeks[0:5] == "LINIA":
            if sumagodzin != 0:
                file1.write("Linia musi pracować przez: " + str(round(sumagodzin, 1)) + "h" + "\n")
            linia = jednaliniadruku(indeks[0:5], int(esty[indeks]), 0, 0, 0)
            sumagodzin = 0
        else:
            if indeks in stan:
                jest = stan[indeks]
            else:
                jest = 0
            dorobic = round(esty[indeks] - jest, 1)
            potrzebah = round(dorobic / wydajnosc[indeks] * 8, 1)
            sumagodzin += potrzebah
            linia = jednaliniadruku(indeks, jest, esty[indeks], dorobic, potrzebah)
        file1.write(linia)
        file1.write("\n")
    file1.write("Linia musi pracować przez: " + str(round(sumagodzin, 1)) + "h" + "\n")
    file1.close()  #zamykamy plik


def obciazenie(kolejka, esty, wydajnosc):
    sFile = "moceprzerobowe.txt"
    file1 = open(sFile, "w")  # otwieramy plik do zapisu, istniejący plik zostanie nadpisany(!)
    sumagodzin = 0
    linia = ""
    nrlini = "4"
    for indeks in kolejka:
        if indeks[0:5] == "LINIA":
                if sumagodzin != 0:
                    file1.write("Linia P" + nrlini
                            + " musi pracować przez: "
                            + str(round(sumagodzin, 1))
                            + "h (" + str(round(sumagodzin/24, 1))
                            + "d) w tygodniu" "\n\n")
                sumagodzin = 0
                nrlini = str(int(esty[indeks]))
        else:
            tygodniowapracalini = esty[indeks] / wydajnosc[indeks] * 8
            sumagodzin += tygodniowapracalini
            linia = "Powinniśmy produkować:  " + indeks.ljust(10) +": " \
                    + str(round(tygodniowapracalini, 1)) + "h(" \
                    + str(round(tygodniowapracalini/24, 1)) + "d)""\n"
            file1.write(linia)
    file1.write("Linia P" + nrlini
                + " musi pracować przez: "
                + str(round(sumagodzin, 1))
                + "h (" + str(round(sumagodzin / 24, 1))
                + "d) w tygodniu." "\n\n")
    file1.close()  # zamykamy plik



estymacjeslownik = odczytajestymacje()
stanslownik = odczytajstany()
wydajnosc = wydajnosc()
lista = sort()
obciazenie(lista, estymacjeslownik, wydajnosc)
zapisz(lista, stanslownik, estymacjeslownik, wydajnosc)
