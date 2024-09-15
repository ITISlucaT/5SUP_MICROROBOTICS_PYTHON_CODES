#Per la programmazione in python fate dei programmini per caricare o salvare liste in o da file CSV, dei
#menu da poter impiegare al bisogno e la parte di interfaccia grafica.
import tkinter as tk
from tkinter import ttk, filedialog
import csv
from PIL import Image, ImageTk

def open_csv_file():
    global csv_file_path
    file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
    if file_path:
        csv_file_path = file_path
        display_csv_data(file_path)

def display_csv_data(file_path):
    try:
        with open(file_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            tree.delete(*tree.get_children()) 

            tree["columns"] = header
            for col in header:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            for row in csv_reader:
                tree.insert("", "end", values=row)

            status_label.config(text=f"CSV file loaded: {file_path}")
            save_button.pack()


    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")

def modify_cell(event):
    # Ottieni l'elemento selezionato e la colonna
    selected_item = tree.selection()
    if selected_item:
        item_id = selected_item[0]
        column = tree.identify_column(event.x)
        column_index = int(column.replace('#', '')) - 1
        x, y, width, height = tree.bbox(item_id, column)

        #TOR Ottieni il valore della cella
        cell_value = tree.item(item_id, 'values')[column_index]

        # TOR Crea un campo di input sopra la cella
        entry = tk.Entry(root)
        entry.place(x=x+tree.winfo_x(), y=y+tree.winfo_y(), width=width, height=height)
        entry.insert(0, cell_value)

        def save_edit(event):
            new_value = entry.get()
            current_values = list(tree.item(item_id, 'values'))
            current_values[column_index] = new_value
            tree.item(item_id, values=current_values)
            entry.destroy()  # Rimuovi l'input dopo l'editing

        # TOR Lega l'evento Invio alla chiusura dell'input e al salvataggio del valore
        entry.bind('<Return>', save_edit)

def display_open_CSV_page():
    hide_all_frames()
    open_button.pack(padx=20, pady=10)
    tree.pack(padx=20, pady=20, fill="both", expand=True)
    status_label.pack()
    home_button.pack(pady=10)
    

def display_home_page():
    hide_all_frames()
    home_label.pack(pady=50)
    status_label.pack_forget()
    home_image_label.pack()

def hide_all_frames():
    """Nasconde tutti i widget della finestra."""
    for widget in root.winfo_children():
        widget.pack_forget()

def get_treeview_data():
    """Estrae i dati della Treeview e li restituisce sotto forma di lista di liste."""
    data = []
    # Ottieni l'intestazione (nomi delle colonne)
    columns = tree["columns"]
    data.append(columns)  

    for row_id in tree.get_children():
        row_values = tree.item(row_id, "values")
        data.append(list(row_values))  
    
    return data

def save_CSV():
    global csv_file_path
    datas = get_treeview_data()
    print(csv_file_path)
    if csv_file_path:
        try:
            with open(csv_file_path, 'w', newline='') as f:
                csv_writer = csv.writer(f)
                for row in datas:
                    csv_writer.writerow(row)
                status_label.config(text=f"File salvato correttamente.")
        except Exception as e:
            status_label.config(text=f"Errore durante il salvataggio {str(e)}")
    else:
        status_label.config(text=f"Nessun file aperto")

csv_file_path = None

root = tk.Tk()
root.title("Criminal Information")
root.geometry("800x600")


menubar = tk.Menu(root)


filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Apri CSV", command=display_open_CSV_page)
filemenu.add_command(label="Esci", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


root.config(menu=menubar)

img = Image.open("fbi.png") 
img = img.resize((400, 401))  
img_tk = ImageTk.PhotoImage(img)


home_label = tk.Label(root, text="Anagrafica criminali", font=("Arial", 24))


home_image_label = tk.Label(root, image=img_tk) 


open_button = tk.Button(root, text="Open CSV File", command=open_csv_file)
save_button = tk.Button(root, text="Salva", command=save_CSV)
home_button = tk.Button(root, text="Torna alla Home", command=display_home_page)
tree = ttk.Treeview(root, show="headings")
status_label = tk.Label(root, text="", padx=20, pady=10)

# TOR Lega l'evento di doppio clic alla modifica della cella
tree.bind('<Double-1>', modify_cell)


home_label = tk.Label(root, text="Anagrafe criminali", font=("Arial", 24))

display_home_page()

root.mainloop()
