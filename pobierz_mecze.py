import os
import requests
from datetime import datetime
from supabase import create_client, Client

# Pobieranie kluczy z bezpiecznych zmiennych środowiskowych GitHub Actions
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Połączenie z bazą danych Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

API_KEY = "5faa4ab67a7bd457fb0783838bf1d3d"
dzisiaj = datetime.now().strftime('%Y-%m-%d')
url = f"https://v3.football.api-sports.io/fixtures?date={dzisiaj}"

headers = {
    'x-apisports-key': API_KEY
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    liczba_meczow = data.get('results', 0)
    print(f"Pobrano {liczba_meczow} meczů z API.")
    
    mecze_do_zapisu = []
    
    for match in data.get('response', []):
        liga = match['league']['name']
        kraj = match['league']['country']
        home = match['teams']['home']['name']
        away = match['teams']['away']['name']
        
        # Przygotowujemy słownik pasujący do kolumn w Twojej tabeli 'mecze'
        rekord = {
            "kraj": kraj,
            "liga": liga,
            "gospodarz": home,
            "gosc": away,
            "data_meczu": dzisiaj
        }
        mecze_do_zapisu.append(rekord)
    
    # Jeśli są jakieś mecze, wysyłamy je paczką do Supabase
    if mecze_do_zapisu:
        res = supabase.table("mecze").insert(mecze_do_zapisu).execute()
        print(f"Sukces! Zapisano mecze w bazie Supabase.")
    else:
        print("Brak meczów do zapisania na dzisiaj.")
else:
    print(f"Błąd API: {response.status_code}")
