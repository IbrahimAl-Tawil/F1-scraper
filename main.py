import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://pitwall.app/drivers/archive/"
years = range(2010, 2025)  

all_data = []

for year in years:
    print(f"Scraping data for year {year}...")
    url = f"{base_url}{year}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table')  
        if table:
            headers = [th.text.strip() for th in table.find_all('th')]  
            rows = table.find_all('tr')[1:]
            
            for row in rows:
                cells = [td.text.strip() for td in row.find_all('td')]
                cells.append(year)  
                all_data.append(cells)
        else:
            print(f"No table found for {year}")
    else:
        print(f"Failed to fetch data for {year}. Status code: {response.status_code}")


columns = headers + ['Year'] 
df = pd.DataFrame(all_data, columns=columns)


df.to_csv('f1_drivers_data.csv', index=False)
print("Data saved to 'f1_drivers_data.csv'")
