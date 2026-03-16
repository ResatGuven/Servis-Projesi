import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları ve Görsel Tema (Kurumsal Renk Tonları)
st.set_page_config(
    page_title="Warmhaus Servis Portalı",
    page_icon="🚐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Özel CSS ile Stil Verme (Sadeliği ve Şıklığı Artıran Kısım)
st.markdown("""
<style>
    /* Genel Arka Plan ve Yazı Tipi */
    .stApp {
        background-color: #f4f7f6; /* Çok hafif gri arka plan */
        font-family: 'Roboto', sans-serif;
    }
    
    /* Ana Başlık Stili */
    .main-title {
        color: #1e3a8a; /* Koyu Lacivert */
        text-align: center;
        font-weight: 700;
        font-size: 36px;
        margin-bottom: 20px;
    }
    
    /* Alt Başlık Stili */
    .section-subtitle {
        color: #0d9488; /* Turkuaz Vurgu */
        font-weight: 600;
        font-size: 20px;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    /* Güzergah Seçim Kutusu Stili */
    .stSelectbox label {
        color: #4b5563; /* Orta Gri */
        font-weight: 500;
    }
    
    /* Bilgi Kartı Stili (Şoför ve Liste İçin) */
    .info-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); /* Hafif gölge */
        margin-bottom: 20px;
        border-left: 5px solid #0d9488; /* Turkuaz sol şerit */
    }

    /* Şoför İsim Başlığı */
    .driver-name {
        color: #111827; /* Çok Koyu Gri */
        font-size: 24px;
        font-weight: 700;
    }

    /* Veri DataFrame Tablosu Özelleştirme */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# 2. Google Sheets Bilgileri (Aynı Kalıyor)
SHEET_ID = "1kWV5OgXsHprJro7O3zgb-wc8bzAnzUhdVReo2sheADI"
LISTE_GID = "1161773988"
PERSONEL_GID = "1207904188"

url_liste = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={LISTE_GID}"
url_personel = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={PERSONEL_GID}"

@st.cache_data(ttl=60)
def get_data(url):
    df = pd.read_csv(url)
    return df.dropna(how='all', axis=1)

# 3. Arayüz Başlığı (Özel Klasman)
st.markdown('<div class="main-title">🚐 Warmhaus Servis Portalı</div>', unsafe_allow_html=True)

try:
    df_liste = get_data(url_liste)
    df_personel = get_data(url_personel)

    # 4. Sadeleştirilmiş Güzergah Seçimi (İlk Bakış)
    hatlar = sorted(df_liste['Servis Hat Seçiniz'].unique())
    
    # Başlangıç talimatı
    st.markdown('<div class="section-subtitle">🚩 Lütfen Servis Hattınızı Seçin:</div>', unsafe_allow_html=True)
    secilen_hat = st.selectbox("", ["Güzergah Seçiniz..."] + list(hatlar), label_visibility="collapsed")

    st.markdown("---")

    # 5. Seçilen Hata Göre İçerik (Şık Kartlarla)
    if secilen_hat != "Güzergah Seçiniz...":
        filtreli_liste = df_liste[df_liste['Servis Hat Seçiniz'] == secilen_hat]
        filtreli_sofor = df_personel[df_personel['Servis Hattı'] == secilen_hat]
        
        # A. Şoför Bilgi Kartı (Estetik Tasarım)
        if not filtreli_sofor.empty:
            sofor_bilgi = filtreli_sofor.iloc[0]
            st.markdown(f"""
                <div class="info-card">
                    <div class="driver-name">👤 {sofor_bilgi['Şoför']}</div>
                    <p style="margin-top: 10px; color: #4b5563;">
                        <strong>📍 Hat:</strong> {secilen_hat} Hattı<br>
                        <strong>🚗 Plaka:</strong> {sofor_bilgi['Plaka']}<br>
                        <strong>📞 Telefon:</strong> <a href="tel:{sofor_bilgi['Telefon']}" style="color: #0d9488; text-decoration: none;">{sofor_bilgi['Telefon']}</a>
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        # B. Personel Liste Kartı (Hafif Gölgeden)
        st.markdown('<div class="section-subtitle">👥 Servis Yolcu Listesi</div>', unsafe_allow_html=True)
        
        # Sadece gerekli sütunları şık bir tabloyla göster
        st.dataframe(
            filtreli_liste[['AD-SOYAD', 'SERVİS DURAĞI']], 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "AD-SOYAD": st.column_config.TextColumn("👤 Personel Adı"),
                "SERVİS DURAĞI": st.column_config.TextColumn("📍 Biniş Durağı")
            }
        )
        
    else:
        # Başlangıç Durumu: Sade Bir Yönlendirme
        st.info("Yukarıdaki menüden gitmek istediğiniz servis hattını seçerek şoför bilgilerini ve yolcu listesini görebilirsiniz.")

except Exception as e:
    st.error(f"Veri yüklenirken bir sorun oluştu. Lütfen bağlantınızı ve Google Sheets ayarlarınızı kontrol edin. (Hata: {e})")

# Alt Bilgi (Sade)
st.markdown("---")
st.caption("Veriler Google Sheets üzerinden otomatik olarak güncellenmektedir. Warmhaus Dijital Çözümler.")
