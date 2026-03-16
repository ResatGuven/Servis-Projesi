import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları (Mobil Odaklı ve Başlıklı)
st.set_page_config(
    page_title="Warmhaus Personel Portalı",
    page_icon="🚐",
    layout="wide", # Geniş ekran
    initial_sidebar_state="collapsed" # Yan menü kapalı
)

# 2. Özel CSS ile Stil Verme (Canlılık ve Şıklık Katan Kısım)
st.markdown("""
<style>
    /* Genel Arka Plan ve Yazı Tipi */
    .stApp {
        background-color: #ffffff; /* Bembeyaz arka plan */
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Ana Başlık Stili */
    .main-title {
        color: #1e3a8a; /* Koyu Lacivert */
        text-align: center;
        font-weight: 800;
        font-size: 36px;
        padding: 20px 0;
        margin-bottom: 10px;
        border-bottom: 2px solid #e2e8f0; /* Hafif alt çizgi */
    }
    
    /* Alt Başlık Stili */
    .section-subtitle {
        color: #0284c7; /* Canlı Mavi/Turkuaz */
        font-weight: 700;
        font-size: 22px;
        margin-top: 20px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
    }
    
    .section-subtitle i { margin-right: 10px; } /* İkon boşluğu */

    /* Bilgi Kartı Stili (Şoför ve Liste İçin) */
    .info-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 16px; /* Yuvarlak köşeler */
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); /* Şık gölge */
        margin-bottom: 25px;
        border: 1px solid #e2e8f0; /* Hafif kenarlık */
    }

    /* Şoför İsim Başlığı */
    .driver-name {
        color: #111827; /* Çok Koyu Gri */
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 10px;
    }
    
    /* Şoför Detay Yazıları */
    .driver-detail {
        color: #4b5563; /* Orta Gri */
        font-size: 16px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
    }
    .driver-detail i { margin-right: 8px; color: #0284c7; } /* İkon rengi */

    /* Veri DataFrame Tablosu Özelleştirme */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* DataFrame Başlık Rengi */
    .stDataFrame thead tr th {
        background-color: #f1f5f9 !important;
        color: #1e3a8a !important;
        font-weight: 700 !important;
    }

    /* Mobil Uyum İçin Ekstra Düzenlemeler */
    @media (max-width: 768px) {
        .main-title { font-size: 28px; }
        .info-card { padding: 15px; }
        .driver-name { font-size: 22px; }
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

# 3. Google Sheets Verileri (Aynı Kalıyor)
SHEET_ID = "1kWV5OgXsHprJro7O3zgb-wc8bzAnzUhdVReo2sheADI"
LISTE_GID = "1161773988"
PERSONEL_GID = "1207904188"

url_liste = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={LISTE_GID}"
url_personel = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={PERSONEL_GID}"

@st.cache_data(ttl=60) # Veriyi 60 saniyede bir tazele
def get_data(url):
    df = pd.read_csv(url)
    return df.dropna(how='all', axis=1) # Boş sütunları temizle

# 4. Arayüz Başlığı (Özel Klasman)
st.markdown('<div class="main-title">🚐 Warmhaus Personel Servis Portalı</div>', unsafe_allow_html=True)

try:
    df_liste = get_data(url_liste)
    df_personel = get_data(url_personel)

    # 5. Sadeleştirilmiş Güzergah Seçimi (İlk Bakış)
    hatlar = sorted(df_liste['Servis Hat Seçiniz'].unique())
    
    # Başlangıç talimatı (İkonlu)
    st.markdown('<div class="section-subtitle"><i class="fas fa-map-marker-alt"></i> Lütfen Servis Hattınızı Seçin:</div>', unsafe_allow_html=True)
    secilen_hat = st.selectbox("", ["Güzergah Seçiniz..."] + list(hatlar), label_visibility="collapsed")

    st.markdown("---")

    # 6. Seçilen Hata Göre İçerik (Şık Kartlarla)
    if secilen_hat != "Güzergah Seçiniz...":
        filtreli_liste = df_liste[df_liste['Servis Hat Seçiniz'] == secilen_hat]
        filtreli_sofor = df_personel[df_personel['Servis Hattı'] == secilen_hat]
        
        # A. Şoför Bilgi Kartı (Estetik Tasarım)
        if not filtreli_sofor.empty:
            sofor_bilgi = filtreli_sofor.iloc[0]
            st.markdown(f"""
                <div class="info-card">
                    <div class="driver-name">👤 {sofor_bilgi['Şoför']}</div>
                    <div class="driver-detail"><i class="fas fa-bus"></i> <b>Hat:</b> {secilen_hat} Hattı</div>
                    <div class="driver-detail"><i class="fas fa-id-card"></i> <b>Plaka:</b> {sofor_bilgi['Plaka']}</div>
                    <div class="driver-detail"><i class="fas fa-phone-alt"></i> <b>Telefon:</b> <a href="tel:{sofor_bilgi['Telefon']}" style="color: #0284c7; text-decoration: none; font-weight:600;">{sofor_bilgi['Telefon']}</a></div>
                </div>
            """, unsafe_allow_html=True)
        
        # B. Personel Liste Kartı (Canlı Başlık)
        st.markdown(f'<div class="section-subtitle"><i class="fas fa-users"></i> {secilen_hat} Hattı Yolcu Listesi</div>', unsafe_allow_html=True)
        
        # Sadece gerekli sütunları şık bir tabloyla göster
        st.dataframe(
            filtreli_liste[['AD-SOYAD', 'SERVİS DURAĞI']], 
            use_container_width=True, # Genişliği kapla
            hide_index=True, # İndeks numarasını gizle
            column_config={
                "AD-SOYAD": st.column_config.TextColumn("👤 Personel Adı"),
                "SERVİS DURAĞI": st.column_config.TextColumn("📍 Biniş Durağı")
            }
        )
        
    else:
        # Başlangıç Durumu: Sade Bir Yönlendirme (İkonlu)
        st.info("👋 Merhaba! Yukarıdaki menüden gitmek istediğiniz servis hattını seçerek şoför bilgilerini ve yolcu listesini anında görebilirsiniz.")

except Exception as e:
    st.error(f"Veriler yüklenirken bir sorun oluştu. Lütfen bağlantınızı ve Google Sheets ayarlarınızı kontrol edin. (Hata: {e})")

# Alt Bilgi (Sade ve Kurumsal)
st.markdown("---")
st.caption("Veriler Google Sheets üzerinden otomatik olarak güncellenmektedir. Warmhaus Dijital Çözümler © 2026")
