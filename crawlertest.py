import schedule
import time
from bs4 import BeautifulSoup
import requests
import datetime

def check_for_new_cve():
    url = "https://www.cvedetails.com/vulnerability-list/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    cve_table = soup.find("table", class_="searchresults sortable")
    cve_rows = cve_table.find_all("tr")

    num_cve_previous = len(cve_rows)


    params = {
        "startdate": datetime.date.today().isoformat(),
        "order": "2"
    }
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")

    cve_table = soup.find("table", class_="searchresults sortable")
    cve_rows = cve_table.find_all("tr")

    num_cve_current = len(cve_rows)
    if num_cve_previous < num_cve_current:
        new_cve_count = num_cve_current - num_cve_previous
        print(f"new cve: {new_cve_count}")
        
    else:
        print("No change found:(")


schedule.every(60).minutes.do(check_for_new_cve)

while True:
    schedule.run_pending()
    time.sleep(1)
