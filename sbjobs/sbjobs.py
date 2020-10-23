import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

job = "https://boards.greenhouse.io/embed/job_app?for=apeelsciences&token=2405361&b=https://www.apeel.com/careers"
app = "https://jobs.jobvite.com/appfolio/jobs/"
jb2 = "https://jobs.jobvite.com/appfolio/jobs/o9abdfwr"


def apeel_jobs():
    url = "https://boards.greenhouse.io/embed/job_board?for=apeelsciences&b=https://www.apeel.com/careers"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    with open("joblistings/apeel_jobs.csv", "w") as apeel:
        writer = csv.writer(apeel)
        writer.writerow(
            [
                "timestamp",
                "job_id",
                "link",
                # "dept_id", "office_id",
                "location",
                "title",
            ]
        )
        for opening in soup.find_all("div", class_="opening"):
            dept_id = opening.attrs["department_id"]
            office_id = opening.attrs["office_id"]
            anchor = opening.find("a")
            link = anchor.attrs["href"]
            job_id = link.split("=")[1]
            title = anchor.text
            location = opening.find("span").text.strip()
            writer.writerow(
                [
                    datetime.today(),
                    job_id,
                    link,
                    # dept_id, office_id,
                    location,
                    title,
                ]
            )


def appfolio_jobs():
    url = "https://jobs.jobvite.com/appfolio/jobs/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    listing = soup.find_all("tr")  # , class_="jv-job-list")
    with open("joblistings/appfolio_job.csv", "w") as writefile:
        writefile = csv.writer(writefile)
        writefile.writerow(["timestamp", "job_id", "link", "location", "title"])
        for lists in listing:
            postings = lists.find("td", class_="jv-job-list-name")
            anchor = postings.find(
                "a",
            )
            link = anchor.attrs["href"]
            position = anchor.text
            location = " ".join(
                lists.find("td", class_="jv-job-list-location").text.split()
            )

            writefile.writerow(
                [
                    datetime.today(),
                    link.split("/")[-1],
                    "https://jobs.jobvite.com" + link,
                    location,
                    position,
                ]
            )


def procore_job():
    procore_url = "https://www.procore.com/jobs/openings"
    r = requests.get(procore_url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    jobs = soup.find_all("tr", class_="c-filter-items clickable filterable")

    with open("joblistings/procore_jobs.csv", "w", newline="") as r:
        fieldnames = ["timestamp", "job_id", "link", "location", "position"]
        writer = csv.DictWriter(
            r, fieldnames=fieldnames, delimiter=",", lineterminator="\n"
        )
        writer.writeheader()
        for job in jobs:
            title = job.find_all("p", class_="careers-title")
            location = job.find_all("p", class_="careers-location")
            for titl in title:
                for cities in location:
                    writer.writerow(
                        {
                            "position": titl.text.strip(),
                            "link": str("https://www.procore.com" + titl.a["href"]),
                            "job_id": titl.a["href"].split("/")[-1],
                            "location": cities.text.strip(),
                            "timestamp": datetime.today(),
                        }
                    )


def logicmonitor_jobs():
    logic_url = (
        "https://www.logicmonitor.com/wp-content/plugins/greenhouse/test_ajax.php"
    )
    param = {
        "f_key": "ACC043547019B9220376DFB78052DE72ACC695108C21281991DCFA78486FC177",
        "dep_val": "all",
        "loc_val": "all",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Referer": "https://js.driftt.com/deploy/assets/index.html",
    }

    r = requests.post(logic_url, headers=headers, data=param)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")
    with open("joblistings/logicmonitor_job.csv", "w") as writefile:
        writefile = csv.writer(writefile)
        writefile.writerow(["timestamp", "job_id", "link", "location", "title"])
        for job in soup.find_all("div", class_="row cool-link"):
            anchor = job.find("a")
            link = anchor.attrs["href"]
            job_id = link.split("=")[-1]
            position = anchor.find("h4").text
            location = job.find("i", class_="n-m-loc").text
            writefile.writerow([datetime.today(), job_id, link, location, position])


def invoca_jobs():
    url = "https://boards.greenhouse.io/embed/job_board?for=invoca&b=https://www.invoca.com/company/careers"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("div", class_="opening")
    with open("joblistings/invoca_job.csv", "w") as writefile:
        writefile = csv.writer(writefile)
        writefile.writerow(["timestamp", "job_id", "link", "location", "title"])
        for job in jobs:
            anchor = job.find("a")
            link = anchor.attrs["href"]
            job_id = link.split("=")[-1]
            location = job.find("span", class_="location").text.strip()
            position = anchor.text
            writefile.writerow([datetime.today(), job_id, link, location, position])


def job_desc_text(url):
    """Scrapes the text of job description from given link

    Args:
        url ([type]): [description]

    Returns:
        [type]: [description]
    """
    # url = f"https://boards.greenhouse.io/embed/job_app?for=apeelsciences&token={link}&b=https://www.apeel.com/careers"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
    }
    response = requests.get(url, headers=headers).text
    job_desc_text = BeautifulSoup(response, "html.parser").text.replace("\n", " ")
    return job_desc_text


if __name__ == "__main__":
    appfolio_jobs()
 