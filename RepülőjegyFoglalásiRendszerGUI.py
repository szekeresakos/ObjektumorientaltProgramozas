import tkinter as tk
from tkinter import messagebox
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
        return ["   " f"{j.jaratszam} - {j.celallomas} ({j.jarat_tipus()}, {j.jegyar} Ft)" for j in self.jaratok]

    def jegyet_foglal(self, utas_nev, jaratszam):
        jarat = self.keres_jarat(jaratszam)
        if jarat:
            foglalas = JegyFoglalas(utas_nev, jarat)
            self.foglalasok.append(foglalas)
            return True, f"Foglalás sikeres! Ár: {jarat.jegyar} Ft"
        return False, "Nincs ilyen járat!"

    def foglalas_lemondasa(self, utas_nev, jaratszam):
        for f in self.foglalasok:
            if f.utas_nev == utas_nev and f.jarat.jaratszam == jaratszam:
                self.foglalasok.remove(f)
                return True, "Foglalás törölve."
        return False, "Foglalás nem található!"

    def listaz_foglalasok(self):
        return ["   " f"{f.utas_nev} - {f.jarat.jaratszam} ({f.jarat.celallomas})" for f in self.foglalasok]

    def keres_jarat(self, jaratszam):
        return next((j for j in self.jaratok if j.jaratszam == jaratszam), None)



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


### GUI
def foglalas_gui():
    nev = nev_entry.get().strip()
    jaratszam = jarat_entry.get().strip().upper()
    if not nev or not jaratszam:
        messagebox.showwarning("Hiba", "Kérlek, add meg a nevet és a járatszámot!")
        return
    siker, uzenet = legitarsasag.jegyet_foglal(nev, jaratszam)
    messagebox.showinfo("Foglalás", uzenet)
    frissit_foglalas_lista()
    nev_entry.delete(0, tk.END)
    jarat_entry.delete(0, tk.END)

def lemondas_gui():
    nev = nev_entry.get().strip()
    jaratszam = jarat_entry.get().strip().upper()
    if not nev or not jaratszam:
        messagebox.showwarning("Hiba", "Kérlek, add meg a nevet és a járatszámot!")
        return
    siker, uzenet = legitarsasag.foglalas_lemondasa(nev, jaratszam)
    messagebox.showinfo("Lemondás", uzenet)
    frissit_foglalas_lista()
    nev_entry.delete(0, tk.END)
    jarat_entry.delete(0, tk.END)

def frissit_jarat_lista():
    jaratok = legitarsasag.listaz_jaratok()
    jarat_lista.delete(0, tk.END)
    for j in jaratok:
        jarat_lista.insert(tk.END, j)

def frissit_foglalas_lista():
    foglalasok = legitarsasag.listaz_foglalasok()
    foglalas_lista.delete(0, tk.END)
    for f in foglalasok:
        foglalas_lista.insert(tk.END, f)


ablak = tk.Tk()
ablak.title("Repülőjegy Foglalási Rendszer")

tk.Label(ablak, text="Név:").grid(row=0, column=0, sticky="e")
nev_entry = tk.Entry(ablak)
nev_entry.grid(row=0, column=1)

tk.Label(ablak, text="Járatszám:").grid(row=1, column=0, sticky="e")
jarat_entry = tk.Entry(ablak)
jarat_entry.grid(row=1, column=1)

tk.Button(ablak, text="Jegy foglalása", command=foglalas_gui).grid(row=2, column=0, pady=5)
tk.Button(ablak, text="Foglalás lemondása", command=lemondas_gui).grid(row=2, column=1, pady=5)

tk.Label(ablak, text="Elérhető járatok:").grid(row=3, column=0, columnspan=2)
jarat_lista = tk.Listbox(ablak, width=55)
jarat_lista.grid(row=4, column=0, columnspan=2)
frissit_jarat_lista()

tk.Label(ablak, text="Foglalások:").grid(row=5, column=0, columnspan=2)
foglalas_lista = tk.Listbox(ablak, width=55)
foglalas_lista.grid(row=6, column=0, columnspan=2)
frissit_foglalas_lista()

ablak.mainloop()
