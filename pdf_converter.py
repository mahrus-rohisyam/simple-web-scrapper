import os
import queue
import threading
from datetime import datetime
from fpdf import FPDF
from tqdm import tqdm  # Progress bar for better user feedback

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

# Path to your fonts directory
fonts_dir = "./fonts"

# Initialize a queue
file_queue = queue.Queue()

# Worker function to process files
def process_file():
    while True:
        filename = file_queue.get()
        if filename is None:
            break  # Stop the thread if None is received

        # Create a PDF instance for each file to ensure thread safety
        pdf = PDF()
        pdf.add_font("DejaVu", "", os.path.join(fonts_dir, "DejaVuSans.ttf"), uni=True)
        pdf.add_font("DejaVu", "B", os.path.join(fonts_dir, "DejaVuSans-Bold.ttf"), uni=True)
        pdf.add_font("DejaVu", "I", os.path.join(fonts_dir, "DejaVuSans-Oblique.ttf"), uni=True)

        # Read the text from the current .txt file with UTF-8 encoding
        with open(os.path.join(input_dir, filename), "r", encoding="utf-8") as file:
            text = file.read()

        # Add a new page and set font
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

        # Mark task as done
        file_queue.task_done()
        tqdm.write(f"Converted {filename} to {output_filename}")

# List of all .txt files in the input directory
txt_files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]

# Progress bar for the queuing process
progress_bar = tqdm(total=len(txt_files), desc="Queueing files", unit="file")

# Start worker threads
num_worker_threads = 4
threads = []
for _ in range(num_worker_threads):
    thread = threading.Thread(target=process_file)
    thread.start()
    threads.append(thread)

# Enqueue files
for filename in txt_files:
    file_queue.put(filename)
    progress_bar.update(1)

# Wait for all files to be processed
file_queue.join()

# Stop workers
for _ in range(num_worker_threads):
    file_queue.put(None)

for thread in threads:
    thread.join()

progress_bar.close()

print("All files have been converted.")
