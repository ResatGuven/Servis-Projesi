import streamlit as st
import pandas as pd

# Sayfa Genişliği ve Başlık Ayarı
st.set_page_config(page_title="Servis Takip Sistemi", layout="wide", initial_sidebar_state="collapsed")

# 1. Google Sheets Bilgileri (Son paylaştığın güncel linklerden aldım)
SHEET_ID = "1kWV5OgXsHprJro7O3zgb-wc8bzAnzUhdVReo2sheADI"
LISTE_GID = "1161773988"     # Servisliste sekmesinin güncel ID'si
PERSONEL_GID = "1207904188"  # Servispersonel sekmesinin güncel ID'si

# 2. En güvenli veri çekme link formatı (gviz)
url_liste = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={LISTE_GID}"
url_personel = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={PERSONEL_GID}"

# Veri çekme fonksiyonu
@st.cache_data(ttl=60) # Veriyi dakikada bir günceller
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
        
        # Sütun isimlerini temizle (Google bazen boş sütunlar ekleyebilir)
        df_liste = df_liste.dropna(how='all', axis=1)
        
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
        st.error(f"Liste yüklenirken bir hata oluştu. Hata: {e}")
        st.info("Lütfen Google Sheets 'Paylaş' ayarının 'Bağlantıya sahip olan herkes' olarak seçili olduğundan emin ol.")

with tab2:
    try:
        df_personel = get_data(url_personel)
        df_personel = df_personel.dropna(how='all', axis=1)
        
        st.subheader("Aktif Servis Şoförleri")
        
        # Şoförleri kartlar halinde göster
        cols = st.columns(3)
        for index, row in df_personel.iterrows():
            with cols[index % 3]:
                with st.container(border=True):
                    # Görsellerdeki sütun başlıklarına göre ayarlandı
                    st.write(f"### 👤 {row['Şoför']}")
                    st.write(f"**📍 Hat:** {row['Servis Hattı']}")
                    st.write(f"**🚗 Plaka:** {row['Plaka']}")
                    st.write(f"**📞 Tel:** {row['Telefon']}")
    except Exception as e:
        st.error(f"Şoför bilgileri yüklenemedi. Hata: {e}")

# Alt Bilgi
st.markdown("---")
st.caption("Veriler Google Sheets üzerinden anlık olarak çekilmektedir.")
