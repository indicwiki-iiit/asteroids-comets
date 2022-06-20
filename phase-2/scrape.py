import requests
from bs4 import BeautifulSoup
import re
import time
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    text = TAG_RE.sub(' ', text)
    text = re.sub('\s+',' ',text)
    return text

for num in range(8997, 109000):
    URL = "https://in-the-sky.org/data/object.php?id=A" + str(num)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup)
    results = soup.find_all("div", class_="objinfo")
    # print(type(results))
    result = []
    for r in results:
        print(remove_tags(str(r)))
    time.sleep(5)
        # result.extend(th.find_all(text='objinfo'))