from datetime import datetime
import os
import requests
from supabase import create_client, Client

# Konfiguracja API i Supabase
API_KEY = "TWOJ_KLUCZ_API"  # Zostaw swój klucz do API-Football
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def pobierz_i_zapisz_mecze():
    # Pobieramy dzisiejszą datę
    dzisiaj = "2024-05-15"
    # Jeśli chcesz przetestować konkretny dzień, w którym na pewno były mecze, 
    # możesz odkomentować poniższą linijkę i wpisać datę:
    # dzisiaj = "2026-05-15"

    url = f"https://v3.football.api-sports.io/fixtures?date={dzisiaj}"
    headers = {
        'x-apisports-key': API_KEY
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    mecze = data.get('response', [])
    print(f"Pobrano {len(mecze)} meczów z API.")

    if not mecze:
        print("Brak meczów do zapisania na dzisiaj.")
        return

    for mecz in mecze:
        kraj = mecz['league']['country']
        liga = mecz['league']['name']
        gospodarz = mecz['teams']['home']['name']
        gosc = mecz['teams']['away']['name']
        data_meczu = mecz['fixture']['date']

        dane_rekordu = {
            "kraj": kraj,
            "liga": liga,
            "gospodarz": gospodarz,
            "gosc": gosc,
            "data_meczu": data_meczu
        }

        # Zapis do tabeli z wielką literą "Mecze"
        supabase.table("Mecze").insert(dane_rekordu).execute()

    print("Zapisano mecze do bazy pomyślnie!")

if __name__ == "__main__":
    pobierz_i_zapisz_mecze()
