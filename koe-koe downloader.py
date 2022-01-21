from bs4 import BeautifulSoup
import requests, re, csv, os, glob
from datetime import datetime 
# from pathlib import Path # from pathlib import Path  # enable this if you wanna have a main folder for koe-koe and this + line 36 onwards will make subfolders automatically


# r = requests.get("<enter the autoplay link↙↙↙↙↙↙>").text
r = requests.get("https://koe-koe.com/auto_play.php?word=%E3%82%8C%E3%82%93&g=1").text
dateToday = datetime.today().strftime("%Y-%m-%d")
soup = BeautifulSoup(r, "lxml")
empy = []
for a in soup.find_all("a", href=True):
    empy.append(a["href"])
nameName = empy[4]


def listToString(s):
    str1 = " "
    return str1.join(s)


empy2 = listToString(empy)
empy3 = re.findall(r"\b\d{4,6}\b", empy2)


rdyforregex = list(dict.fromkeys(empy3))


nameName = nameName.split("=")
nameName = nameName[1]
author = nameName[:-3]

# if you ever feel like not saving them in the current directory, change "pathtomain" to the main folder's path
# name your main folder "Koe-Koe folder" or whatever, and this will automatically make the subfolders for each
# new user, and will download all the missing audios from said user

# pathtomain = r"shift right on a folder and click "Copy as path" "
# pathtomain =r"D:\Koe-Koe folder" #for example
# os.chdir(pathtomain)
# try:
#     if os.path.exists(f"{pathtomain}/{author}") == False:
#         os.mkdir(f"{author}")
#     else:
#         pass
# except FileExistsError as e:
#     pass
# newdir = Path(os.path.join(pathtomain, f"{author}"))
# os.chdir(newdir)


listFromTheDirectory = []
for file in glob.glob("*.mp3"):
    listFromTheDirectory.append(file)
turnedtoString = listToString(listFromTheDirectory)
listToString(turnedtoString)

idsFromDirectory = re.findall(r"\b\d{4,6}\b", turnedtoString)


convertedString = listToString(rdyforregex)

ids = re.findall(r"\b\d{4,6}\b", convertedString)
if os.path.isfile(f"./{author}.csv") == False:
    outputFile = open(f"{author}.csv", "w", newline="", encoding="utf16")
    outputDictWriter = csv.DictWriter(
        outputFile,
        ["id", "name", "title", "lenghtDate", "dateToday", "randomParagraph"],
    )
    outputDictWriter.writeheader()
    outputFile.close()

compareOldAndNewDownloadNew = list(set(ids).difference(idsFromDirectory))

lines = open(f"{author}.csv", "r", encoding="utf16").read()


for i in ids:
    if i in compareOldAndNewDownloadNew:
        linkka = f"https://koe-koe.com/detail.php?n={i}"
        furtherRequest = requests.get(linkka).text

        sosoup = BeautifulSoup(furtherRequest, "lxml")
        taitaitle = sosoup.find("div", {"id": "content_body"}).h2.text
        taitoru = re.sub(r'[\\/:"*?<>|]+', "", taitaitle)
        if int(i) > 161334:
            linkkas = f"https://file.koe-koe.com/sound/upload/{i}.mp3"
            print(f"Saving: {author} {taitoru} {i}.mp3")
            wawawa = requests.get(linkkas)
            open(f"{author}  {taitoru} [{i}].mp3", "wb").write(wawawa.content)
            print(f"Saved: {author} {taitoru} {i}.mp3\n")
        elif int(i) < 161334:
            linkkas = f"https://file.koe-koe.com/sound/old/{i}.mp3"
            print(f"Saving: {author} {taitoru} {i}.mp3")
            wawawa = requests.get(linkkas)
            open(f"{author}  {taitoru} [{i}].mp3", "wb").write(wawawa.content)
            print(f"Saved: {author} {taitoru} {i}.mp3\n")

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

        with open(f"{author}.csv", "a+", encoding="utf16", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                [i, nameNshit, taitoru, lenghtAndDate, dateToday, paragraphDescr]
            )

print("\ndone")
