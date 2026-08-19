import requests
from datetime import datetime

API_KEY = "5faa4ab67a7bd457fb07838838bf1d3d"
dzisiaj = datetime.now().strftime("%Y-%m-%d")
url = f"https://v3.football.api-sports.io/fixtures?date={dzisiaj}"

headers = {'x-apisports-key': API_KEY}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    liczba_meczow = data.get('results', 0)
    
    # Otwieramy plik do zapisu ('w' oznacza write - nadpisywanie)
    with open("mecze_dzis.txt", "w", encoding="utf-8") as plik:
        plik.write(f"Mecze na dzień {dzisiaj}\n")
        plik.write(f"Liczba meczów: {liczba_meczow}\n\n")
        
        for match in data.get('response', []):
            liga = match['league']['name']
            kraj = match['league']['country']
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            linia = f"[{kraj}] {liga}: {home} vs {away}\n"
            plik.write(linia)
            
    print(f"Sukces! Pobrano i zapisano {liczba_meczow} meczów do pliku mecze_dzis.txt")
else:
    print(f"Błąd: {response.status_code}")