import streamlit as st
from supabase import create_client, Client

# Konfiguracja strony
st.set_page_config(page_title="Moja Aplikacja Piłkarska", page_icon="⚽", layout="wide")

st.title("⚽ Dzisiejsze Mecze Piłkarskie")
st.write("Aplikacja pobiera dane bezpośrednio z bazy danych Supabase.")

try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    # Pobieranie danych z tabeli 'Mecze'
    response = supabase.table("Mecze").select("*").execute()
    dane = response.data

    if dane:
        st.success(f"Znaleziono {len(dane)} meczów w bazie!")
        st.dataframe(dane, use_container_width=True)
    else:
        st.info("Brak meczów w tabeli 'Mecze'. Uruchom najpierw skrypt pobierający!")

except Exception as e:
    st.error(f"Wystąpił błąd podczas łączenia z bazą: {e}")
