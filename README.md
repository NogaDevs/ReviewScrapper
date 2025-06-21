# ikyu-review-scraper

This project includes a Scrapy spider and a Python parser for extracting and processing hotel reviews from **ikyu.com**. The goal is to collect, structure, and store review data from a specific hotel, making further analysis easy.

## Project Structure

- **ikyuspider.py**: Scrapy spider to download HTML review pages.
- **parser.py**: Script to process, extract, and save the reviews in JSON and CSV formats.

---

## 1. Requirements

- Python 3.8+
- Scrapy
- pandas

Install the main dependencies with:

```bash
pip install scrapy pandas
```

---

## 2. How it works

### a) Review Extraction (Spider)

The spider (`ikyuspider.py`):

- Generates URLs for the review pages based on a fixed pattern.
- Downloads the HTML of each review page.
- Saves each HTML file under a date-structured folder: `parsed_files/YYYY-MM-DD/html/`.

### b) Data Processing (Parser)

The parser (`parser.py`):

- Loads the downloaded HTML files.
- Extracts review blocks and translates rating labels.
- Calculates the average rating per review.
- Saves the processed data as:
  - **JSON** files (one per page).
  - A consolidated **CSV** file for further analysis.
- All results are saved in `parsed_files/YYYY-MM-DD/json/` and `parsed_files/YYYY-MM-DD/ikyu_reviews.csv`.

---

## 3. Usage

### Step 1: Run the spider

Before running the spider, find the hotel URL and change it in the spider.
Run the spider using Scrapy. Make sure you are in the project root directory:

```bash
scrapy runspider ikyuspider.py
```

This will download all the required HTML files.

### Step 2: Process the data

Then, run the parser:

```bash
python parser.py
```

This will extract the reviews, calculate averages, and save JSON and CSV files.

---

## 4. Output

- **HTML files**: `/parsed_files/YYYY-MM-DD/html/ikyu-review-pN.html`
- **JSON files**: `/parsed_files/YYYY-MM-DD/json/ikyu-review-pN.json`
- **CSV file**: `/parsed_files/YYYY-MM-DD/ikyu_reviews.csv`

Each processed review includes:
- Publication date
- Ratings per category (room, equipment, service, meal, bath, satisfaction)
- Average score

---

## 5. Customization

- The parser is tailored for the HTML structure and Japanese labels from ikyu.com reviews. If the website structure changes, you may need to adjust the extraction patterns.
- You can change the number of pages to download/process by editing the `range(13)` value in both scripts.

---

## 6. Credits and Contact

This project was developed as a scraping and data analysis exercise for hotel reviews.  
For questions or suggestions, open an **Issue** or contact the repository owner.

---
