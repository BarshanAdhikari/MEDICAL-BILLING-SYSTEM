from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk
import qrcode
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random

# Sample data for tests and doctors
tests = {
    "Blood Test ": 100,
    "X-Ray ": 200,
    "MRI ": 500,
    "CT Scan ": 400,
    "USG ": 300,
    "ECG ": 150,
    "Urine Test": 1000,                            
    "Liver Function Test ": 250,
    "Kidney Function Test ": 250,
    "Thyroid Test": 200,
    "Cholesterol Test": 180,
    "Blood Sugar Test": 120,
    "Vitamin D Test": 220,
    "Calcium Test": 130,
    "Allergy Test": 350,
    "HIV Test": 300,
    "Pregnancy Test": 100,
    "Stool Test ": 150,
    "Bone Density Test": 450,
    "Pap Smear": 200,
}

doctors = {
    "Dr.Rishav": {"image": "doctor1.jpg", "specialization": "Cardiologist", "experience": "10 years"},
    "Dr.Sandipan": {"image": "doctor2.jpg", "specialization": "Dermatologist", "experience": "8 years"},
    "Dr.Amit": {"image": "doctor3.jpg", "specialization": "Pediatrician", "experience": "7 years"},
    "Dr.Shilpa": {"image": "doctor4.jpg", "specialization": "Gynecologist", "experience": "9 years"},
    "Dr.Vikram": {"image": "doctor5.jpg", "specialization": "dentist", "experience": "6 years"},
    
}

# Function to update doctor details
def update_doctor_details(event):
    doctor_name = doctor_var.get()
    if doctor_name in doctors:
        doctor_info = doctors[doctor_name]
        doctor_label.config(text=doctor_name)
        specialization_label.config(text=f"Specialization: {doctor_info['specialization']}")
        experience_label.config(text=f"Experience: {doctor_info['experience']}")
        
        # Load and display doctor image
        try:
            doctor_image = Image.open(doctor_info['image'])
            doctor_image = doctor_image.resize((300, 300), Image.LANCZOS)
            doctor_photo = ImageTk.PhotoImage(doctor_image)
            doctor_image_label.config(image=doctor_photo)
            doctor_image_label.image = doctor_photo
        except FileNotFoundError:
            placeholder_image = Image.open("placeholder.png")  
            placeholder_image = placeholder_image.resize((300, 300), Image.LANCZOS)
            placeholder_photo = ImageTk.PhotoImage(placeholder_image)
            doctor_image_label.config(image=placeholder_photo)
            doctor_image_label.image = placeholder_photo

# Function to generate and display QR code
def generate_qr_code(amount):
    payment_id = "barshanadhikari181-1@okicici"  
    payment_url = f"upi://pay?pa={payment_id}&pn=YourName&mc=1234&tid=000123&am={amount}&tn=Payment%20for%20medical%20services&cu=INR&url=https://your-website.com"
    
    # Generate QR code
    qr = qrcode.make(payment_url)
    qr_path = "payment_qr.png"
    qr.save(qr_path)
    
    # Load and display the QR code image
    try:
        qr_image = Image.open(qr_path)
        qr_image = qr_image.resize((150, 150), Image.LANCZOS)
        qr_photo = ImageTk.PhotoImage(qr_image)

        # Display QR code
        qr_image_label.config(image=qr_photo)
        qr_image_label.image = qr_photo  
    except Exception as e:
        messagebox.showerror("Error", f"Could not display QR Code: {e}")

