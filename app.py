import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="Lyreco AI SEO Agent", page_icon="🟢", layout="wide")

# --- 2. FUNKCJA SCRAPERA ---
def scrape_lyreco(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None, "Blad polaczenia"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tytul
        h1 = soup.find('h1')
        title = h1.text.strip() if h1 else "Produkt Lyreco"
        
        # Opis
        desc_div = soup.find('div', {'class': 'product-details-description'})
        raw_desc = desc_div.text.strip() if desc_div else "Brak opisu"
        
        # Specyfikacja (prosta wersja tekstowa)
        specs = "Specyfikacja pobrana."
        
        return f"PRODUKT: {title}\nOPIS: {raw_desc}", None

    except Exception as e:
        return None, str(e)

# --- 3. MOCKUP AI (Tekst na sztywno, zeby nie psulo kodu) ---
def get_mock_ai_response():
    # Uzywam prostych cudzyslowow i dodawania, zeby Python nie glupial przy kopiowaniu
    part1 = "### 🟢 SEKCJA 1: AI SNAPSHOT\nBostik Blu Tack to masa klejaca do biura.\n\n"
    part2 = "### 👥 SEKCJA 2: HUMAN DEEP DIVE\n- Bezpieczny montaz plakatow\n- Organizacja kabli\n- Czyszczenie klawiatur\n\n"
    part3 = "### 🤖 SEKCJA 3: AGENTIC DATA\nCode: 719.594\nWeight: 120g"
    return part1 + part2 + part3

# --- 4. INTERFEJS ---
st.title("Lyreco GEO Optimizer")
st.info("Demo wersji 1.0")

col1, col2 = st.columns([3, 1])

with col1:
    default_url = "https://shop.lyreco.co.uk/en/product/719.594/bostik-blu-tack-economy-120g-pack"
    url_input = st.text_input("URL Produktu:", value=default_url)

with col2:
    st.write("")
    st.write("")
    # To musi byc w nowej linii!
    generate_btn = st.button("Uruchom Agenta")

if generate_btn:
    with st.spinner('Analiza...'):
        # A. Pobieranie
        data, error = scrape_lyreco(url_input)
        
        if error:
            st.error(f"Blad: {error}")
        else:
            # B. Symulacja
            time.sleep(1)
            ai_output = get_mock_ai_response()
            
            # C. Wyniki
            st.success("Gotowe!")
            
            t1, t2 = st.tabs(["WYNIK AI", "DANE SUROWE"])
            
            with t1:
                st.markdown(ai_output)
            
            with t2:
                st.text(data)
