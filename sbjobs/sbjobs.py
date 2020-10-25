import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
            # direct_link = f"https://boards.greenhouse.io/embed/job_app?for=apeelsciences&token={job_id}&b=https://www.apeel.com/careers"
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


def carpe_jobs():
    #jazzhr javascript entries
    url = "https://app.jazz.co/widgets/basic/create/carpe"
    # url = "https://carpe.io/company/careers"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())
    jobs = soup.find_all('div')#, {'id':'resumator-jobs', 'class':'resumator-job-text'})
    for job in jobs:
        print(job)


def procore_job():
    procore_url = "https://www.procore.com/jobs/openings"
    r = requests.get(procore_url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    jobs = soup.find_all("tr", class_="c-filter-items clickable filterable")

    with open("joblistings/procore_jobs.csv", "w", newline="") as r:
        fieldnames = ["timestamp", "job_id", "link", "location", "title"]
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
                            "title": titl.text.strip(),
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


def evidation_jobs():
    url = "https://boards-api.greenhouse.io/v1/boards/evidation/jobs"
    response = requests.get(url)
    response.raise_for_status()
    results = response.json()
    with open("joblistings/evidation_job.csv", "w") as writefile:
        fieldnames = ["timestamp", "job_id", "link", "location", "position"]
        writer = csv.DictWriter(
            writefile, fieldnames=fieldnames, delimiter=",", lineterminator="\n"
        )
        writer.writeheader()
        for job in results["jobs"]:
            writer.writerow(
                {
                    "timestamp": datetime.today(),
                    "link": job["absolute_url"],
                    "job_id": job["internal_job_id"],
                    "location": job["location"]["name"],
                    "position": job["title"],
                }
            )


def well_jobs():
    """
       <div class="col-lg-5 offset-lg-1">
    <h3 class="color-blue">
     Client Success
    </h3>
    <div class="name color-black">
     <!--<a href="/careers/position?gh_jid=4903504002">Business Analyst</a>-->
     <a href="/careers/apply?gh_jid=4903504002">
      Business Analyst
     </a>
    </div>
    """
    url = "https://wellapp.com/careers/"
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    # create writer

    # go through soup
    blocks = soup.find_all("div", class_="col-lg-5 offset-lg-1")
    with open("joblistings/well_job.csv", "w") as writefile:
        writefile = csv.writer(writefile)
        writefile.writerow(["timestamp", "job_id", "link", "location", "title"])
        for block in blocks:
            for job in block.find_all("div", {"class": "name color-black"}):
                link = url + job.a["href"]
                job_id = link.split("=")[-1]
                position = job.a.text.strip()
                location = None  # block.find('div', {'class':'location'})
                writefile.writerow([datetime.today(), job_id, link, location, position])


def cj_jobs():
    url = "https://careers.smartrecruiters.com/PublicisGroupe/cj"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("li", class_="opening-job job column wide-7of16 medium-1of2")
    with open("joblistings/cj_job.csv", "w") as writefile:
        writefile = csv.writer(writefile)
        writefile.writerow(["timestamp", "job_id", "link", "location", "title"])
        for job in jobs:
            link = job.a["href"].split("?")[0]
            job_id = link.split("-")[0].split("/")[-1]
            title = job.h4.text
            location = None if not job.i else job.i["title"]

            writefile.writerow([datetime.today(), job_id, link, location, title])


def hg_jobs():
    url = "https://boards.greenhouse.io/embed/job_board?for=hginsights&b=https://hginsights.com/careers/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    # there might be multiple jobs within the section tag in the future
    jobs = soup.find_all("section", class_="level-0")
    with open("joblistings/hg_job.csv", "w") as writefile:
        writefile = csv.writer(writefile)
        writefile.writerow(["timestamp", "job_id", "link", "location", "title"])
        for job in jobs:
            # also has dept and office ids 
            job_id = job.a["href"].split("=")[-1]
            link = job.a["href"]
            # direct_link = f"https://boards.greenhouse.io/embed/job_app?for=hginsights&token={job_id}&b=https://hginsights.com/current-openings/"
            job_id = link.split("=")[-1]
            title = job.a.text
            location = job.span.text.strip()

            writefile.writerow([datetime.today(), job_id, link, location, title])


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
