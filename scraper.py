import json, re, datetime, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

SOURCES = [
 ("SSC","https://ssc.gov.in"),("UPSC","https://upsc.gov.in"),
 ("Railways","https://indianrailways.gov.in"),("IBPS","https://ibps.in"),
 ("SBI","https://sbi.co.in/web/careers"),("Army","https://joinindianarmy.nic.in"),
 ("NTA","https://nta.ac.in"),("CTET","https://ctet.nic.in"),
 ("BPSC","https://bpsc.bihar.gov.in"),("BSSC","https://bssc.bihar.gov.in"),
 ("UPPSC","https://uppsc.up.nic.in"),("MPSC","https://mpsc.gov.in"),
 ("RPSC","https://rpsc.rajasthan.gov.in"),("TNPSC","https://tnpsc.gov.in"),
 ("HPSC","https://hpsc.gov.in"),("JPSC","https://jpsc.gov.in"),
]
KEY = re.compile(r"recruit|vacanc|notification|admit card|result|answer key|apply online|advertisement|exam", re.I)
BAD = re.compile(r"tender|rti\b|privacy|contact|sitemap|feedback|tel:|mailto:|javascript", re.I)
HEAD = {"User-Agent": "Mozilla/5.0 (compatible; JobsBot/1.0)"}
today = datetime.date.today().isoformat()

try:
    items = json.load(open("updates.json"))
except Exception:
    items = []
seen = {i["url"] for i in items}

for name, base in SOURCES:
    try:
        r = requests.get(base, headers=HEAD, timeout=25, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        added = 0
        for a in soup.find_all("a", href=True):
            t = " ".join(a.get_text().split())
            u = urljoin(base, a["href"])
            if not (12 <= len(t) <= 150) or not u.startswith("http"):
                continue
            if not KEY.search(t) or BAD.search(t + u) or u in seen:
                continue
            items.append({"title": t, "url": u, "source": name, "date": today})
            seen.add(u); added += 1
            if added >= 8: break
        print(name, "added", added)
    except Exception as e:
        print(name, "failed:", e)

items.sort(key=lambda i: i["date"], reverse=True)
json.dump(items[:200], open("updates.json", "w"), indent=1, ensure_ascii=False)
