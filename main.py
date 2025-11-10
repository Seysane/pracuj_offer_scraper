import json, time , os
import pandas as pd
import datetime as dt
import argparse

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from collections import defaultdict

class CustomHelpFormatter(argparse.HelpFormatter):
    def __init__(self, *args, **kwargs):
        kwargs['max_help_position'] = 30
        kwargs['width'] = 100
        super().__init__(*args, **kwargs)

parser = argparse.ArgumentParser(
    description="Pracuj.pl Job Offer Scraper",
    formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=30, width=100),
    epilog=(
        "\nExamples:\n"
        "  python main.py --keyword python --max-pages 3 --no-json\n"
        "  python main.py --keyword java\n"
        "  python main.py               # interactive mode"
    )
)
parser.add_argument("--keyword", type=str, help="Keyword to search for (e.g. python, java)")
parser.add_argument("--max-pages", type=int, help="Maximum num of pages to scrape (optional)")
parser.add_argument("--no-json", action="store_true", help="Skip saving JSON output")
parser.add_argument("--no-csv", action="store_true", help="Skip saving CSV output")
args = parser.parse_args()

if args.keyword:
    keyword = args.keyword
else:
    keyword = input("Enter keyword to search for: ").strip()

max_pages = args.max_pages
save_json = not args.no_json
save_csv = not args.no_csv

os.makedirs("CSV_DATA", exist_ok=True)
os.makedirs("JSON_DATA", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    offers_data = []

    page_num = 1
    while True:
        if max_pages and page_num > max_pages:
            print(f"\nReached max page limit ({max_pages}).")
            break

        url = f"https://www.pracuj.pl/praca/{keyword};kw?pn={page_num}"
        print(f"⏳ Opening page {page_num}...")
        page.goto(url, timeout=120000)
        page.wait_for_selector("script#__NEXT_DATA__",state="attached", timeout=30000)
        print(f"✅ Page {page_num} loaded!")
        time.sleep(1)

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        script_tag = soup.find("script", id="__NEXT_DATA__")

        if not script_tag:
            print("⚠️ No __NEXT_DATA__ found, stopping scraper.")
            break

        data = json.loads(script_tag.string)
        page_props = data["props"]["pageProps"]
        dehydrated = page_props["dehydratedState"]
        queries = dehydrated.get("queries", [])

        if queries:
            first_query_state = queries[0].get("state", {})
            data_inside = first_query_state.get("data", {})

        grouped_offers = data_inside.get("groupedOffers", [])

        if not grouped_offers:
            print(f"⚠️ No offers found on page {page_num}, stopping scraper.")
            break

        for group in grouped_offers:
            offer = {
                "company": group.get("companyName"),
                "title": group.get("jobTitle"),
                "location": None,
                "link": None,
                "salary": group.get("salaryDisplayText"),
            }

            suboffers = group.get("offers", [])
            if suboffers:
                offer["link"] = suboffers[0].get("offerAbsoluteUri")
                offer["location"] = suboffers[0].get("displayWorkplace")

            if not offer["link"]:
                offer["link"] = group.get("companyProfileAbsoluteUri")

            offers_data.append(offer)

        page_num += 1
        
if not offers_data:
    print("❌ No offers found.")
    exit()

today_date = dt.datetime.today().strftime("%d-%m-%Y")

if save_csv:
    df = pd.DataFrame(offers_data)
    df_sorted = df.sort_values(by="company")
    csv_path = f"CSV_DATA/pracuj_offers_{keyword}_{today_date}.csv"
    df_sorted.to_csv(csv_path, mode='a', index=False, encoding="utf-8-sig")
    print(f"\n💾 Saved {len(df)} offers to {csv_path} file.")

if save_json:
    grouped_data = defaultdict(list)
    for offer in offers_data:
        company = offer["company"]
        no_info = "N/A"
        grouped_data[company].append({
            "title": offer["title"] or no_info,
            "location": offer["location"] or no_info,
            "link": offer["link"] or no_info,
            "salary": offer["salary"] or no_info,
        })

    json_data = [{"company": c, "offers": o} 
                for c, o in sorted(grouped_data.items(), key=lambda x: x[0].lower())]

    json_path = f"JSON_DATA/pracuj_offers_grouped_{keyword}_{today_date}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    print(f"💾 Saved {len(json_data)} grouped offers to {json_path} file.")

print("\n Scraping complete.")