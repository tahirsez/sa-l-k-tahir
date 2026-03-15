import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="MHRS Destekli Sağlık Asistanı", page_icon="🏥", layout="wide")

# MHRS Kurumsal Renkleri ve CSS Teması
st.markdown("""
    <style>
    /* MHRS Kırmızısı ve Genel Tema */
    :root {
        --mhrs-red: #e30613;
        --mhrs-dark: #2d2d2d;
    }
    .main { background-color: #fcfcfc; }
    
    /* Buton Tasarımı */
    .stButton>button { 
        width: 100%; 
        border-radius: 5px; 
        background-color: #e30613; 
        color: white; 
        height: 3.5em; 
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #b3050f;
        border: none;
    }
    
    /* Yan Panel (Sidebar) MHRS Teması */
    [data-testid="stSidebar"] {
        background-color: #f4f4f4;
        border-right: 2px solid #e30613;
    }
    
    /* Başlık ve Yazı Stilleri */
    h1 { color: #e30613; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Bilgi Kutucukları */
    .stAlert { border-radius: 10px; border-left: 5px solid #e30613; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Bağlantısı
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Anahtarı bulunamadı!")

# 3. Yan Panel (Sidebar) - MHRS Logosu ve Menü
with st.sidebar:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    # MHRS Logosu (Resmi MHRS sitesinden çekiliyor)
    st.image("https://mhrs.gov.tr/vatandas/assets/images/mhrs-logo.png", width=180)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### 🏥 Sistem Durumu")
    st.info(f"Tarih: {datetime.now().strftime('%d/%m/%Y')}\n\nKonum: Karaman")
    
    st.write("---")
    st.markdown("### 🔗 Hızlı Erişim")
    st.link_button("MHRS Randevu Al", "https://mhrs.gov.tr/vatandas/#/")
    st.link_button("E-Nabız Giriş", "https://enabiz.gov.tr/")

# 4. Ana Ekran İçeriği
st.markdown("# 🩺 Akıllı Sağlık Danışma ve Yönlendirme")
st.write("Şikayetinizi yazın, yapay zeka sizi en uygun polikliniğe yönlendirsin.")

with st.container():
    sikayet = st.text_area("Belirtilerinizi buraya yazınız:", 
                          placeholder="Örn: Mide yanması ve halsizlik şikayetim var...",
                          height=150)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        analiz_butonu = st.button("🚀 ANALİZ ET VE YÖNLENDİR")

# 5. Analiz ve Sonuç Ekranı
if analiz_butonu and sikayet:
    try:
        with st.spinner('MHRS Protokollerine göre analiz ediliyor...'):
            prompt = f"Sen bir sağlık triyaj asistanısın. Şikayet: '{sikayet}'. Hangi polikliniğe gidilmeli ve aciliyet durumu nedir? MHRS formatında kısa bir rapor sun."
            response = model.generate_content(prompt)
            
            st.markdown("---")
            st.subheader
