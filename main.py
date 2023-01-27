from bs4 import BeautifulSoup
import requests

def getSoup(www):
    return BeautifulSoup(requests.get(www).text, "lxml")

wbijamWWW = "https://b.wbijam.pl/pierwsza_seria.html"
searchPhrase = wbijamWWW.rsplit("/")[-1].rsplit(".")[0] 		# zwraca pierwsza_seria
soup = getSoup(wbijamWWW)									# funkcja zwraca bf
linksMainPage = soup.find_all("a", href=True)				# szukam wszystkich linków ze strony pierwsza_seria
for linkTagMainPage in reversed(linksMainPage):
    episodeShortURL = linkTagMainPage.get("href")
    if episodeShortURL.startswith(searchPhrase + "-"):							#sprawdza czy link jest odcinkiem
        episodeNumber = episodeShortURL.rsplit("-", 1)[-1].rsplit(".")[0]	#numer odcinka
        episodeURL = wbijamWWW.replace(wbijamWWW.rsplit("/")[-1], "") + episodeShortURL		
        soup = getSoup(episodeURL)
        tabela = soup.find_all("table", class_="lista")
        for link in tabela:
            rows = link.findAll("tr")
            for row in rows:
                if row.text.find("cda") > -1:
                    videoWbijamCode = row.find("span", rel=True).get("rel")
                    wbijamCdaURL = (wbijamWWW.replace(wbijamWWW.rsplit("/")[-1], "")+"odtwarzacz-"+ videoWbijamCode+".html")
                    soup = getSoup(wbijamCdaURL)
                    cdaWbijamTag = soup.find("iframe", src=True).get("src")
                    cdaFinallCode = cdaWbijamTag.rsplit("/")[-1]
                    print("Odcinek numer: "+episodeNumber+" Link: "+"https://www.cda.pl/video/"+cdaFinallCode)

    else:
        print("Zły url")
