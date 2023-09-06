import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import jinja2
import random
import datetime

class StationDataEditor:
    def __init__(self, roots):
        self.root = roots
        self.root.title("Edytor Rozkładu")

        self.data = []

        todaytemp = datetime.datetime.today()
        dzienzarzadzenietemp = random.randint(2, 31)
        miesaczarzadzenietemp = random.randint(2, 12)

        self.numer_pociagus = tk.StringVar()
        self.rodzaj_pociagus = tk.StringVar()
        self.przewoznik = tk.StringVar()
        self.numer_wniosku = tk.StringVar(value=f"BBPR2h-{random.randint(10, 999)}")
        self.numer_zarzadzenia = tk.StringVar(value=f"ZPRRJ_{todaytemp.year}_{random.randint(1000, 999999)}")
        self.data_wniosku = tk.StringVar(value=f"{dzienzarzadzenietemp - 2}.{miesaczarzadzenietemp - 1}.{todaytemp.year - 1}")
        self.data_zarzadzenia = tk.StringVar(value=f"{dzienzarzadzenietemp}.{miesaczarzadzenietemp}.{todaytemp.year - 1}")
        self.data_generowania = tk.StringVar(value=f"{todaytemp.day}.{todaytemp.month}.{todaytemp.year}")
        self.godzina_generowania = tk.StringVar(value=f"{todaytemp.hour}:{todaytemp.minute}:{todaytemp.second}")
        self.vmax = tk.StringVar(value="120")

        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack()

        # Rodzaj pociągu
        tk.Label(self.root, text="Rodzaj pociągu:").pack()
        rodzaj_pociagu = tk.Entry(self.root, textvariable=self.rodzaj_pociagus)
        rodzaj_pociagu.pack()

        # Nr pociągu
        tk.Label(self.root, text="Nr pociągu:").pack()
        nr_numer_pociagu = tk.Entry(self.root, textvariable=self.numer_pociagus)
        nr_numer_pociagu.pack()

        # Przewoźnik
        tk.Label(self.root, text="Przewoźnik:").pack()
        przewoznik = tk.Entry(self.root, textvariable=self.przewoznik)
        przewoznik.pack()

        # vmax
        tk.Label(self.root, text="V-max:").pack()
        vmaxi = tk.Entry(self.root, textvariable=self.vmax)
        vmaxi.pack()

        self.add_button = tk.Button(
            self.root, text="Dodaj Stację", command=self.add_station
        )
        self.add_button.pack()

        self.generate_button = tk.Button(
            self.root, text="Generuj HTML", command=self.generate_html
        )
        self.generate_button.pack()

    def add_station(self):
        station_window = tk.Toplevel(self.root)
        station_window.title("Dodaj Stację")

        try:
            tempdata = self.data[-1]
        except IndexError:
            tempdata = {"nr_linii": "0", "km": "", "wja-v": "", "wyj-v": "", "lokomotywa":"EP08"}

        tk.Label(station_window, text="Nr linii:").pack()
        nr_linii_entry = tk.Entry(station_window)
        nr_linii_entry.insert(0, tempdata["nr_linii"])
        nr_linii_entry.pack()

        tk.Label(station_window, text="Km:").pack()
        km_entry = tk.Entry(station_window)
        km_entry.insert(0, tempdata["km"])
        km_entry.pack()

        tk.Label(station_window, text="Wjazd V:").pack()
        v_entry = tk.Entry(station_window)
        v_entry.insert(0, tempdata["wja-v"])
        v_entry.pack()

        tk.Label(station_window, text="Wyjazd V:").pack()
        v_entry2 = tk.Entry(station_window)
        v_entry2.insert(0, tempdata["wyj-v"])
        v_entry2.pack()

        tk.Label(station_window, text="Rodzaj miejsca postoju:").pack()
        rodzajstacji_format = tk.StringVar(root)
        rodzajstacji_formaty = ttk.Combobox(
            master=station_window,
            textvariable=rodzajstacji_format,
            values=["Stacja", "po.", "podg."]
        )
        rodzajstacji_formaty.current(0)
        rodzajstacji_formaty.pack()

        tk.Label(station_window, text="Nazwa miejsca postoju:").pack()
        stacja_entry = tk.Entry(station_window)
        stacja_entry.pack()

        tk.Label(station_window, text="Rodzaj postoju:").pack()
        rodzajpostoju_format = tk.StringVar(root)
        rodzajpostoju_formaty = ttk.Combobox(
            master=station_window,
            textvariable=rodzajpostoju_format,
            values=["BRAK", "ph", "pt", "pm"]
        )
        rodzajpostoju_formaty.current(0)
        rodzajpostoju_formaty.pack()
        
        tk.Label(station_window, text="Lokomotywa:").pack()
        # Sprawdzanie czy lokomotywa się zmieniła
        lokomotywa_entry = tk.Entry(station_window)
        if tempdata["lokomotywa"] == "EP08":
            lokomotywa_entry.insert(0, "EP08")
        lokomotywa_entry.pack()

        # Długość składu
        tk.Label(station_window, text="Długość składu:").pack()
        dlugosc_skladu_entry = tk.Entry(station_window)
        dlugosc_skladu_entry.pack()

        # Obciążenie składu
        tk.Label(station_window, text="Obciążenie składu:").pack()
        obciazenie_skladu_entry = tk.Entry(station_window)
        obciazenie_skladu_entry.pack()
        
        tk.Label(station_window, text="Godzina przyjazdu:").pack()
        godzinain_entry = tk.Entry(station_window)
        godzinain_entry.pack()

        tk.Label(station_window, text="Godzina odjazdu:").pack()
        godzinaout_entry = tk.Entry(station_window)
        godzinaout_entry.pack()

        tk.Label(station_window, text="Formatowanie stacji:").pack()
        stacja_format = tk.StringVar(root)
        stacja_formaty = ttk.Combobox(
            master=station_window,
            textvariable=stacja_format,
            values=["Normalna", "Początkowa", "Końcowa"]
        )
        stacja_formaty.current(1)
        stacja_formaty.pack()

        tk.Button(
            station_window,
            text="Dodaj",
            command=lambda:
            self.save_station(
                nr_linii_entry.get(),
                km_entry.get(),
                v_entry.get (),
                v_entry2.get(),
                rodzajstacji_format.get(),
                stacja_entry.get(),
                rodzajpostoju_format.get(),
                lokomotywa_entry.get(),
                dlugosc_skladu_entry.get(),
                obciazenie_skladu_entry.get(),
                godzinain_entry.get(),
                godzinaout_entry.get(),
                stacja_format.get(),
            ),
        ).pack()

    def save_station(self, nr_linii, km, wja_v, wyj_v, rodzajstacji, stacja, rodzajpostoju, lokomotywa, dlugosc_skladu, obciazenie_skladu, godzinain, godzinaout, stacja_format):
        if stacja_format == "Normalna":
            if rodzajstacji == "po.":
                stacja = f"{stacja}, po."
            elif rodzajstacji == "podg.":
                stacja = f"{stacja}, podg."
            else:
                rodzajstacji = ""
                if godzinain == "":
                    godzinain = "|"
        
        if rodzajpostoju == "BRAK":
            rodzajpostoju = ""
            if stacja_format == "Normalna":
                godzinain = "|"
        else:
            rodzajpostoju = f"; {rodzajpostoju}"

        # Sprawdzanie czy coś się zmieniło żeby dostosować formatowanie

        zmiananrlinii = False
        zmianalokomotywy = False

        try:
            if nr_linii != self.data[-1]["nr_linii"]:
                zmiananrlinii = True
            if lokomotywa != self.data[-1]["lokomotywa"]:
                zmianalokomotywy = True
            if dlugosc_skladu != self.data[-1]["dlugosc_skladu"]:
                zmianalokomotywy = True
            if obciazenie_skladu != self.data[-1]["obciazenie_skladu"]:
                zmianalokomotywy = True
        except IndexError:
            pass

        self.data.append(
            {
                "nr_linii": nr_linii,
                "zmiananrlinii": zmiananrlinii,
                "km": km,
                "wja-v": wja_v,
                "wyj-v": wyj_v,
                "rodzajstacji": rodzajstacji,
                "stacja": stacja,
                "rodzajpostoju": rodzajpostoju,
                "lokomotywa": lokomotywa,
                "dlugosc_skladu": dlugosc_skladu,
                "obciazenie_skladu": obciazenie_skladu,
                "zmianalokomotywy": zmianalokomotywy,
                "godzinain": godzinain,
                "godzinaout": godzinaout,
                "stacja_format": stacja_format
            }
        )
        messagebox.showinfo("Sukces", "Stacja została dodana.")

    def generate_html(self):
        if not self.data:
            messagebox.showwarning("Uwaga", "Brak danych stacji do wygenerowania HTML.")
            return
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader, trim_blocks=True)
        TEMPLATE_FILE = "template1.html"
        template = templateEnv.get_template(TEMPLATE_FILE)
        generated_html = template.render(
            data=self.data,
            rodzaj_pociagu=self.rodzaj_pociagus.get(),
            numer_pociagu=self.numer_pociagus.get(),
            vmax = self.vmax.get(),
            relacja_start=self.data[0]["stacja"].split(",")[0],
            relacja_koniec=self.data[-1]["stacja"].split(",")[0]
        )

        with open("rozklad.html", "w", encoding="utf-8") as file:
            file.write(generated_html)
            file.close()

        TEMPLATE_FILE = "template2.html"
        template = templateEnv.get_template(TEMPLATE_FILE)
        generated_html = template.render(
            numer_pociagu=self.numer_pociagus.get(),
            przewoznik=self.przewoznik.get(),
            numer_wniosku=self.numer_wniosku.get(),
            numer_zarzadzenia=self.numer_zarzadzenia.get(),
            data_wniosku=self.data_wniosku.get(),
            data_zarzadzenia=self.data_zarzadzenia.get(),
            data_generowania=self.data_generowania.get(),
            godzina_generowania=self.godzina_generowania.get()
        )

        with open("okladka.html", "w", encoding="utf-8") as file:
            file.write(generated_html)
            file.close()

        messagebox.showinfo("Sukces", "Plik HTML został wygenerowany.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StationDataEditor(root)
    root.mainloop()
