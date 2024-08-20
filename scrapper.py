import os
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# URL to scrape
url = "https://www.gutenberg.org/browse/scores/top"

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
fonts_dir = "./fonts"

# Function to scrape the "Top 100 EBooks yesterday" section
def scrape_top_ebooks():
    ebooks = []
    section = soup.find('h2', id="books-last1")
    if section:
        ol = section.find_next_sibling('ol')
        if ol:
            for li in ol.find_all('li'):
                book_title = li.get_text().split('(')[0].strip()
                book_link = li.find('a')['href']
                ebooks.append({
                    'title': book_title,
                    'link': f"https://www.gutenberg.org{book_link}"
                })
    return ebooks

# Function to download the text file and convert to PDF
def download_and_convert_to_pdf(ebook):
    book_code = ebook['link'].split('/')[-1]  # Extract the book code from the link
    text_url = f"https://www.gutenberg.org/ebooks/{book_code}.txt.utf-8"
    
    # Send a GET request to download the text content
    text_response = requests.get(text_url)
    
    if text_response.status_code == 200:
        # Handle the encoding issue
        text_content = text_response.content.decode('utf-8-sig')
        
        # Create a PDF file
        pdf = FPDF()
        pdf.add_font("DejaVu", "", os.path.join(fonts_dir, "DejaVuSans.ttf"), uni=True)
        pdf.add_font("DejaVu", "B", os.path.join(fonts_dir, "DejaVuSans-Bold.ttf"), uni=True)
        pdf.add_font("DejaVu", "I", os.path.join(fonts_dir, "DejaVuSans-Oblique.ttf"), uni=True)

        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("DejaVu", size=12)
        
        # Write each line of the text into the PDF
        for line in text_content.splitlines():
            pdf.multi_cell(0, 10, line)
        
        # Save the PDF file with the book title as the name
        pdf_filename = f"{ebook['title']}.pdf"
        pdf_filename = "".join([c for c in pdf_filename if c.isalpha() or c.isdigit() or c == ' ']).rstrip() + ".pdf"
        
        # Ensure the filename is unique
        pdf_filename = os.path.join("downloads", pdf_filename)
        os.makedirs(os.path.dirname(pdf_filename), exist_ok=True)
        
        pdf.output(pdf_filename)
        print(f"Downloaded and converted: {pdf_filename}")
    else:
        print(f"Failed to download text for: {ebook['title']}")

# Main function to execute the scraper and download
def main():
    ebooks = scrape_top_ebooks()
    
    # Create a thread pool for parallel processing
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Use tqdm for progress indication
        list(tqdm(executor.map(download_and_convert_to_pdf, ebooks), total=len(ebooks), desc="Processing eBooks"))

if __name__ == "__main__":
    main()