def write_bill_to_pdf():

    patient_name = patient_name_entry.get()
    selected_tests_indices = tests_listbox.curselection()
    selected_tests = [tests_listbox.get(i) for i in selected_tests_indices]
    doctor_name = doctor_var.get()
    payment_method = payment_var.get()  # Get selected payment method
    patient_age=patient_age_entry.get()
    p_gen=patient_gender.get()
    
    
    if not patient_name or not selected_tests or not doctor_name or not payment_method or not patient_age or not p_gen:
        messagebox.showerror("Error", "Please fill all details before generating the bill.")
        return
    
    # Calculate total fees
    total = sum(tests[test] for test in selected_tests)

    # Create a unique bill number (for example, use a random number or time-based ID)
    bill_number = random.randint(1000, 9999)

    # Get current date
    current_date = datetime.now().strftime("%d-%m-%Y")

    # Create the PDF document
    pdf_path = f"{patient_name}_{bill_number}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Margins
    outer_margin = 40
    inner_margin = 20
    c.setLineWidth(3)

    # Header: Medical Institute
    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, 680, "MEDICAL BILL")
    
    # Add a line under the header
    c.setLineWidth(1)
    c.line(outer_margin, 670, 550, 670)
    c.line(outer_margin, 672, 552, 672)  

    # Date, Patient Name (left) and Bill Number (right)
    c.setFont("Helvetica", 12)
    c.drawString(50, 650, f"Date: {current_date}")
    c.drawString(400, 650, f"Bill Number: {bill_number}")

    # Patient Name gender ,age
    c.drawString(50, 630, f"Patient Name: {patient_name}")
    c.drawString(229, 630, f"Gender: {p_gen}")
    c.drawString(400, 630, f"Patient Age: {patient_age}")

    # Add a line after Patient Name
    c.line(outer_margin, 625, 550, 625)  

    # Column Headers (Tests and Fees)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 600, "Tests Selected")
    c.drawString(350, 600, "Fees (RS)")

    # List Tests and Fees
    y_position = 580
    for test in selected_tests:
        c.setFont("Helvetica", 10)
        c.drawString(50, y_position, test)
        c.drawString(350, y_position, str(tests[test]))
        y_position -= 20

    # Add a line after the test details
    c.line(outer_margin, y_position, 550, y_position)  

    # Doctor Name
    y_position -= 20
    c.drawString(50, y_position, f"Selected Doctor: {doctor_name}")

    # Total Bill and Payment Method
    y_position -= 20
    c.drawString(50, y_position, f"Total Bill: RS:{total}")
    y_position -= 20
    c.drawString(50, y_position, f"Payment Method: {payment_method}")

    # Save the PDF file
    c.save()

    # Open the PDF file
    os.startfile(pdf_path)  # This will open the PDF on Windows
    messagebox.showinfo("Success", f"Bill generated successfully! Saved as {pdf_path}")
    
# Function to calculate total bill
def calculate_total():
    total = 0
    selected_tests_indices = tests_listbox.curselection()
    for index in selected_tests_indices:
        test_name = tests_listbox.get(index)
        total += tests[test_name]
    total_label.config(text=f"Total Bill: RS:{total}")

# Function to update QR code display based on payment method
def update_payment_method(event):
    if payment_var.get() == "Online":
        # Generate QR code instantly when 'Online' is selected
        selected_tests_indices = tests_listbox.curselection()
        total = sum(tests[tests_listbox.get(i)] for i in selected_tests_indices)
        generate_qr_code(total)
        qr_name.grid(row=7, column=1, pady=10)
        qr_image_label.grid(row=8, column=1, pady=10)
    else:
        qr_name.grid_forget()
        qr_image_label.grid_forget()

# Setup main window 
root = Tk()
root.geometry("1000x600")
root.config(background="gray")
root.title("ABC MEDICAL INSTITUTE")

# Date handling
today = datetime.today()
date_only = today.strftime("%Y-%m-%d")

# Header (same as before)
header_frame = Frame(root, background="white")
header_frame.pack(fill=X)

title = Label(header_frame, text="MEDICAL BILL", background="gray", foreground="red", font=("bodoni mt", 20, "bold"), borderwidth=10, relief=GROOVE, padx=5, pady=5)
title.pack(side=TOP, fill=X)

date_label = Label(header_frame, text=f"Date: {date_only}", font=("comicsansns", 13, "bold"))
date_label.pack(side=LEFT, padx=10)

# Division line
separator = Frame(root, height=2, bg="black")
separator.pack(fill=X, padx=10, pady=10)

