import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from genetisch_algoritme import *
from functools import partial

entries = {}


def place_logo(event):
    """Plaatst het logo in het midden van het venster"""
    logo_x = (root.winfo_width() - logo_img.width) // 2
    logo_y = (root.winfo_height() - logo_img.height) // 2
    logo_label.place(x=logo_x, y=logo_y)


def new_window():
    """Opent een nieuw venster voor het invoeren van medewerkers per dag"""
    root.withdraw()  # Verberg het huidige venster
    root2 = tk.Toplevel()  # Maak een nieuw venster
    root2.geometry('1000x1000')
    root2.title('rooster A1')

    label_text = Label(root2, text='Selecteer het aantal medewerkers per dag', fg='grey', font=('Arial', 25))
    label_text.place(relx=0.5, rely=0.1, anchor='center')

    dagen = ['Maandag', 'Dinsdag', 'Woensdag', 'Donderdag', 'Vrijdag', 'Zaterdag', 'Zondag']
    y_offset = 0.2

    for i, dag in enumerate(dagen, start=1):
        label = Label(root2, text=dag, fg='grey', font=('Arial', 25))
        label.place(relx=0.1, rely=y_offset, anchor='center')

        entry = Entry(root2, width=20)
        entry.place(relx=0.4, rely=y_offset, anchor=CENTER)

        entries[dag] = entry

        y_offset += 0.1

    opslaan_button = Button(root2, text='Opslaan', command=partial(opslaan, dagen, entries))
    opslaan_button.place(relx=0.5, rely=0.9, anchor='center')

    show_rooster = Button(root2, text='Show rooster', command=rooster_window)
    show_rooster.place(relx=0.7, rely=0.9, anchor='center')


def opslaan(dagen, entries):
    """Haalt het aantal medewerkers per dag op uit de invoervelden"""
    medewerkers_per_dag = {}
    for i, dag in enumerate(dagen, start=1):
        if dag in entries:
            entry = entries[dag]
            value = entry.get()
            if value == '' or value is None:
                value = 0
            medewerkers_per_dag[i] = int(value)
    print(medewerkers_per_dag)
    return medewerkers_per_dag


def rooster_window(beste_individu, dagen):
    """Toont het rooster in een nieuw venster"""
    root.withdraw()  # Verberg het huidige venster
    root3 = tk.Toplevel()  # Maak een nieuw venster
    root3.geometry('1000x1000')  # Formaat instellen voordat mainloop() wordt aangeroepen
    root3.title('rooster A1')

    # Maak een Treeview-widget
    tree = ttk.Treeview(root3)

    # Definieer de kolommen van de tabel
    tree["columns"] = ("day", "employees")

    # Opmaak van de kolommen
    tree.column("#0", width=0, stretch=tk.NO)  # Verberg de eerste kolom
    tree.column("day", width=300)
    tree.column("employees", width=500, stretch=tk.YES)

    # Koppen van de kolommen
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("day", text="Dag", anchor=tk.W)
    tree.heading("employees", text="Medewerkers", anchor=tk.W)

    # Voeg data toe aan de tabel
    for i, row in enumerate(maak_rooster(beste_individu), start=1):
        day = row[0]
        employees = ", ".join(row[1:])
        tree.insert(parent="", index="end", iid=i, text="", values=(day, employees))

    # Plaats de Treeview-widget
    tree.pack()

    root3.mainloop()


root = tk.Tk()
root.geometry('1000x1000')
root.title('Welkom bij Restaurant A1')

# Achtergrondafbeelding
background_img = Image.open('achtergrond.png')
background_photo = ImageTk.PhotoImage(background_img)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Logo-afbeelding
logo_img = Image.open('logo.png')
logo_photo = ImageTk.PhotoImage(logo_img)
logo_label = tk.Label(root, image=logo_photo)

# Tekst toevoegen
label_text = Label(root, text='Welkom bij Restaurant A1', bg='orange', fg='white', font=('Arial', 50))
label_text.place(relx=0.5, rely=0.3, anchor='center')

root.bind("<Configure>", place_logo)  # Koppel de functie aan het "<Configure>"-event

rooster_knop = Button(root, command=new_window, text='Naar rooster', fg='deep sky blue')
rooster_knop.place(relx=0.5, rely=0.7, anchor='center')

root.mainloop()
