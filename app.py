import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="Lyreco AI SEO Agent", page_icon="🟢", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    .stButton>button {background-color: #2b5c96; color: white; border-radius: 5px; width: 100%;}
    h1 {color: #2b5c96;}
    </style>
""", unsafe_allow_html=True)

# --- 2. FUNKCJA SCRAPERA ---
def scrape_lyreco(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None, f"Błąd połączenia: {response.status_code}"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tytuł
        title_tag = soup.find('h1')
        title = title_tag.text.strip() if title_tag else "Produkt Lyreco"
        
        # Opis
        raw_desc = "Brak opisu."
        desc_div = soup.find('div', {'class': 'product-details-description'})
        if desc_div:
            raw_desc = desc_div.text.strip()
        
        # Specyfikacja
        specs = {}
        table = soup.find('table', {'class': 'table-data-sheet'})
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['th', 'td'])
                if len(cols) == 2:
                    specs[cols[0].text.strip()] = cols[1].text.strip()
        
        full_context = f"PRODUKT: {title}\nOPIS: {raw_desc}\nSPECYFIKACJA: {str(specs)}"
        return full_context, None

    except Exception as e:
        return None, str(e)

# --- 3. MOCKUP AI (Demo Response) ---
def get_mock_ai_response():
    # Tutaj jest ten tekst, który sprawiał problemy. Teraz jest bezpieczny.
    response = """
### 🟢 SEKCJA 1: AI SNAPSHOT (Google SGE)
**Bostik Blu Tack (Economy Pack)** to wielorazowa masa mocująca, stanowiąca bezpieczną alternatywę dla taśm i pinezek. Idealna do biur (montaż ogłoszeń bez niszczenia ścian) i zabezpieczania sprzętu przed przesuwaniem.

### 👥 SEKCJA 2: HUMAN DEEP DIVE (Use Cases)
* **Bezpieczny montaż:** Mocowanie harmonogramów BHP na drzwiach bez wiercenia.
* **Organizacja biurka:** Stabilizacja lekkich przedmiotów (korytka kablowe, podkładki).
* **Czyszczenie:** Usuwa kurz i okruchy z klawiatur i szczelin drukarek.
* **Ekonomia:** Jedno opakowanie 120g wystarcza na 500+ punktów mocowania.

### 🤖 SEKCJA 3: AGENTIC DATA (JSON)
```json
{
  "product_name": "Bostik Blu Tack",
  "weight": "120g",
  "reusability": "high",
  "surface_safety": "non-damaging",
  "application": ["mounting", "cleaning", "stabilizing"]
}
"" return response

--- 4. INTERFEJS ---
st.title("🚀 Lyreco GEO & Agentic Optimizer") st.info("Narzędzie do transformacji opisów produktów pod Generative Engine Optimization.")

col1, col2 = st.columns([3, 1])

with col1: url_input = st.text_input("Wklej URL produktu (Lyreco UK):", value="https://shop.lyreco.co.uk/en/product/719.594/bostik-blu-tack-economy-120g-pack")

with col2: st.write("") st.write("") generate_btn = st.button("Uruchom Agenta")

if generate_btn: with st.spinner('Analizuję strukturę strony Lyreco...'): # A. Pobieranie data, error = scrape_lyreco(url_input)

    if error:
        st.error(f"Błąd: {error}")
    else:
        # B. Symulacja AI
        time.sleep(1.5)
        ai_output = get_mock_ai_response()
        
        # C. Wyniki
        st.success("Analiza zakończona pomyślnie!")
        
        tab1, tab2 = st.tabs(["🟢 WYNIK AI (GEO Optimized)", "🔴 DANE SUROWE (Robot View)"])
        
        with tab1:
            st.markdown(ai_output)
        
        with tab2:
            st.text_area("Co pobrał scraper:", value=data, height=300)
