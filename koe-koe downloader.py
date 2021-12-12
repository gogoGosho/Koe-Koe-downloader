from bs4 import BeautifulSoup
import requests, re, csv, os

# r = requests.get("<enter the autoplay link↙↙↙↙↙↙>").text
r = requests.get(
    "https://koe-koe.com/auto_play.php?word=%E3%81%8A%E3%81%AA%E3%81%AA&g=1"
).text

soup = BeautifulSoup(r, "lxml")
empy = []
for a in soup.find_all("a", href=True):
    empy.append(a["href"])
nameName = empy[4]
empy = empy[6:-16]
rdyforregex = list(dict.fromkeys(empy))


def listToString(s):
    str1 = " "
    return str1.join(s)


nameName = nameName.split("=")
nameName = nameName[1]
author = nameName[:-3]

convertedString = listToString(rdyforregex)

ids = re.findall(r"[0-9]+", convertedString)
if os.path.isfile(f"./{author}.csv") == False:
    outputFile = open(f"{author}.csv", "w", newline="", encoding="utf16")
    outputDictWriter = csv.DictWriter(
        outputFile, ["name", "title", "lenghtDate", "id", "randomParagraph"]
    )
    outputDictWriter.writeheader()
    outputFile.close()
for i in ids:
    linkka = f"https://koe-koe.com/detail.php?n={i}"
    furtherRequest = requests.get(linkka).text

    sosoup = BeautifulSoup(furtherRequest, "lxml")
    taitoru = sosoup.find("div", {"id": "content_body"}).h2.text
    linkkas = f"https://file.koe-koe.com/sound/upload/{i}.mp3"
    print(f"Saving: {author} {taitoru} {i}.mp3")
    wawawa = requests.get(linkkas)
    open(f"{author} {taitoru} {i}.mp3", "wb").write(wawawa.content)
    print(f"Saved: {author} {taitoru} {i}.mp3")
    try:
        lenghtAndDate = sosoup.select("#text > div:nth-child(2) > p:nth-child(2)")[
            0
        ].text
    except Exception as e:
        lenghtAndDate = None
    try:
        nameNshit = sosoup.select(
            "#text > div:nth-child(2) > p:nth-child(1) > span:nth-child(1) > a:nth-child(1)"
        )[0].text
    except Exception as e:
        nameNshit = f"{author}"
    try:
        paragraphDescr = list(
            sosoup.select("#text > div:nth-child(2) > p:nth-child(1)")[0]
        )
    except Exception as e:
        paragraphDescr = None
    with open(f"{author}.csv", "a", encoding="utf16", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([nameNshit, taitoru, lenghtAndDate, i, paragraphDescr])
