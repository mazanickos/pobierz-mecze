import streamlit as st
from supabase import create_client, Client

# Konfiguracja strony
st.set_page_config(page_title="Moja Aplikacja Piłkarska", page_icon="⚽", layout="wide")

st.title("⚽ Dzisiejsze Mecze Piłkarskie")
st.write("Aplikacja pobiera dane bezpośrednio z bazy danych Supabase.")

# Pobieranie danych z Supabase za pomocą sekretów
# (Streamlit Cloud pozwala bezpiecznie trzymać klucze)
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)

    # Pobieranie danych z tabeli 'mecze'
    response = supabase.table("mecze").select("*").execute()
    dane = response.data

    if dane:
        st.success(f"Znaleziono {len(dane)} meczów w bazie!")
        # Wyświetlenie danych jako ładna tabela w Streamlit
        st.dataframe(dane, use_container_width=True)
    else:
        st.info("Brak meczów w tabeli 'mecze'. Uruchom najpierw skrypt pobierający!")

except Exception as e:
    st.error(f"Wystąpił błąd podczas łączenia z bazą: {e}")
