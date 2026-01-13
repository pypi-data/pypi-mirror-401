import requests
import pandas as pd
import re
from bs4 import BeautifulSoup


def scrape_surf_report(url: str, output_csv: str) -> pd.DataFrame:
    """
    Scrape surf data from surf-report.com and save it to a CSV file.

    Parameters
    ----------
    url : str
        Surf-report URL (e.g. Lacanau, Carcans, Moliets)
    output_csv : str
        Path where the CSV file will be saved

    Returns
    -------
    pandas.DataFrame
        Extracted surf conditions
    """

    response  = requests.get(url)
    response.raise_for_status()
    print("Connection OK")
    
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("div", class_="forecast-tab")
    lines = soup.find_all('div', class_='line')
    # It is this list of dictionaries that will contain everything
    all_data = []

    for table in tables:
        # 1. Day recovery (e.g., "Friday, January 9")
        title_div = table.find("div", class_=re.compile("title"))
        day = title_div.get_text(strip=True) if title_div else "Inconnu"

        # 2. Retrieving data rows (skipping the header)
        lines = table.find_all("div", class_="line")[1:]

        for line in lines:
            cells = line.find_all("div", class_=re.compile("cell"))
            if len(cells) < 5:
                continue

            # Time extraction
            hour = cells[0].get_text(strip=True)

            # Wave extraction
            wave = cells[2].get_text(strip=True)

            # Extraction of wind direction (via the image's alt attribute)
            direction_div = line.find("div", class_=re.compile(r"wind.*img"))
            direction = None
            if direction_div:
                img = direction_div.find("img")
                if img:
                    direction = img.get("alt")

            # Wind speed extraction
            speed_div = line.find("div", class_=re.compile("large-bis-bis"))
            speed = speed_div.get_text(strip=True) if speed_div else "N/C"

            # --- ASSOCIATION: We are creating a dictionary for this line ---
            row = {
                "Jour": day,
                "Heure": hour,
                "Taille Vagues": wave,
                "Vitesse Vent(km/h)": speed,
                "Direction Vent": direction
            }
            
            # We add this line to our global list
            all_data.append(row)

    # --- CONVERSION TO DATAFRAME ---
    df = pd.DataFrame(all_data)
    df.to_csv(output_csv, index=False, encoding="utf-8")

    return df