# Input Section 
input_frame = Frame(root, background="blue")
input_frame.pack(side=LEFT, fill=BOTH, expand=True)

# Patient Name 
Label(input_frame, text="Patient Name:", font=("comicsansns", 11, "bold")).grid(row=0, column=0, padx=10, pady=10)
patient_name_entry = Entry(input_frame)
patient_name_entry.grid(row=0, column=1, padx=10, pady=10)
#patient age
Label(input_frame,text="enter age",font=("comicsansns", 11, "bold")).grid(row=1,column=0,padx=10,pady=10)
patient_age_entry = Entry(input_frame)
patient_age_entry.grid(row=1, column=1, padx=10, pady=10)

#patient gender
patient_gender=StringVar() 
patient_gender.set(0)
Label(input_frame,text="gender",font=("comicsansns", 11, "bold")).grid(row=2,column=0,padx=10,pady=10)
rb1=Radiobutton(input_frame,text="M",variable=patient_gender,value="male").grid(row=2,column=1,padx=10,pady=10)
rb2=Radiobutton(input_frame,text="F",variable=patient_gender,value="female").grid(row=2,column=2,padx=10,pady=10)
rb3=Radiobutton(input_frame,text="O",variable=patient_gender,value="other").grid(row=2,column=3,padx=10,pady=10)

# Medical Tests 
Label(input_frame, text="Select Medical Tests:", font=("comicsansns", 11, "bold")).grid(row=3, column=0, padx=10, pady=10)
tests_listbox = Listbox(input_frame, selectmode=MULTIPLE, font=("comicsansns", 10))
for test in tests.keys():
    tests_listbox.insert(END, test)
tests_listbox.grid(row=3, column=1, padx=10, pady=10)
tests_listbox.bind("<<ListboxSelect>>", lambda e: calculate_total())

# Doctor Selection 
Label(input_frame, text="Select Doctor:", font=("comicsansns", 11, "bold")).grid(row=4, column=0, padx=10, pady=10)
doctor_var = StringVar()
doctor_combobox = ttk.Combobox(input_frame, textvariable=doctor_var, values=list(doctors.keys()), state='readonly')
doctor_combobox.grid(row=4, column=1, padx=10, pady=10)
doctor_combobox.bind("<<ComboboxSelected>>", update_doctor_details)

# Payment Method Selection 
Label(input_frame, text="Payment Method:", font=("comicsansns", 11, "bold")).grid(row=5, column=0, padx=10, pady=10)
payment_var = StringVar()
payment_combobox = ttk.Combobox(input_frame, textvariable=payment_var, values=["Online", "Offline"], state='readonly')
payment_combobox.grid(row=5, column=1, padx=10, pady=10)
payment_combobox.bind("<<ComboboxSelected>>", update_payment_method)

# Total Bill 
total_label = Label(input_frame, text="Total Bill: RS:0", font=("comicsansns", 12, "bold"))
total_label.grid(row=6, columnspan=2, padx=10, pady=10)

# QR Code Image Label 
qr_name = Label(input_frame, text="To pay scan this", font=("comicsansns", 11, "bold"))
qr_image_label = Label(input_frame, background="white")

# Button to save bill details
save_button = Button(input_frame, text="GENERATE BILL", font=("comicsansns", 10, "bold"), command=write_bill_to_pdf)
save_button.grid(row=8, column=3, pady=20)  

# Doctor Details Section
doctor_frame = Frame(root, background="white")
doctor_frame.pack(side=RIGHT, fill=BOTH, expand=True)

doctor_label = Label(doctor_frame, text="Doctor: Not Selected", font=("comicsansns", 12, "bold"))
doctor_label.pack(pady=10)

specialization_label = Label(doctor_frame, text="Specialization: Not Available", font=("comicsansns", 11, "bold"))
specialization_label.pack(pady=10)

experience_label = Label(doctor_frame, text="Experience: Not Available", font=("comicsansns", 11, "bold"))
experience_label.pack(pady=10)

doctor_image_label = Label(doctor_frame, background="white")
doctor_image_label.pack(pady=10)


root.mainloop()
