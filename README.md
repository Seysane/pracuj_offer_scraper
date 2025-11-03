<h1 align="center">Pracuj.pl Job Offer Scraper</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12.7-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Playwright-1.49-2EAD33" />
  <img src="https://img.shields.io/badge/BeautifulSoup-4.12-6BAF92" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" />
  <img src="https://img.shields.io/badge/Status-Active-success.svg" />
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/Seysane/pracuj_offer_scraper.svg" />
  <img src="https://img.shields.io/github/forks/Seysane/pracuj_offer_scraper.svg" />
  <img src="https://img.shields.io/github/issues/Seysane/pracuj_offer_scraper.svg" />
  <img src="https://img.shields.io/github/last-commit/Seysane/pracuj_offer_scraper.svg" />
</p>

<p align="center"><i>Automated job offer scraper for Pracuj.pl built with Playwright and BeautifulSoup.</i></p>


---

## 📚 Table of Contents
- [About](#about)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Example Output](#example-output)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Future Improvements](#future-improvements)
- [FAQ](#faq)
- [License](#license)

---

## 🧠 About
This project is a Python-based scraper that collects job listings from Pracuj.pl based on a keyword entered by the user (e.g. "Python", "JavaScript", etc.).
It uses **Playwright** to render dynamic content and **BeautifulSoup** to parse the extracted HTML.

The results are saved as:
- CSV (sorted by company name)
- JSON (grouped by company)

---

## ⚙️ Features
- ✅ Scrapes job offers for any user-defined keyword
- 🧩 Uses Playwright to handle dynamically rendered content
- 📊 Exports results to CSV (sorted) and JSON (grouped by company)
- 🔠 Automatically sorts CSV output alphabetically by company name
- 🕒 Includes timestamps in filenames

---

## 📌 Requirements
- Python **3.11+** (tested on 3.12.7)
- Playwright installed with Chromium (see installation)
- Requires internet access — the scraper does not use cached data.

---

## 🛠️ Installation
```bash
# Clone the repository
git clone https://github.com/Seysane/pracuj_offer_scraper.git
cd pracuj_offer_scraper
```
```bash
# Create and activate a virtual environment
python -m venv env
source env/bin/activate   # macOS/Linux
env\Scripts\activate      # Windows
```
```bash
# Install dependencies
pip install -r requirements.txt
```
```bash
# Install Chromium for Playwright (required!)
playwright install chromium
# Or
playwright install  # installs Chromium, Firefox, WebKit
```

---

## 🚀 Usage
To run the scraper, execute:

```bash
python main.py
```

You will be prompted to enter a keyword (e.g. `python`, `java`, `remote`, `junior`), and the scraper will automatically collect all job offers matching the keyword you entered.

The scraper will:

- Load all job offers from Pracuj.pl that match the keyword in title, description etc.
- Extract and parse job data from internal JSON
- Save results into:

  - `CSV_DATA/` → **CSV file sorted alphabetically by company**
  - `JSON_DATA/` → **JSON file grouped by company**

---

## 📂 Project Structure
```
pracuj_offer_scraper/
├── CSV_DATA/                        # Contains all generated CSV files
├── JSON_DATA/                       # Contains all grouped JSON files
├── main.py                          # Main scraper script
├── requirements.txt                 # Python dependencies
└── README.md                        # Documentation
```

---

## 🧾 Example Output

### 📄 CSV Example (exported file sample)
```
company,title,location,link,salary
EPAM Systems,Azure Engineering Manager,Kraków,https://www.pracuj.pl/...,"No information provided"
Sii Sp. z o.o.,Python Automation Tester,Gdańsk,https://www.pracuj.pl/...,"-"
```
(Example of exported dataset sorted by company)

### 📦 JSON Example (grouped by company)
```json
{
        "company": "Google",
        "offers": [
            {
                "title": "Software Engineer II - YouTube Ads",
                "location": "Warszawa, Śródmieście",
                "link": "https://www.pracuj.pl/praca/software-engineer-ii-youtube-ads-warszawa-emilii-plater-53,oferta,1004410373",
                "salary": "No information provided"
            },
            {
                "title": "Senior Software Engineer - Android ML Services",
                "location": "Kraków",
                "link": "https://www.pracuj.pl/praca/senior-software-engineer-android-ml-services-krakow,oferta,1004410339",
                "salary": "No information provided"
            }
        ]
    }
```
(Example of exported grouped dataset sorted by company)

---

## 📸 Screenshots

### CSV Output Preview
![CSV Preview](screenshots/csv_preview.png)

### JSON Output Preview
![JSON Preview](screenshots/json_preview.png)

### Terminal Run Example
![Terminal Output](screenshots/terminal_run.png)

---

## 🧩 Tech Stack
- 🐍 Python 3.12.7	- Core programming language (tested on 3.12.7)
- 🎭 [Playwright](https://playwright.dev/) – Browser automation (headless Chromium)
- 🍜 [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) – Parsing HTML content
- 🧮 pandas	        - Data manipulation and CSV export
- 📦 json	        - Grouped output format
- 🕒 datetime	    - Timestamp generation for files

---

## 🔮 Future Improvements
- Add CLI flags (`--keyword`, `--no-csv`, `--max-pages`)
- Add filtering (remote only, salary range, location)
- Add option to export to Excel or database

---

## ❓ FAQ

### Is scraping Pracuj.pl legal?
> No scraper can guarantee full compliance with site policies — you should use it **only for publicly available data** and respect the terms of use. ⚠️ This tool is intended for educational and research purposes only.

**Important:**  
- See the site's crawler rules in the [`robots.txt`](https://www.pracuj.pl/robots.txt) file.
- If a path is explicitly disallowed (e.g., `Disallow: /_scripts/`), scraping that path might violate the site’s intent — you should avoid scraping disallowed directories.  
- Always check the current Terms & Conditions of Pracuj.pl; they might restrict automated access.  
- Use a reasonable request rate to **avoid overloading the server** and potentially being blocked.

### Why Playwright instead of requests?
> Pracuj.pl dynamically loads job offers via JavaScript, so static requests (requests/selenium) are not enough — Playwright is required to render full content.

### Does the scraper bypass login or access private data?
> No. It only collects publicly available job listings and does not log into any user account.

### Can I run this on Windows / Linux / macOS?
> Yes — Playwright supports all major operating systems.

### What happens if Pracuj.pl changes layout or API?
> Selectors may break — updates may be required.

### Can this scraper be used for commercial purposes?
> Yes, but only if you comply with Pracuj.pl’s Terms of Service and the MIT license of this project.

---

## ⚖️ License
This project is licensed under the **MIT License**.  
See the `LICENSE` file for full details.

📄 This project is open-source and released under the **MIT License** — free to use, modify and distribute.

---

## 👨‍💻 Author

Created by **Sebastian Siciński**
📧 [itsbastian.kontakt@gmail.com](mailto:itsbastian.kontakt@gmail.com) 
🔗 [LinkedIn](https://www.linkedin.com/in/sebastian-sici%C5%84ski-b74096243/)
🐙 [GitHub](https://github.com/Seysane)

---

⭐ If you find this project useful, consider giving it a star!

---

[🔼 Back to top](#pracujpl-job-offer-scraper)