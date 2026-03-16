import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder # Personel ekleme/çıkarma için gerekebilir (opsiyonel)

# 1. Sayfa Ayarları (Tam Mobil Odaklı)
st.set_page_config(page_title="Warmhaus Portal", page_icon="🚐", layout="centered")

# 2. Üst Düzey Mobil App Tasarımı (CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    /* Mobil Header */
    .app-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 40px 20px;
        border-radius: 0 0 32px 32px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 20px rgba(30, 58, 138, 0.2);
        margin-bottom: 25px;
    }
    
    .app-title { font-size: 28px; font-weight: 800; letter-spacing: -1px; margin: 0; }
    .app-subtitle { font-size: 14px; opacity: 0.8; font-weight: 400; }

    /* Modern Kart Yapısı */
    .mobile-card {
        background: white;
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid #f1f5f9;
    }
    
    .driver-name { font-size: 22px; font-weight: 700; color: #0f172a; margin-bottom: 4px; }
    .driver-tag { font-size: 12px; font-weight: 600; color: #3b82f6; text-transform: uppercase; }

    /* Arama ve Seçim Kutusu */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 16px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 5px !important;
    }

    /* Şık Buton */
    .call-btn {
        background: #22c55e;
        color: white !important;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 14px;
        border-radius: 16px;
        text-decoration: none;
        font-weight: 700;
        margin-top: 15px;
        gap: 10px;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

# 3. Veri Yönetimi Fonksiyonları
SHEET_ID = "1kWV5OgXsHprJro7O3zgb-wc8bzAnzUhdVReo2sheADI"
LISTE_GID = "1161773988"
PERSONEL_GID = "1207904188"

# Not: Veri yazma işlemi için Google Sheets API (Service Account) gerekir. 
# Şimdilik mevcut yapı üzerinden "Görünüm" ve "Yönetim Arayüzü" kuruyoruz.

@st.cache_data(ttl=10)
def get_data(url):
    return pd.read_csv(url).dropna(how='all', axis=1)

# Header Alanı
st.markdown("""
    <div class="app-header">
        <div class="app-title">WARMHAUS</div>
        <div class="app-subtitle">Akıllı Servis Takip Sistemi</div>
    </div>
""", unsafe_allow_html=True)

# 4. Yan Menü: Admin Girişi
with st.sidebar:
    st.title("🔐 Yönetici Paneli")
    admin_sifre = st.text_input("Yönetici Şifresi", type="password")
    is_admin = admin_sifre == "Admin123" # Şifreni buradan değiştir

    if is_admin:
        st.success("Yönetici girişi yapıldı!")
        islem = st.radio("Yapılacak İşlem", ["Listeyi Görüntüle", "Personel Ekle/Çıkar", "Şoför Güncelle"])
    else:
        st.info("Yönetici işlemleri için şifre giriniz.")

# 5. Ana Uygulama Mantığı
try:
    url_liste = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={LISTE_GID}"
    url_personel = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={PERSONEL_GID}"
    
    df_liste = get_data(url_liste)
    df_personel = get_data(url_personel)

    if is_admin and islem == "Personel Ekle/Çıkar":
        st.subheader("🛠 Personel Yönetimi")
        # Buraya Personel Ekleme Formu Gelecek
        with st.form("personel_ekle"):
            yeni_ad = st.text_input("Ad Soyad")
            yeni_hat = st.selectbox("Hat", df_liste['Servis Hat Seçiniz'].unique())
            yeni_durak = st.text_input("Biniş Durağı")
            ekle_btn = st.form_submit_button("Personeli Kaydet")
            if ekle_btn:
                st.warning("Google Sheets API entegrasyonu tamamlanmalıdır.")

    elif is_admin and islem == "Şoför Güncelle":
        st.subheader("🚛 Şoför Yönetimi")
        st.dataframe(df_personel)

    else:
        # NORMAL KULLANICI EKRANI (MOBİL APP TASARIMI)
        hatlar = sorted(df_liste['Servis Hat Seçiniz'].unique())
        secilen_hat = st.selectbox("📍 Gideceğiniz Hattı Seçin", ["Hattınızı seçin..."] + list(hatlar))

        if secilen_hat != "Hattınızı seçin...":
            sofor_verisi = df_personel[df_personel['Servis Hattı'] == secilen_hat]
            yolcu_listesi = df_liste[df_liste['Servis Hat Seçiniz'] == secilen_hat]

            if not sofor_verisi.empty:
                s = sofor_verisi.iloc[0]
                st.markdown(f"""
                    <div class="mobile-card">
                        <div class="driver-tag">Servis Şoförü</div>
                        <div class="driver-name">{s['Şoför']}</div>
                        <div style="color: #64748b; font-size: 14px;">
                            <i class="fas fa-shuttle-van"></i> Plaka: <b>{s['Plaka']}</b>
                        </div>
                        <a href="tel:{s['Telefon']}" class="call-btn">
                            <i class="fas fa-phone-alt"></i> Şoförü Ara
                        </a>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown(f"### 👥 {secilen_hat} Listesi")
            st.dataframe(yolcu_listesi[['AD-SOYAD', 'SERVİS DURAĞI']], use_container_width=True, hide_index=True)

except Exception as e:
    st.error("Veri bağlantısı hatası.")

st.markdown("<br><center style='color:#cbd5e1; font-size:12px;'>Warmhaus IT - 2026</center>", unsafe_allow_html=True)
