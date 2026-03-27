import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image

# Global variable to store image path
profile_image_path = ""

# Function to select profile picture
def select_image():
    global profile_image_path
    profile_image_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
    )
    if profile_image_path:
        messagebox.showinfo("Selected Image", f"Selected image: {profile_image_path}")

# Function to generate PDF CV
def generate_pdf():
    global profile_image_path
    name = entry_name.get().strip()
    contact = entry_contact.get().strip()
    email = entry_email.get().strip()
    address = entry_address.get().strip()
    location = entry_location.get().strip()
    profile = text_profile.get("1.0", tk.END).strip()
    education = text_education.get("1.0", tk.END).strip()
    certifications = text_cert.get("1.0", tk.END).strip()
    skills = text_skills.get("1.0", tk.END).strip()
    experience = text_experience.get("1.0", tk.END).strip()
    projects = text_projects.get("1.0", tk.END).strip()

    if not name:
        messagebox.showerror("Error", "Full Name is required!")
        return

    # Download / Save As dialog
    default_name = name.replace(" ", "_") + "_CV.pdf"
    file_path = filedialog.asksaveasfilename(
        initialfile=default_name,
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )

    if file_path:
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        # Draw profile picture if selected
        if profile_image_path:
            try:
                img = Image.open(profile_image_path)
                img.thumbnail((100, 100))  # resize to 100x100 max
                img_reader = ImageReader(img)
                c.drawImage(img_reader, width - 150, height - 120, width=100, height=100)
            except Exception as e:
                messagebox.showwarning("Image Error", f"Could not add image:\n{e}")

        # Header: Name
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.darkblue)
        c.drawString(50, height - 50, name.upper())

        # Contact info
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.black)
        contact_info = f"{contact} | {email} | {address} | {location}"
        c.drawString(50, height - 70, contact_info)

        # Separator line
        c.setStrokeColor(colors.darkblue)
        c.setLineWidth(1)
        c.line(50, height - 80, width - 50, height - 80)

        # Function to draw sections
        def draw_section(title, content, start_y):
            y = start_y
            if content.strip() == "":
                return y
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.darkblue)
            c.drawString(50, y, title)
            y -= 15
            c.setFont("Helvetica", 12)
            c.setFillColor(colors.black)
            for line in content.splitlines():
                if line.strip():
                    c.drawString(60, y, f"- {line.strip()}")
                    y -= 15
            return y - 10

        y_pos = height - 100
        y_pos = draw_section("Profile / Summary", profile, y_pos)
        y_pos = draw_section("Education", education, y_pos)
        y_pos = draw_section("Certifications", certifications, y_pos)
        y_pos = draw_section("Skills", skills, y_pos)
        y_pos = draw_section("Experience", experience, y_pos)
        y_pos = draw_section("Projects", projects, y_pos)

        # Footer
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(colors.grey)
        c.drawString(50, 20, "Generated with Python - Inaye Consultechnical Solutions")

        # Save PDF
        c.save()
        messagebox.showinfo("Download Complete", f"Your CV PDF has been saved!\n\nPath: {file_path}")

# GUI Window
window = tk.Tk()
window.title("Professional PDF CV Generator")
window.geometry("600x850")

# Input fields
fields = [
    ("Full Name", 50),
    ("Contact", 50),
    ("Email", 50),
    ("Address", 50),
    ("Location", 50)
]

entries = {}
for label_text, width in fields:
    tk.Label(window, text=label_text).pack()
    entry = tk.Entry(window, width=width)
    entry.pack()
    entries[label_text] = entry

entry_name = entries["Full Name"]
entry_contact = entries["Contact"]
entry_email = entries["Email"]
entry_address = entries["Address"]
entry_location = entries["Location"]

# Button to select profile picture
tk.Button(window, text="Select Profile Picture", command=select_image, bg="darkgreen", fg="white").pack(pady=5)

# Text areas for sections
tk.Label(window, text="Profile / Summary").pack()
text_profile = tk.Text(window, height=4, width=50)
text_profile.pack()

tk.Label(window, text="Education").pack()
text_education = tk.Text(window, height=4, width=50)
text_education.pack()

tk.Label(window, text="Certifications").pack()
text_cert = tk.Text(window, height=4, width=50)
text_cert.pack()

tk.Label(window, text="Skills").pack()
text_skills = tk.Text(window, height=4, width=50)
text_skills.pack()

tk.Label(window, text="Experience").pack()
text_experience = tk.Text(window, height=6, width=50)
text_experience.pack()

tk.Label(window, text="Projects").pack()
text_projects = tk.Text(window, height=6, width=50)
text_projects.pack()

# Generate PDF Button
tk.Button(window, text="Generate Professional PDF CV", command=generate_pdf, bg="darkblue", fg="white").pack(pady=15)

window.mainloop()
    
