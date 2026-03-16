import streamlit as st
import pandas as pd

# Mobil uyumlu genişlik ve sayfa ayarı
st.set_page_config(page_title="Servis Takip", layout="wide", initial_sidebar_state="collapsed")

# Google Sheets Bilgileri
SHEET_ID = "1kWV5OgXsHprJro7O3zgb-wc8bzAnzUhdVReo2sheADI"
LISTE_GID = "1161773988"
PERSONEL_GID = "1207904188"

url_liste = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={LISTE_GID}"
url_personel = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={PERSONEL_GID}"

@st.cache_data(ttl=60)
def get_data(url):
    df = pd.read_csv(url)
    return df.dropna(how='all', axis=1)

# Başlık
st.title("🚐 Servis Güzergah Portalı")
st.markdown("Lütfen listesini görmek istediğiniz **Servis Hattını** seçin:")

try:
    df_liste = get_data(url_liste)
    df_personel = get_data(url_personel)

    # 1. Güzergah Seçim Kutucukları (Filtreleme)
    hatlar = sorted(df_liste['Servis Hat Seçiniz'].unique())
    
    # Seçim menüsünü buton gibi kullanmak için (Mobil dostu)
    secilen_hat = st.selectbox("🚩 Güzergah Seçin:", ["Hepsini Göster"] + list(hatlar))

    st.markdown("---")

    # 2. Seçilen Hata Göre Veriyi Filtrele
    if secilen_hat != "Hepsini Göster":
        filtreli_liste = df_liste[df_liste['Servis Hat Seçiniz'] == secilen_hat]
        filtreli_sofor = df_personel[df_personel['Servis Hattı'] == secilen_hat]
        
        # Şoför Bilgisi (Öne Çıkarılmış)
        if not filtreli_sofor.empty:
            sofor_bilgi = filtreli_sofor.iloc[0]
            with st.expander(f"📞 {secilen_hat} Hattı Şoför Bilgileri (Tıkla)", expanded=True):
                c1, c2, c3 = st.columns(3)
                c1.metric("Şoför", sofor_bilgi['Şoför'])
                c2.metric("Plaka", sofor_bilgi['Plaka'])
                c3.write(f"**Telefon:** \n\n {sofor_bilgi['Telefon']}")
        
        st.subheader(f"👥 {secilen_hat} Hattı Yolcu Listesi")
        st.dataframe(filtreli_liste[['AD-SOYAD', 'SERVİS DURAĞI']], use_container_width=True, hide_index=True)
        
    else:
        st.info("Yukarıdaki menüden bir güzergah seçerek o servisteki kişileri görebilirsiniz.")
        st.dataframe(df_liste[['AD-SOYAD', 'Servis Hat Seçiniz', 'SERVİS DURAĞI']], use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Veri yükleme hatası: {e}")

st.caption("Veriler Google Sheets üzerinden otomatik güncellenir.")
