import json
import re

from bs4 import BeautifulSoup
import requests

BASE_URL = "https://www.u-tokyo.ac.jp"
JOBS_PATH = "/focus/ja/jobs/"
jobs_url = BASE_URL + JOBS_PATH


def normalize_url(url):
    if url.startswith("/"):
        return BASE_URL + url
    return url


def truncate_spaces(text):
    return re.sub(r"\s{2,}", ",", text)


req = requests.get(jobs_url)
req.encoding = req.apparent_encoding

soup = BeautifulSoup(req.text, "html.parser")
table = soup.find("table")
rows = table.find_all("tr")

jobs = []

for row in rows[1:]:
    columns = row.find_all("td")
    job_type = truncate_spaces(columns[0].text.strip())
    job_url = normalize_url(columns[1].find("a")["href"])
    columns[1].find("p").decompose()
    job_position = truncate_spaces(columns[1].text.strip())
    job_deadline = truncate_spaces(columns[2].text.strip())
    job_posted = truncate_spaces(columns[3].text.strip())
    job_department = truncate_spaces(columns[4].text.strip())
    job_organization = truncate_spaces(columns[5].text.strip())

    jobs.append({
        "type": job_type,
        "position": job_position,
        "deadline": job_deadline,
        "posted": job_posted,
        "department": job_department,
        "organization": job_organization,
        "url": job_url
    })

with open("jobs_ja.json", "w") as f:
    json.dump(jobs, f, ensure_ascii=False, indent=4)
