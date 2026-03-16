import streamlit as st
import pandas as pd

# Sayfa Genişliği ve Başlık Ayarı
st.set_page_config(page_title="Servis Takip Sistemi", layout="wide", initial_sidebar_state="collapsed")

# 1. Google Sheets Bilgileri (Senin linkinden aldım)
SHEET_ID = "1kWV5OgXsHprJro7O3zgb-wc8bzAnzUhdVReo2sheADI"
LISTE_GID = "0"             # Servisliste sekmesi
PERSONEL_GID = "1564855422"  # Servispersonel sekmesi

# 2. CSV formatında veri çekme linkleri
url_liste = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={LISTE_GID}"
url_personel = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={PERSONEL_GID}"

# Veri çekme fonksiyonu
@st.cache_data(ttl=60) # Veriyi her dakika tazeler
def get_data(url):
    return pd.read_csv(url)

# Arayüz Başlığı
st.title("🚐 Servis Güzergah ve Şoför Takip Sistemi")
st.markdown("---")

# Sayfalar (Sekmeler)
tab1, tab2 = st.tabs(["📋 Tüm Personel Listesi", "📞 Şoför & Araç Bilgileri"])

with tab1:
    try:
        df_liste = get_data(url_liste)
        
        # Filtreleme Seçenekleri
        search = st.text_input("Personel, Güzergah veya Durak Ara:", placeholder="Örn: Akpınar veya Canan Altın...")
        
        if search:
            # Tüm sütunlarda arama yapar
            filtered_df = df_liste[df_liste.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        else:
            filtered_df = df_liste

        # Tabloyu Göster
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error("Liste yüklenirken bir hata oluştu. Lütfen Google Sheets paylaşım ayarlarını kontrol et.")

with tab2:
    try:
        df_personel = get_data(url_personel)
        st.subheader("Aktif Servis Şoförleri")
        
        # Şoförleri kartlar halinde yan yana göster
        cols = st.columns(3)
        for index, row in df_personel.iterrows():
            with cols[index % 3]:
                with st.container(border=True):
                    st.write(f"### 👤 {row['Şoför']}")
                    st.write(f"**📍 Hat:** {row['Servis Hattı']}")
                    st.write(f"**🚗 Plaka:** {row['Plaka']}")
                    st.write(f"**📞 Tel:** {row['Telefon']}")
    except Exception as e:
        st.error
