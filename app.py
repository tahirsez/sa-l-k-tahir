import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Sağlık Analiz Portalı", page_icon="🩺", layout="wide")

# PROFESYONEL CSS
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .header-container {
        background-color: #e30613;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .content-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #dee2e6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    p, span, label, h1, h2, h3, .stMarkdown { color: #212529 !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 5px solid #e30613 !important; }
    [data-testid="stSidebar"] .stButton>button, [data-testid="stSidebar"] a {
        background-color: #f1f3f5 !important; color: #e30613 !important; border: 1px solid #e30613 !important;
        font-weight: bold !important; text-decoration: none !important;
    }
    .stButton>button {
        background-color: #e30613 !important; color: white !important;
        font-weight: bold !important; border-radius: 8px !important; height: 3.5rem !important;
    }
    /* Hızlı Cevap Butonu İçin Özel Stil */
    .hizli-btn>div>button {
        background-color: #2d2d2d !important;
    }
    .footer-text {
        text-align: center; color: #6c757d !important; margin-top: 50px; font-size: 0.9rem;
        border-top: 1px solid #dee2e6; padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API Bağlantısı
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Anahtarı bulunamadı!")

# 3. Yan Panel
with st.sidebar:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    try:
        st.image("logo.png", width=150)
    except:
        st.markdown("<h1 style='color:#e30613;'>🩺</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #212529;'>DİJİTAL SAĞLIK<br>ASİSTANI</h3>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("---")
    st.link_button("🏥 MHRS Randevu Sistemi", "https://mhrs.gov.tr/vatandas/#/")
    st.link_button("📑 E-Nabız Portalı", "https://enabiz.gov.tr/")
    st.write("---")
    st.caption(f"🗓️ {datetime.now().strftime('%d.%m.%Y')} | 📍 Karaman")

# 4. Ana Ekran
st.markdown("<div class='header-container'><h1 style='color: white !important; margin:0; font-size: 26px;'>AKILLI SAĞLIK ANALİZ VE YÖNLENDİRME SİSTEMİ</h1></div>", unsafe_allow_html=True)

col1, col_mid, col2 = st.columns([1, 10, 1])

with col_mid:
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Şikayet Bildirimi")
    sikayet = st.text_area("Belirtileriniz:", placeholder="Örn: Şiddetli baş ağrısı...", height=150, label_visibility="collapsed")
    
    st.write("")
    
    # BUTONLARI YAN YANA KOYALIM
    btn_col1, btn_col2 = st.columns([1, 1])
    
    with btn_col1:
        detayli_analiz = st.button("🚀 DETAYLI ANALİZ BAŞLAT")
    
    with btn_col2:
        # Bu butonu CSS ile biraz farklılaştırdık
        st.markdown("<div class='hizli-btn'>", unsafe_allow_html=True)
        hizli_cevap = st.button("⚡ HIZLI CEVAP AL")
        st.markdown("</div>", unsafe_allow_html=True)

    # İŞLEME MANTIĞI
    if detayli_analiz or hizli_cevap:
        if sikayet:
            try:
                with st.spinner('Analiz ediliyor...'):
                    if detayli_analiz:
                        prompt = f"Şikayet: '{sikayet}'. 5 başlıkta (Analiz, Poliklinik, Aciliyet, Tavsiye, Uyarı) DETAYLI analiz yap."
                    else:
                        prompt = f"Şikayet: '{sikayet}'. Sadece hangi poliklinik ve aciliyet durumu olduğunu 2 kısa cümlede söyle."
                    
                    response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown("#### 🩺 Analiz Sonucu")
                st.info(response.text)
                st.link_button("👉 MHRS'den Randevu Al", "https://mhrs.gov.tr/vatandas/#/")
            except Exception as e:
                st.error(f"Hata: {e}")
        else:
            st.warning("Lütfen bir şikayet yazınız.")
    st.markdown("</div>", unsafe_allow_html=True)

# 5. FOOTER
st.markdown("""<div class='footer-text'>Bu uygulama KMÜ Otomotiv Teknolojisi öğrencisi <b>Tahir Sezen</b> tarafından geliştirilmiştir. © 2026</div>""", unsafe_allow_html=True)
