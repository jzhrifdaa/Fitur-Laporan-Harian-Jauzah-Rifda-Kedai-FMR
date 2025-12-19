import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import random
from datetime import date
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import tkinter.messagebox as messagebox
import json
import os

# folder history harian
HISTORY_FOLDER = "history"
os.makedirs(HISTORY_FOLDER, exist_ok=True)

# File untuk menyimpan menu
MENU_FILE = "menu.json"

# Fungsi untuk load menu dari file
def load_menu():
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, 'r') as f:
            return json.load(f)
    else:
        # Default menu
        return {
            "Steak Ayam": 28000,
            "Nasi Goreng": 15000,
            "Ayam Goreng": 18000,
            "Ayam Bakar": 22000,
            "Soto Ayam": 16000,
            "Rawon": 27000,
            "Mendoan": 10000,
            "Tahu Isi": 10000,
            "Risol": 12000,
            "Lumpia": 12000,
            "Es Teh": 5000,
            "Es Jeruk": 6000,
            "Lemon Tea": 6000,
            "Es Coklat": 10000,
        }

# Fungsi untuk save menu ke file
def save_menu(menu):
    with open(MENU_FILE, 'w') as f:
        json.dump(menu, f)

prices = load_menu()

# Fungsi untuk membuat PDF struk
def generate_pdf(order_id, transaction_list, total, order_day, order_time):
    filename = f"{order_id}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Header
    story.append(Paragraph("Kedai FMR", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("__________________________________________", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Order ID: {order_id}", styles['Normal']))
    story.append(Paragraph(f"Date: {order_day.strftime('%x')}", styles['Normal']))
    story.append(Paragraph(f"Time: {order_time.strftime('%X')}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Items
    for item in transaction_list:
        story.append(Paragraph(item, styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(total, styles['Normal']))
    
    doc.build(story)
    messagebox.showinfo("Success", f"Receipt saved as {filename}")

# Fungsi History
def save_order_history(order_id, items, total, order_day, order_time):
    filename = os.path.join(HISTORY_FOLDER, f"history_{order_day}.json")
    
    order_data = {
        "order_id": order_id,
        "time": order_time.strftime("%H:%M:%S"),
        "items": items,
        "total": total
    }

    if os.path.exists(filename):
        with open(filename, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append(order_data)

    with open(filename, "w") as f:
        json.dump(history, f, indent=4)

# Tombol order
def generate_daily_report(order_day):
    filename = os.path.join(HISTORY_FOLDER, f"history_{order_day}.json")

    if not os.path.exists(filename):
        messagebox.showerror("Error", "No orders for today")
        return

    with open(filename, "r") as f:
        history = json.load(f)

    pdf_name = f"Laporan_{order_day}.pdf"
    doc = SimpleDocTemplate(pdf_name, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("LAPORAN HARIAN KEDAI FMR", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Tanggal: {order_day}", styles["Normal"]))
    story.append(Spacer(1, 12))

    grand_total = 0

    for order in history:
        story.append(Paragraph(f"Order ID: {order['order_id']} ({order['time']})", styles["Heading3"]))
        for item in order["items"]:
            story.append(Paragraph(item, styles["Normal"]))
        story.append(Paragraph(order["total"], styles["Normal"]))
        story.append(Spacer(1, 10))

        grand_total += int(order["total"].replace("TOTAL : Rp ", ""))

    story.append(Spacer(1, 12))
    story.append(Paragraph(f"TOTAL PENDAPATAN: Rp {grand_total}", styles["Heading2"]))

    doc.build(story)
    messagebox.showinfo("Success", f"Laporan harian disimpan sebagai {pdf_name}")

#order is when starting a new order
def ORDER_ID():
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    letters = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    order_id = "FMR_"
    random_letters = ""
    random_digits = ""
    for i in range(0, 3):
        random_letters += random.choice(letters)
        random_digits += str(random.choice(numbers))
    
    order_id += random_letters + random_digits
    return order_id

def main_app(is_admin=False):
    root = Tk()
    root.title("Kedai FMR")

    # Fungsi untuk reload menu (untuk update setelah edit admin)
    def reload_menu():
        global prices
        prices = load_menu()
        # Update labels harga di menu
        steak_ayamDishLabel.config(text=f"Steak Ayam ..... Rp {prices['Steak Ayam']:,}")
        nasi_gorengDishLabel.config(text=f"Nasi Goreng ..... Rp {prices['Nasi Goreng']:,}")
        ayam_gorengDishLabel.config(text=f"Ayam Goreng ..... Rp {prices['Ayam Goreng']:,}")
        ayam_bakarDishLabel.config(text=f"Ayam Bakar ..... Rp {prices['Ayam Bakar']:,}")
        sotoDishLabel.config(text=f"Soto Ayam ..... Rp {prices['Soto Ayam']:,}")
        rawonDishLabel.config(text=f"Rawon ..... Rp {prices['Rawon']:,}")
        mendoanDishLabel.config(text=f"Mendoan ..... Rp {prices['Mendoan']:,}")
        tahu_isiDishLabel.config(text=f"Tahu Isi ..... Rp {prices['Tahu Isi']:,}")
        risolDishLabel.config(text=f"Risol ..... Rp {prices['Risol']:,}")
        lumpiaDishLabel.config(text=f"Lumpia ..... Rp {prices['Lumpia']:,}")
        es_tehDishLabel.config(text=f"Es Teh ..... Rp {prices['Es Teh']:,}")
        es_jerukDishLabel.config(text=f"Es Jeruk ..... Rp {prices['Es Jeruk']:,}")
        lemon_teaDishLabel.config(text=f"Lemon Tea ..... Rp {prices['Lemon Tea']:,}")
        es_coklatDishLabel.config(text=f"Es Coklat ..... Rp {prices['Es Coklat']:,}")

    # Fungsi untuk jendela edit admin
    def admin_edit():
        edit_win = Toplevel(root)
        edit_win.title("Admin Edit Menu")
        edit_win.geometry("400x600")
        
        ttk.Label(edit_win, text="Edit Menu Items").pack(pady=10)
        
        entries = {}
        for item, price in prices.items():
            frame = ttk.Frame(edit_win)
            frame.pack(fill='x', padx=10, pady=2)
            ttk.Label(frame, text=item, width=15).pack(side='left')
            entry = ttk.Entry(frame)
            entry.insert(0, str(price))
            entry.pack(side='right')
            entries[item] = entry
        
        def save_changes():
            try:
                new_prices = {item: int(entry.get()) for item, entry in entries.items()}
                save_menu(new_prices)
                reload_menu()
                messagebox.showinfo("Success", "Menu updated successfully!")
                edit_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for prices.")
        
        ttk.Button(edit_win, text="Save Changes", command=save_changes).pack(pady=10)

    #region and to order button
    def add():
        current_order = orderTransaction.cget("text")
        added_dish = displayLabel.cget("text") + " Rp" + str(prices[displayLabel.cget("text")])
        if current_order:
            updated_order = current_order + "\n" + added_dish
        else:
            updated_order = added_dish
        orderTransaction.configure(text=updated_order)

        # updating the order total
        order_total = orderTotalLabel.cget("text").replace("TOTAL : ", "")
        order_total = order_total.replace("Rp ", "")
        update_total = int(order_total) + prices[displayLabel.cget("text")]
        orderTotalLabel.configure(text="TOTAL : Rp " + str(update_total))

    #region remove button function
    def remove():
        dish_to_remove = displayLabel.cget("text") + " Rp" + str(prices[displayLabel.cget("text")])
        current_order = orderTransaction.cget("text")
        transaction_list = current_order.split("\n") if current_order else []
        
        if dish_to_remove in transaction_list:
            transaction_list.remove(dish_to_remove)
            updated_order = "\n".join(transaction_list) if transaction_list else ""
            orderTransaction.configure(text=updated_order)
            
            # updating the order total
            order_total = orderTotalLabel.cget("text").replace("TOTAL : ", "").replace("Rp ", "")
            update_total = int(order_total) - prices[displayLabel.cget("text")]
            orderTotalLabel.configure(text="TOTAL : Rp " + str(update_total))

    #region display sections
    def displaysteak_ayam():
        steak_ayamDishframe.configure(relief="sunken", style="SelectedDish.TFrame")
        nasi_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_bakarDishframe.configure(style="DishFrame.TFrame")
        sotoDishframe.configure(style="DishFrame.TFrame")
        rawonDishframe.configure(style="DishFrame.TFrame")
        mendoanDishframe.configure(style="DishFrame.TFrame")
        tahu_isiDishframe.configure(style="DishFrame.TFrame")
        risolDishframe.configure(style="DishFrame.TFrame")
        lumpiaDishframe.configure(style="DishFrame.TFrame")
        es_tehDishframe.configure(style="DishFrame.TFrame")
        es_jerukDishframe.configure(style="DishFrame.TFrame")
        lemon_teaDishframe.configure(style="DishFrame.TFrame")
        es_coklatDishframe.configure(style="DishFrame.TFrame")
        
        displayLabel.configure(
            image=steak_ayamImage,
            text="Steak Ayam",
            font=('Helvetica', 14, "bold"),
            foreground="white",
            compound="bottom",
            padding=(5, 5, 5, 5),
        )

    def displaynasi_goreng():
        nasi_gorengDishframe.configure(relief="sunken", style="SelectedDish.TFrame")
        steak_ayamDishframe.configure(style="DishFrame.TFrame")
        ayam_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_bakarDishframe.configure(style="DishFrame.TFrame")
        sotoDishframe.configure(style="DishFrame.TFrame")
        rawonDishframe.configure(style="DishFrame.TFrame")
        mendoanDishframe.configure(style="DishFrame.TFrame")
        tahu_isiDishframe.configure(style="DishFrame.TFrame")
        risolDishframe.configure(style="DishFrame.TFrame")
        lumpiaDishframe.configure(style="DishFrame.TFrame")
        es_tehDishframe.configure(style="DishFrame.TFrame")
        es_jerukDishframe.configure(style="DishFrame.TFrame")
        lemon_teaDishframe.configure(style="DishFrame.TFrame")
        es_coklatDishframe.configure(style="DishFrame.TFrame")

        displayLabel.configure(
            image=nasi_gorengImage,
            text="Nasi Goreng",
            font=('Helvetica', 14, "bold"),
            foreground="white",
            compound="bottom",
            padding=(5, 5, 5, 5),
        )

    def displayayam_goreng():
        ayam_gorengDishframe.configure(relief="sunken", style="SelectedDish.TFrame")
        steak_ayamDishframe.configure(style="DishFrame.TFrame")
        nasi_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_bakarDishframe.configure(style="DishFrame.TFrame")
        sotoDishframe.configure(style="DishFrame.TFrame")
        rawonDishframe.configure(style="DishFrame.TFrame")
        mendoanDishframe.configure(style="DishFrame.TFrame")
        tahu_isiDishframe.configure(style="DishFrame.TFrame")
        risolDishframe.configure(style="DishFrame.TFrame")
        lumpiaDishframe.configure(style="DishFrame.TFrame")
        es_tehDishframe.configure(style="DishFrame.TFrame")
        es_jerukDishframe.configure(style="DishFrame.TFrame")
        lemon_teaDishframe.configure(style="DishFrame.TFrame")
        es_coklatDishframe.configure(style="DishFrame.TFrame")

        displayLabel.configure(
            image=ayam_gorengImage,
            text="Ayam Goreng",
            font=('Helvetica', 14, "bold"),
            foreground="white",
            compound="bottom",
            padding=(5, 5, 5, 5),
        )

    def displayayam_bakar():
        ayam_bakarDishframe.configure(relief="sunken", style="SelectedDish.TFrame")
        steak_ayamDishframe.configure(style="DishFrame.TFrame")
        nasi_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_gorengDishframe.configure(style="DishFrame.TFrame")
        sotoDishframe.configure(style="DishFrame.TFrame")
        rawonDishframe.configure(style="DishFrame.TFrame")
        mendoanDishframe.configure(style="DishFrame.TFrame")
        tahu_isiDishframe.configure(style="DishFrame.TFrame")
        risolDishframe.configure(style="DishFrame.TFrame")
        lumpiaDishframe.configure(style="DishFrame.TFrame")
        es_tehDishframe.configure(style="DishFrame.TFrame")
        es_jerukDishframe.configure(style="DishFrame.TFrame")
        lemon_teaDishframe.configure(style="DishFrame.TFrame")
        es_coklatDishframe.configure(style="DishFrame.TFrame")

        displayLabel.configure(
            image=ayam_bakarImage,
            text="Ayam Bakar",
            font=('Helvetica', 14, "bold"),
            foreground="white",
            compound="bottom",
            padding=(5, 5, 5, 5),
        )

    def displaysoto():
        sotoDishframe.configure(relief="sunken", style="SelectedDish.TFrame")
        steak_ayamDishframe.configure(style="DishFrame.TFrame")
        nasi_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_bakarDishframe.configure(style="DishFrame.TFrame")
        rawonDishframe.configure(style="DishFrame.TFrame")
        mendoanDishframe.configure(style="DishFrame.TFrame")
        tahu_isiDishframe.configure(style="DishFrame.TFrame")
        risolDishframe.configure(style="DishFrame.TFrame")
        lumpiaDishframe.configure(style="DishFrame.TFrame")
        es_tehDishframe.configure(style="DishFrame.TFrame")
        es_jerukDishframe.configure(style="DishFrame.TFrame")
        lemon_teaDishframe.configure(style="DishFrame.TFrame")
        es_coklatDishframe.configure(style="DishFrame.TFrame")

        displayLabel.configure(
            image=sotoImage,
            text="Soto Ayam",
            font=('Helvetica', 14, "bold"),
            foreground="white",
            compound="bottom",
            padding=(5, 5, 5, 5),
        )

    def displayrawon():
        rawonDishframe.configure(relief="sunken", style="SelectedDish.TFrame")
        steak_ayamDishframe.configure(style="DishFrame.TFrame")
        nasi_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_bakarDishframe.configure(style="DishFrame.TFrame")
        sotoDishframe.configure(style="DishFrame.TFrame")
        mendoanDishframe.configure(style="DishFrame.TFrame")
        tahu_isiDishframe.configure(style="DishFrame.TFrame")
        risolDishframe.configure(style="DishFrame.TFrame")
        lumpiaDishframe.configure(style="DishFrame.TFrame")
        es_tehDishframe.configure(style="DishFrame.TFrame")
        es_jerukDishframe.configure(style="DishFrame.TFrame")
        lemon_teaDishframe.configure(style="DishFrame.TFrame")
        es_coklatDishframe.configure(style="DishFrame.TFrame")

        displayLabel.configure(
            image=rawonImage,
            text="Rawon",
            font=('Helvetica', 14, "bold"),
            foreground="white",
            compound="bottom",
            padding=(5, 5, 5, 5),
        )

    def displaymendoan():
        mendoanDishframe.configure(relief="sunken", style="SelectedDish.TFrame")
        steak_ayamDishframe.configure(style="DishFrame.TFrame")
        nasi_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_bakarDishframe.configure(style="DishFrame.TFrame")
        sotoDishframe.configure(style="DishFrame.TFrame")
        rawonDishframe.configure(style="DishFrame.TFrame")
        tahu_isiDishframe.configure(style="DishFrame.TFrame")
        risolDishframe.configure(style="DishFrame.TFrame")
        lumpiaDishframe.configure(style="DishFrame.TFrame")
        es_tehDishframe.configure(style="DishFrame.TFrame")
        es_jerukDishframe.configure(style="DishFrame.TFrame")
        lemon_teaDishframe.configure(style="DishFrame.TFrame")
        es_coklatDishframe.configure(style="DishFrame.TFrame")

        displayLabel.configure(
            image=mendoanImage,
            text="Mendoan",
            font=('Helvetica', 14, "bold"),
            foreground="white",
            compound="bottom",
            padding=(5, 5, 5, 5),
        )

    def displaytahu_isi():
        tahu_isiDishframe.configure(relief="sunken", style="SelectedDish.TFrame")
        steak_ayamDishframe.configure(style="DishFrame.TFrame")
        nasi_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_bakarDishframe.configure(style="DishFrame.TFrame")
        sotoDishframe.configure(style="DishFrame.TFrame")
        rawonDishframe.configure(style="DishFrame.TFrame")
        mendoanDishframe.configure(style="DishFrame.TFrame")
        risolDishframe.configure(style="DishFrame.TFrame")
        lumpiaDishframe.configure(style="DishFrame.TFrame")
        es_tehDishframe.configure(style="DishFrame.TFrame")
        es_jerukDishframe.configure(style="DishFrame.TFrame")
        lemon_teaDishframe.configure(style="DishFrame.TFrame")
        es_coklatDishframe.configure(style="DishFrame.TFrame")
        
        displayLabel.configure(
            image=tahu_isiImage,
            text="Tahu Isi",
            font=('Helvetica', 14, "bold"),
            foreground="white",
            compound="bottom",
            padding=(5, 5, 5, 5),
        )

    def displayrisol():
        risolDishframe.configure(relief="sunken", style="SelectedDish.TFrame")
        steak_ayamDishframe.configure(style="DishFrame.TFrame")
        nasi_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_bakarDishframe.configure(style="DishFrame.TFrame")
        sotoDishframe.configure(style="DishFrame.TFrame")
        rawonDishframe.configure(style="DishFrame.TFrame")
        mendoanDishframe.configure(style="DishFrame.TFrame")
        tahu_isiDishframe.configure(style="DishFrame.TFrame")
        lumpiaDishframe.configure(style="DishFrame.TFrame")
        es_tehDishframe.configure(style="DishFrame.TFrame")
        es_jerukDishframe.configure(style="DishFrame.TFrame")
        lemon_teaDishframe.configure(style="DishFrame.TFrame")
        es_coklatDishframe.configure(style="DishFrame.TFrame")

        displayLabel.configure(
            image=risolImage,
            text="Risol",
            font=('Helvetica', 14, "bold"),
            foreground="white",
            compound="bottom",
            padding=(5, 5, 5, 5),
        )

    def displaylumpia():
        lumpiaDishframe.configure(relief="sunken", style="SelectedDish.TFrame")
        steak_ayamDishframe.configure(style="DishFrame.TFrame")
        nasi_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_bakarDishframe.configure(style="DishFrame.TFrame")
        sotoDishframe.configure(style="DishFrame.TFrame")
        rawonDishframe.configure(style="DishFrame.TFrame")
        mendoanDishframe.configure(style="DishFrame.TFrame")
        tahu_isiDishframe.configure(style="DishFrame.TFrame")
        risolDishframe.configure(style="DishFrame.TFrame")
        es_tehDishframe.configure(style="DishFrame.TFrame")
        es_jerukDishframe.configure(style="DishFrame.TFrame")
        lemon_teaDishframe.configure(style="DishFrame.TFrame")
        es_coklatDishframe.configure(style="DishFrame.TFrame")

        displayLabel.configure(
            image=lumpiaImage,
            text="Lumpia",
            font=('Helvetica', 14, "bold"),
            foreground="white",
            compound="bottom",
            padding=(5, 5, 5, 5),
        )

    def displayes_teh():
        es_tehDishframe.configure(relief="sunken", style="SelectedDish.TFrame")
        steak_ayamDishframe.configure(style="DishFrame.TFrame")
        nasi_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_bakarDishframe.configure(style="DishFrame.TFrame")
        sotoDishframe.configure(style="DishFrame.TFrame")
        rawonDishframe.configure(style="DishFrame.TFrame")
        mendoanDishframe.configure(style="DishFrame.TFrame")
        tahu_isiDishframe.configure(style="DishFrame.TFrame")
        risolDishframe.configure(style="DishFrame.TFrame")
        lumpiaDishframe.configure(style="DishFrame.TFrame")
        es_jerukDishframe.configure(style="DishFrame.TFrame")
        lemon_teaDishframe.configure(style="DishFrame.TFrame")
        es_coklatDishframe.configure(style="DishFrame.TFrame")

        displayLabel.configure(
            image=es_tehImage,
            text="Es Teh",
            font=('Helvetica', 14, "bold"),
            foreground="white",
            compound="bottom",
            padding=(5, 5, 5, 5),
        )

    def displayes_jeruk():
        es_jerukDishframe.configure(relief="sunken", style="SelectedDish.TFrame")
        steak_ayamDishframe.configure(style="DishFrame.TFrame")
        nasi_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_bakarDishframe.configure(style="DishFrame.TFrame")
        sotoDishframe.configure(style="DishFrame.TFrame")
        rawonDishframe.configure(style="DishFrame.TFrame")
        mendoanDishframe.configure(style="DishFrame.TFrame")
        tahu_isiDishframe.configure(style="DishFrame.TFrame")
        risolDishframe.configure(style="DishFrame.TFrame")
        lumpiaDishframe.configure(style="DishFrame.TFrame")
        es_tehDishframe.configure(style="DishFrame.TFrame")
        lemon_teaDishframe.configure(style="DishFrame.TFrame")
        es_coklatDishframe.configure(style="DishFrame.TFrame")

        displayLabel.configure(
            image=es_jerukImage,
            text="Es Jeruk",
            font=('Helvetica', 14, "bold"),
            foreground="white",
            compound="bottom",
            padding=(5, 5, 5, 5),
        )

    def displaylemon_tea():
        lemon_teaDishframe.configure(relief="sunken", style="SelectedDish.TFrame")
        steak_ayamDishframe.configure(style="DishFrame.TFrame")
        nasi_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_bakarDishframe.configure(style="DishFrame.TFrame")
        sotoDishframe.configure(style="DishFrame.TFrame")
        rawonDishframe.configure(style="DishFrame.TFrame")
        mendoanDishframe.configure(style="DishFrame.TFrame")
        tahu_isiDishframe.configure(style="DishFrame.TFrame")
        risolDishframe.configure(style="DishFrame.TFrame")
        lumpiaDishframe.configure(style="DishFrame.TFrame")
        es_tehDishframe.configure(style="DishFrame.TFrame")
        es_jerukDishframe.configure(style="DishFrame.TFrame")
        es_coklatDishframe.configure(style="DishFrame.TFrame")

        displayLabel.configure(
            image=lemon_teaImage,
            text="Lemon Tea",
            font=('Helvetica', 14, "bold"),
            foreground="white",
            compound="bottom",
            padding=(5, 5, 5, 5),
        )

    def displayes_coklat():
        es_coklatDishframe.configure(relief="sunken", style="SelectedDish.TFrame")
        steak_ayamDishframe.configure(style="DishFrame.TFrame")
        nasi_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_gorengDishframe.configure(style="DishFrame.TFrame")
        ayam_bakarDishframe.configure(style="DishFrame.TFrame")
        sotoDishframe.configure(style="DishFrame.TFrame")
        rawonDishframe.configure(style="DishFrame.TFrame")
        mendoanDishframe.configure(style="DishFrame.TFrame")
        tahu_isiDishframe.configure(style="DishFrame.TFrame")
        risolDishframe.configure(style="DishFrame.TFrame")
        lumpiaDishframe.configure(style="DishFrame.TFrame")
        es_tehDishframe.configure(style="DishFrame.TFrame")
        es_jerukDishframe.configure(style="DishFrame.TFrame")
        lemon_teaDishframe.configure(style="DishFrame.TFrame")

        displayLabel.configure(
            image=es_coklatImage,
            text="Es Coklat",
            font=('Helvetica', 14, "bold"),
            foreground="white",
            compound="bottom",
            padding=(5, 5, 5, 5),
        )

    def order():
        new_receipt = orderIDLabel.cget("text").replace("ORDER ID : ", "")
        transaction_list = orderTransaction.cget("text").split("\n") if orderTransaction.cget("text") else []
        
        order_day = date.today()
        order_time = datetime.now()
        total = orderTotalLabel.cget("text")
        
        generate_pdf(new_receipt, transaction_list, total, order_day, order_time)
        save_order_history(new_receipt, transaction_list, total, order_day, order_time)

        # Reset
        orderTotalLabel.configure(text="TOTAL : Rp 0")
        orderIDLabel.configure(text="ORDER ID : " + ORDER_ID())
        orderTransaction.configure(text="")

    #Styling and Image
    s = ttk.Style()
    s.configure('MainFrame.TFrame', background="#2B2B28")
    s.configure('MenuFrame.TFrame', background="#6B2301")
    s.configure('DisplayFrame.TFrame', background="#0F1110")
    s.configure('OrderFrame.TFrame', background="#363431")
    s.configure('DishFrame.TFrame', background="#F58709", relief="raised")
    s.configure('SelectedDish.TFrame', background="#FCF8F3", relief="sunken")
    s.configure('MenuLabel.TLabel',
                background="#6B2301",
                font=("Arial", 13, "italic"),
                foreground="white",
                padding=(2, 2, 2, 2),
                width=25
                )
    s.configure('orderTotalLabel.TLabel',
                background="#0F1110",
                font=("Arial", 10, "bold"),
                foreground="white",
                padding=(2, 2, 2, 2),
                anchor="w")
    s.configure('orderTransaction.TLabel',
                background="#4A4A48",
                font=("Helvetica", 12),
                foreground="white",
                wraplength=170,
                anchor="nw",
                padding=(3, 3, 3, 3),
                )

    #region images
    # top banner images
    LogoImageObject = Image.open("images/logo.png").resize((130, 130))
    LogoImage = ImageTk.PhotoImage(LogoImageObject)

    TopBannerImageObject = Image.open("images/top banner.png").resize((1145, 130))
    TopBannerImage = ImageTk.PhotoImage(TopBannerImageObject)

    #menu images
    displayDefaultImageObject = Image.open("images/menu makanan.png").resize((650, 360))
    displayDefaultImage = ImageTk.PhotoImage(displayDefaultImageObject)

    steak_ayamImageObject = Image.open("menu/steak ayam.png").resize((350, 334))
    steak_ayamImage = ImageTk.PhotoImage(steak_ayamImageObject)

    nasi_gorengImageObject = Image.open("menu/nasi goreng.png").resize((350, 334))
    nasi_gorengImage = ImageTk.PhotoImage(nasi_gorengImageObject)

    ayam_gorengImageObject = Image.open("menu/ayam goreng.png").resize((350, 334))
    ayam_gorengImage = ImageTk.PhotoImage(ayam_gorengImageObject)

    ayam_bakarImageObject = Image.open("menu/ayam bakar.png").resize((350, 334))
    ayam_bakarImage = ImageTk.PhotoImage(ayam_bakarImageObject)

    sotoImageObject = Image.open("menu/soto ayam.png").resize((350, 334))
    sotoImage = ImageTk.PhotoImage(sotoImageObject)

    rawonImageObject = Image.open("menu/rawon.png").resize((350, 334))
    rawonImage = ImageTk.PhotoImage(rawonImageObject)

    mendoanImageObject = Image.open("menu/mendoan.png").resize((350, 334))
    mendoanImage = ImageTk.PhotoImage(mendoanImageObject)

    tahu_isiImageObject = Image.open("menu/tahu isi.png").resize((350, 334))
    tahu_isiImage = ImageTk.PhotoImage(tahu_isiImageObject)

    risolImageObject = Image.open("menu/risol.png").resize((350, 334))
    risolImage = ImageTk.PhotoImage(risolImageObject)

    lumpiaImageObject = Image.open("menu/lumpia.png").resize((350, 334))
    lumpiaImage = ImageTk.PhotoImage(lumpiaImageObject)

    es_tehImageObject = Image.open("menu/es teh.png").resize((350, 334))
    es_tehImage = ImageTk.PhotoImage(es_tehImageObject)

    es_jerukImageObject = Image.open("menu/es jeruk.png").resize((350, 334))
    es_jerukImage = ImageTk.PhotoImage(es_jerukImageObject)

    lemon_teaImageObject = Image.open("menu/lemon tea.png").resize((350, 334))
    lemon_teaImage = ImageTk.PhotoImage(lemon_teaImageObject)

    es_coklatImageObject = Image.open("menu/es coklat.png").resize((350, 334))
    es_coklatImage = ImageTk.PhotoImage(es_coklatImageObject)

    #Section Frame
    mainFrame = ttk.Frame(root, width=800, height=700, style='MainFrame.TFrame')
    mainFrame.grid(row=0, column=0, sticky="NSEW")

    topBannerFrame = ttk.Frame(mainFrame)
    topBannerFrame.grid(row=0, column=0, sticky="NSEW", columnspan=3)

    menuFrame = ttk.Frame(mainFrame, style='MenuFrame.TFrame')
    menuFrame.grid(row=1, column=0, padx=3, pady=2, sticky="NSEW")

    displayFrame = ttk.Frame(mainFrame, style='MenuFrame.TFrame')
    displayFrame.grid(row=1, column=1, padx=3, pady=2, sticky="NSEW")

    orderFrame = ttk.Frame(mainFrame, style="OrderFrame.TFrame")
    orderFrame.grid(row=1, column=2, padx=3, pady=2, sticky="NSEW")

    #dish frame
    steak_ayamDishframe = ttk.Frame(menuFrame, style="DishFrame.TFrame")
    steak_ayamDishframe.grid(row=1, column=0, sticky="NSEW")

    nasi_gorengDishframe = ttk.Frame(menuFrame, style="DishFrame.TFrame")
    nasi_gorengDishframe.grid(row=2, column=0, sticky="NSEW")

    ayam_gorengDishframe = ttk.Frame(menuFrame, style="DishFrame.TFrame")
    ayam_gorengDishframe.grid(row=3, column=0, sticky="NSEW")

    ayam_bakarDishframe = ttk.Frame(menuFrame, style="DishFrame.TFrame")
    ayam_bakarDishframe.grid(row=4, column=0, sticky="NSEW")

    sotoDishframe = ttk.Frame(menuFrame, style="DishFrame.TFrame")
    sotoDishframe.grid(row=5, column=0, sticky="NSEW")

    rawonDishframe = ttk.Frame(menuFrame, style="DishFrame.TFrame")
    rawonDishframe.grid(row=6, column=0, sticky="NSEW")

    mendoanDishframe = ttk.Frame(menuFrame, style="DishFrame.TFrame")
    mendoanDishframe.grid(row=7, column=0, sticky="NSEW")

    tahu_isiDishframe = ttk.Frame(menuFrame, style="DishFrame.TFrame")
    tahu_isiDishframe.grid(row=8, column=0, sticky="NSEW")

    risolDishframe = ttk.Frame(menuFrame, style="DishFrame.TFrame")
    risolDishframe.grid(row=9, column=0, sticky="NSEW")

    lumpiaDishframe = ttk.Frame(menuFrame, style="DishFrame.TFrame")
    lumpiaDishframe.grid(row=10, column=0, sticky="NSEW")

    es_tehDishframe = ttk.Frame(menuFrame, style="DishFrame.TFrame")
    es_tehDishframe.grid(row=11, column=0, sticky="NSEW")

    es_jerukDishframe = ttk.Frame(menuFrame, style="DishFrame.TFrame")
    es_jerukDishframe.grid(row=12, column=0, sticky="NSEW")

    lemon_teaDishframe = ttk.Frame(menuFrame, style="DishFrame.TFrame")
    lemon_teaDishframe.grid(row=13, column=0, sticky="NSEW")

    es_coklatDishframe = ttk.Frame(menuFrame, style="DishFrame.TFrame")
    es_coklatDishframe.grid(row=14, column=0, sticky="NSEW")

    #region top banner section
    LogoLabel = ttk.Label(topBannerFrame, image=LogoImage, background="#FFFCFC") 
    LogoLabel.grid(row=0, column=0, sticky="W")

    RestaurantBannerLabel = ttk.Label(topBannerFrame, image=TopBannerImage, background="#080808")
    RestaurantBannerLabel.grid(row=0, column=1, sticky="NSEW")

    #endregion 

    #region menu section
    MainMenulabel = ttk.Label(menuFrame, text="MENU", style="MenuLabel.TLabel")
    MainMenulabel.grid(row=0, column=0, sticky="WE")
    MainMenulabel.configure(
        anchor="center",
        font=("Helvetica", 14, "bold")
    )

    steak_ayamDishLabel = ttk.Label(steak_ayamDishframe, text=f"Steak Ayam ..... Rp {prices['Steak Ayam']:,}", style="MenuLabel.TLabel")
    steak_ayamDishLabel.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    nasi_gorengDishLabel = ttk.Label(nasi_gorengDishframe, text=f"Nasi Goreng ..... Rp {prices['Nasi Goreng']:,}", style="MenuLabel.TLabel")
    nasi_gorengDishLabel.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    ayam_gorengDishLabel = ttk.Label(ayam_gorengDishframe, text=f"Ayam Goreng ..... Rp {prices['Ayam Goreng']:,}", style="MenuLabel.TLabel")
    ayam_gorengDishLabel.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    ayam_bakarDishLabel = ttk.Label(ayam_bakarDishframe, text=f"Ayam Bakar ..... Rp {prices['Ayam Bakar']:,}", style="MenuLabel.TLabel")
    ayam_bakarDishLabel.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    sotoDishLabel = ttk.Label(sotoDishframe, text=f"Soto Ayam ..... Rp {prices['Soto Ayam']:,}", style="MenuLabel.TLabel")
    sotoDishLabel.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    rawonDishLabel = ttk.Label(rawonDishframe, text=f"Rawon ..... Rp {prices['Rawon']:,}", style="MenuLabel.TLabel")
    rawonDishLabel.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    mendoanDishLabel = ttk.Label(mendoanDishframe, text=f"Mendoan ..... Rp {prices['Mendoan']:,}", style="MenuLabel.TLabel")
    mendoanDishLabel.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    tahu_isiDishLabel = ttk.Label(tahu_isiDishframe, text=f"Tahu Isi ..... Rp {prices['Tahu Isi']:,}", style="MenuLabel.TLabel")
    tahu_isiDishLabel.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    lumpiaDishLabel = ttk.Label(lumpiaDishframe, text=f"Lumpia ..... Rp {prices['Lumpia']:,}", style="MenuLabel.TLabel")
    lumpiaDishLabel.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    risolDishLabel = ttk.Label(risolDishframe, text=f"Risol ..... Rp {prices['Risol']:,}", style="MenuLabel.TLabel")
    risolDishLabel.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    es_tehDishLabel = ttk.Label(es_tehDishframe, text=f"Es Teh ..... Rp {prices['Es Teh']:,}", style="MenuLabel.TLabel")
    es_tehDishLabel.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    es_jerukDishLabel = ttk.Label(es_jerukDishframe, text=f"Es Jeruk ..... Rp {prices['Es Jeruk']:,}", style="MenuLabel.TLabel")
    es_jerukDishLabel.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    lemon_teaDishLabel = ttk.Label(lemon_teaDishframe, text=f"Lemon Tea ..... Rp {prices['Lemon Tea']:,}", style="MenuLabel.TLabel")
    lemon_teaDishLabel.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    es_coklatDishLabel = ttk.Label(es_coklatDishframe, text=f"Es Coklat ..... Rp {prices['Es Coklat']:,}", style="MenuLabel.TLabel")
    es_coklatDishLabel.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    #buttons
    steak_ayamDisplayButton = ttk.Button(steak_ayamDishframe, text="Display", command=displaysteak_ayam)
    steak_ayamDisplayButton.grid(row=0, column=1, padx=10)

    nasi_gorengDisplayButton = ttk.Button(nasi_gorengDishframe, text="Display", command=displaynasi_goreng)
    nasi_gorengDisplayButton.grid(row=0, column=1, padx=10)

    ayam_gorengDisplayButton = ttk.Button(ayam_gorengDishframe, text="Display", command=displayayam_goreng)
    ayam_gorengDisplayButton.grid(row=0, column=1, padx=10)

    ayam_bakarDisplayButton = ttk.Button(ayam_bakarDishframe, text="Display", command=displayayam_bakar)
    ayam_bakarDisplayButton.grid(row=0, column=1, padx=10)

    sotoDisplayButton = ttk.Button(sotoDishframe, text="Display", command=displaysoto)
    sotoDisplayButton.grid(row=0, column=1, padx=10)

    rawonDisplayButton = ttk.Button(rawonDishframe, text="Display", command=displayrawon)
    rawonDisplayButton.grid(row=0, column=1, padx=10)

    mendoanDisplayButton = ttk.Button(mendoanDishframe, text="Display", command=displaymendoan)
    mendoanDisplayButton.grid(row=0, column=1, padx=10)

    tahu_isiDisplayButton = ttk.Button(tahu_isiDishframe, text="Display", command=displaytahu_isi)
    tahu_isiDisplayButton.grid(row=0, column=1, padx=10)

    risolDisplayButton = ttk.Button(risolDishframe, text="Display", command=displayrisol)
    risolDisplayButton.grid(row=0, column=1, padx=10)

    lumpiaDisplayButton = ttk.Button(lumpiaDishframe, text="Display", command=displaylumpia)
    lumpiaDisplayButton.grid(row=0, column=1, padx=10)

    es_tehDisplayButton = ttk.Button(es_tehDishframe, text="Display", command=displayes_teh)
    es_tehDisplayButton.grid(row=0, column=1, padx=10)

    es_jerukDisplayButton = ttk.Button(es_jerukDishframe, text="Display", command=displayes_jeruk)
    es_jerukDisplayButton.grid(row=0, column=1, padx=10)

    lemon_teaDisplayButton = ttk.Button(lemon_teaDishframe, text="Display", command=displaylemon_tea)
    lemon_teaDisplayButton.grid(row=0, column=1, padx=10)

    es_coklatDisplayButton = ttk.Button(es_coklatDishframe, text="Display", command=displayes_coklat)
    es_coklatDisplayButton.grid(row=0, column=1, padx=10)
    #endregion

    #region order section
    orderTitleLabel = ttk.Label(orderFrame, text="ORDER")
    orderTitleLabel.configure(
        foreground="white", background="black",
        font=("Helvetica", 14, "bold"), anchor="center",
        padding=(5, 5, 5, 5), 
    )
    orderTitleLabel.grid(row=0, column=0, sticky="EW")

    orderIDLabel = ttk.Label(orderFrame, text="ORDER ID : " + ORDER_ID())
    orderIDLabel.configure(
        background="black",
        foreground="white",
        font=("Helvetica", 11, "italic"),
        anchor="center",
    )
    orderIDLabel.grid(row=1, column=0, sticky="EW")

    orderTransaction = ttk.Label(orderFrame, style='orderTransaction.TLabel')
    orderTransaction.grid(row=2, column=0, sticky="NEW")

    orderTotalLabel = ttk.Label(orderFrame, text="TOTAL : Rp 0", style='orderTotalLabel.TLabel')
    orderTotalLabel.grid(row=3, column=0, sticky="EW")

    orderButton = ttk.Button(orderFrame, text="ORDER", command=order)
    orderButton.grid(row=4, column=0, sticky="EW")

    if is_admin:
        adminButton = ttk.Button(orderFrame, text="EDIT MENU", command=admin_edit)
        adminButton = ttk.Button(orderFrame, text="LAPORAN HARIAN",command=lambda: generate_daily_report(date.today()))
        adminButton.grid(row=5, column=0, sticky="EW")
        adminButton.grid(row=6, column=0, sticky="EW")

    #region display section
    displayLabel = ttk.Label(displayFrame, image=displayDefaultImage)
    displayLabel.grid(row=0, column=0, sticky="NSEW", columnspan=2)
    displayLabel.configure(background="#0F1110")

    addOrderButton = ttk.Button(displayFrame, text="ADD TO ORDER", command=add)
    addOrderButton.grid(row=1, column=0, padx=2, sticky="NSEW")

    removeOrderButton = ttk.Button(displayFrame, text="REMOVE", command=remove)
    removeOrderButton.grid(row=1, column=1, padx=2, sticky="NSEW")

    #grid configguration
    mainFrame.columnconfigure(2, weight=1)
    mainFrame.rowconfigure(1, weight=1)
    menuFrame.columnconfigure(0, weight=1)
    menuFrame.rowconfigure(1, weight=1)
    menuFrame.rowconfigure(2, weight=1)
    menuFrame.rowconfigure(3, weight=1)
    menuFrame.rowconfigure(4, weight=1)
    menuFrame.rowconfigure(5, weight=1)
    menuFrame.rowconfigure(6, weight=1)
    orderFrame.columnconfigure(0, weight=1)
    orderFrame.rowconfigure(2, weight=1)

    root.mainloop()

# Fungsi untuk jendela login
def login_window():
    login_root = Tk()
    login_root.title("Login - Kedai FMR")
    login_root.geometry("1210x590")
    login_root.configure(bg="#F58709")
    
    ttk.Label(
        login_root, 
        text="Choose Your Role:", 
        font=("Arial", 26, "bold"), 
        foreground="#010000",
        background="#F58709"
    ).pack(pady=25)
    
    def select_customer():
        login_root.destroy()
        main_app(is_admin=False)
    
    def select_admin():
        password_window = Toplevel(login_root)
        password_window.title("Admin Password")
        password_window.geometry("250x180")
        password_window.configure(bg="#F58709") 
        
        # Label putih
        pw_label = Label(
            password_window, 
            text="Enter Password:", 
            font=("Arial", 14),
            fg="black",
            bg="#FFFFFF"
        )
        pw_label.pack(pady=15)
        
        password_entry = ttk.Entry(password_window, show="*")
        password_entry.pack()
        
        def check_password():
            if password_entry.get() == "maulunyil":
                password_window.destroy()
                login_root.destroy()
                main_app(is_admin=True)
            else:
                messagebox.showerror("Error", "Incorrect Password")
        
        # Tombol login
        ttk.Button(password_window, text="Login", command=check_password).pack(pady=15)
    
    ttk.Button(login_root, text="Customer", command=select_customer, style="Big.TButton").pack(pady=7)
    ttk.Button(login_root, text="Admin", command=select_admin, style="Big.TButton").pack(pady=7)

    style = ttk.Style()
    style.configure("Big.TButton", font=("Arial", 20), padding=7)
    
    login_root.mainloop()


if __name__ == "__main__":
    login_window()