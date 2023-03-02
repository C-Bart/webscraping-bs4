import requests
from bs4 import BeautifulSoup


base_url = "https://subslikescript.com/"
url = f"{base_url}movies_letter-A"
response = requests.get(url)
content = response.text

soup = BeautifulSoup(content, 'lxml')

pagination = soup.find("ul", class_="pagination")
pages = pagination.find_all("li", class_="page-item")
last_page = int(pages[-2].text)

links_to = []
for page in range(1, last_page+1):
    new_url = f"{url}?page={page}"
    response = requests.get(new_url)
    content = response.text
    soup = BeautifulSoup(content, 'lxml')

    box = soup.find("article", class_="main-article")
    links = box.find_all('a', href=True)

    for link in links:
        links_to.append(link['href'])

    for link in links_to:
        url = f"{base_url}{link}"
        response = requests.get(url)
        content = response.text
        soup = BeautifulSoup(content, 'lxml')
        box = soup.find("article", class_="main-article")
        title = box.find("h1").text
        transcript = box.find("div", class_="full-script").get_text(separator=" ", strip=True)

        with open(f"titles/{title}.txt", "w", encoding="utf-8") as file:
            file.write(transcript)
