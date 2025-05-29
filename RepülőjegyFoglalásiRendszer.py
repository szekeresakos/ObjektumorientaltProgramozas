from abc import ABC, abstractmethod

class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar

    @abstractmethod
    def jarat_tipus(self):
        pass

class BelfoldiJarat(Jarat):
    def jarat_tipus(self):
        return "Belföldi"

class NemzetkoziJarat(Jarat):
    def jarat_tipus(self):
        return "Nemzetközi"

class JegyFoglalas:
    def __init__(self, utas_nev, jarat):
        self.utas_nev = utas_nev
        self.jarat = jarat

class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []
        self.foglalasok = []

    def jarat_hozzaadasa(self, jarat):
        self.jaratok.append(jarat)

    def listaz_jaratok(self):
        if not self.jaratok:
            print("Nincs elérhető járat.")
        else:
            print("Elérhető járatok:")
            for jarat in self.jaratok:
                print(f"{jarat.jaratszam} - {jarat.celallomas} ({jarat.jarat_tipus()}, {jarat.jegyar} Ft)")

    def jegyet_foglal(self, utas_nev, jaratszam):
        jarat = self.keres_jarat(jaratszam)
        if jarat:
            foglalas = JegyFoglalas(utas_nev, jarat)
            self.foglalasok.append(foglalas)
            print(f"Sikeres foglalás! Ár: {jarat.jegyar} Ft")
        else:
            print("Nincs ilyen járat!")

    def foglalas_lemondasa(self, utas_nev, jaratszam):
        for foglalas in self.foglalasok:
            if foglalas.utas_nev == utas_nev and foglalas.jarat.jaratszam == jaratszam:
                self.foglalasok.remove(foglalas)
                print("Foglalás lemondva.")
                return
        print("Nem található ilyen foglalás!")

    def listaz_foglalasok(self):
        if not self.foglalasok:
            print("Nincs aktív foglalás.")
        else:
            print("Aktív foglalások:")
            for foglalas in self.foglalasok:
                print(f"{foglalas.utas_nev} - {foglalas.jarat.jaratszam} ({foglalas.jarat.celallomas})")

    def keres_jarat(self, jaratszam):
        for jarat in self.jaratok:
            if jarat.jaratszam == jaratszam:
                return jarat
        return None

legitarsasag = LegiTarsasag("MALÉV")
legitarsasag.jarat_hozzaadasa(BelfoldiJarat("MA645", "Debrecen", 15000))
legitarsasag.jarat_hozzaadasa(NemzetkoziJarat("MA702", "Tokyo", 120000))
legitarsasag.jarat_hozzaadasa(NemzetkoziJarat("MA471", "London", 55000))

legitarsasag.jegyet_foglal("Pap Milán", "MA645")
legitarsasag.jegyet_foglal("Nagy Ágnes", "MA702")
legitarsasag.jegyet_foglal("Kovács Dóra", "MA645")
legitarsasag.jegyet_foglal("Szabó Gábor", "MA471")
legitarsasag.jegyet_foglal("Vitek Zsolt", "MA702")
legitarsasag.jegyet_foglal("Tóth Szilvia", "MA471")

def menu():
    while True:
        print(f"\n--- {legitarsasag.nev} Repülőjegy Foglalási Rendszer ---")
        print("1. Jegy foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        valasztas = input("Válassz egy műveletet: ")

        if valasztas == "1":
            legitarsasag.listaz_jaratok()
            nev = input("Add meg a neved: ")
            jarat = input("Add meg a járatszámot: ").upper()
            legitarsasag.jegyet_foglal(nev, jarat)
        elif valasztas == "2":
            nev = input("Add meg a neved: ")
            jarat = input("Add meg a járatszámot: ").upper()
            legitarsasag.foglalas_lemondasa(nev, jarat)
        elif valasztas == "3":
            legitarsasag.listaz_foglalasok()
        elif valasztas == "4":
            print("Kilépés...")
            break
        else:
            print("Érvénytelen választás.")

menu()
