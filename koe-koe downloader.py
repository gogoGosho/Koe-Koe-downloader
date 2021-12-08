from bs4 import BeautifulSoup
import requests, re


# r = requests.get("<enter the autoplay link↙↙↙↙↙↙>").text
r = requests.get(
    "https://koe-koe.com/auto_play.php?word=%E3%81%8A%E3%81%AA%E3%81%AA&g=1"
).text
soup = BeautifulSoup(r, "lxml")
empy = []
for a in soup.find_all("a", href=True):
    empy.append(a["href"])
empy = empy[6:-16]
rdyforregex = list(dict.fromkeys(empy))


def listToString(s):
    str1 = " "
    return str1.join(s)


convertedString = listToString(rdyforregex)
ids = re.findall(r"[0-9]+", convertedString)
for i in ids:
    linkka = f"https://file.koe-koe.com/sound/upload/{i}.mp3"
    print(f"Saving: {linkka}")
    wawawa = requests.get(linkka)
    open(f"{i}.mp3", "wb").write(wawawa.content)
    print(f"Saved: {linkka}")
    # for some reason theyre not in order.. unlucky
