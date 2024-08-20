# Simple Web Scrapper

This Python script downloads the top eBooks from Project Gutenberg, converts them into PDF format, and saves them to a specified directory. It utilizes concurrency to handle multiple files simultaneously and provides progress indicators during the processing.

## Features

- **Scrapes the Top 100 eBooks**: Retrieves the top eBooks list from Project Gutenberg's "Top 100 eBooks yesterday" section.
- **Handles Multiple Files**: Downloads and converts multiple eBooks in parallel using threading.
- **Progress Indication**: Displays progress using a progress bar to track the status of downloads and conversions.
- **Unique File Check**: Avoids downloading and converting eBooks that have already been processed.
- **Encoding Handling**: Properly handles text encoding issues to ensure accurate conversion to PDF.

## Requirements

- Python 3.6+
- `requests` library
- `beautifulsoup4` library
- `fpdf` library
- `tqdm` library

You can install the required libraries using pip:

```bash
pip install requests beautifulsoup4 fpdf tqdm
```

## Setup

1. **Directory Structure**:

   - Ensure you have a `fonts` directory containing the required font files for PDF generation. The script uses the DejaVu fonts (`DejaVuSans.ttf`, `DejaVuSans-Bold.ttf`, `DejaVuSans-Oblique.ttf`).
   - Ensure a `downloads` directory where the PDF files will be saved. The script will create this directory if it does not exist.

2. **Fonts**:
   - Download the DejaVu font files and place them in the `fonts` directory. You can get them from [DejaVu Fonts](https://dejavufonts.github.io/).

## Usage

1. **Running the Script**:

   Run the script from the command line using Python:

   ```bash
   python ebook_downloader.py
   ```

   The script will:

   - Scrape the top 100 eBooks from Project Gutenberg.
   - Download the text content of each eBook.
   - Convert the text content into a PDF file.
   - Save the PDF files to the `downloads` directory.

2. **Progress and Errors**:

   - The progress of each eBook download and conversion is displayed in the command line.
   - Any errors encountered during processing are reported to help with debugging.

## Customization

- **Thread Pool Size**: Adjust the `max_workers` parameter in `ThreadPoolExecutor` to control the number of concurrent downloads and conversions.
- **Fonts Directory**: Update the `fonts_dir` variable in the script to point to the directory where your font files are located.

## Example

Here is an example output when running the script:

```
Processing eBooks: 100%|███████████████████████████████████████████████████| 5/5 [00:10<00:00, 0.5it/s]
Downloaded and converted: downloads/Book_Title.pdf
```

This indicates that the script has processed 5 eBooks and saved them as PDFs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
