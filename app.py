import streamlit as st
import pandas as pd

# Sayfa tasarımı
st.set_page_config(page_title="Servis Takip", layout="wide", initial_sidebar_state="collapsed")

# Google Sheets Linkleri (Kendi ID'lerinle değiştirmen gerekecek)
SHEET_ID = "BURAYA_SHEET_ID_GELECEK" # Linkteki /d/ ile /edit arasındaki uzun kod
LISTE_GID = "0" # Servisliste sayfasının ID'si
PERSONEL_GID = "SAYFA_IDSI" # Servispersonel sayfasının ID'si (linkin sonunda yazar)

url_liste = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={LISTE_GID}"
url_personel = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={PERSONEL_GID}"

@st.cache_data(ttl=60) # Veriyi her dakika yeniler
def get_data(url):
    return pd.read_csv(url)

# Arayüz
st.title("🚐 Servis Güzergah ve Şoför Takip Sistemi")

# Sayfalar arası geçiş için sekmeler
tab1, tab2 = st.tabs(["📋 Tüm Liste", "📞 Şoför İletişim"])

with tab1:
    df_liste = get_data(url_liste)
    
    # Filtreleme (Servis Hattına Göre)
    secilen_hat = st.multiselect("Servis Hattı Seçin:", options=df_liste['Servis Hat Seçiniz'].unique())
    
    if secilen_hat:
        filtered_df = df_liste[df_liste['Servis Hat Seçiniz'].isin(secilen_hat)]
    else:
        filtered_df = df_liste

    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

with tab2:
    df_personel = get_data(url_personel)
    st.subheader("Aktif Şoför ve Araç Bilgileri")
    
    # Kartlar şeklinde gösterim
    cols = st.columns(3)
    for index, row in df_personel.iterrows():
        with cols[index % 3]:
            st.info(f"**{row['Şoför']}**\n\n**Plaka:** {row['Plaka']}\n\n**Tel:** {row['Telefon']}")
