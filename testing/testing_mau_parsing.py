import os
from datetime import date, timedelta

import requests
import bs4
import json
import re
import time


def prepare_string(string: str, spec_symbols: str) -> str:
    for sym in spec_symbols:
        pattern = rf"\{sym}"
        string = re.sub(pattern, rf"\{sym}", string)

    return string


course = 3
institute = "ИГ и СН"
group = prepare_string("БПО-АН-21", "()")

# получение значения института для query-параметра facs
base_schedule_url = "https://www.mauniver.ru/student/timetable/new/"
base_schedule_page_response = requests.get(base_schedule_url)
soup = bs4.BeautifulSoup(base_schedule_page_response.content, "lxml")

date_select = soup.find("option", selected=True)
pers = date_select.get("value")

institute_select = soup.find("option", string=institute)
facs = institute_select.get("value")

# получение страницы групп
params = {
    "facs": facs,
    "courses": course,
    "mode": 1,
    "pers": pers,
}
r = requests.get(base_schedule_url, params=params)
soup = bs4.BeautifulSoup(r.content, "lxml")
a_tag = soup.find("a", string=re.compile(rf"\s*?{group}\s*?"))
group_schedule_url = os.path.join(base_schedule_url, a_tag.get("href"))

# получение всех необходимых данных
start_date = date.today()
end_date = start_date + timedelta(days=7)
params = {
    "perstart": start_date.strftime("%Y-%m-%d"),
    "perend": end_date.strftime("%Y-%m-%d"),
}
group_page_response = requests.get(group_schedule_url, params=params)
soup = bs4.BeautifulSoup(group_page_response.content, "lxml")

data = {}

for day_num, day in enumerate(soup.find_all("table")):
    title = day.find("th")
    if title:
        data.setdefault(title.text, [])

    for row_num, row in enumerate(day.find_all("tr")[1:]):
        data[title.text].append([field.text for field in row.find_all(["th", "td"])])

with open("schedule_data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
