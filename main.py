import os
from datetime import datetime
from fpdf import FPDF

# Create a PDF class instance
class PDF(FPDF):
    def footer(self):
        # Add a footer
        self.set_y(-15)
        self.set_font("DejaVu", "I", 8)
        self.cell(0, 10, "Page " + str(self.page_no()), 0, 0, "C")

# Paths for input and output directories
input_dir = "./sample"
output_dir = "./output"

# Get the current date to append to filenames
current_date = datetime.now().strftime("%Y%m%d")

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create a PDF instance
pdf = PDF()

# Path to your fonts directory
fonts_dir = "./fonts"

# Add a Unicode font from the fonts directory
pdf.add_font("DejaVu", "", os.path.join(fonts_dir, "DejaVuSans.ttf"), uni=True)
pdf.add_font("DejaVu", "B", os.path.join(fonts_dir, "DejaVuSans-Bold.ttf"), uni=True)
pdf.add_font("DejaVu", "I", os.path.join(fonts_dir, "DejaVuSans-Oblique.ttf"), uni=True)

# Iterate through all .txt files in the /sample directory
for filename in os.listdir(input_dir):
    if filename.endswith(".txt"):
        # Read the text from the current .txt file with UTF-8 encoding
        with open(os.path.join(input_dir, filename), "r", encoding="utf-8") as file:
            text = file.read()

        # Add a new page for each file
        pdf.add_page()
        pdf.set_font("DejaVu", size=12)

        # Add the text to the PDF
        pdf.multi_cell(0, 10, txt=text, align="L")

        # Create the output filename with the current date
        base_filename = os.path.splitext(filename)[0]
        output_filename = f"{base_filename}_{current_date}.pdf"
        output_path = os.path.join(output_dir, output_filename)

        # Save the PDF
        pdf.output(output_path)

        print(f"Converted {filename} to {output_filename}")
