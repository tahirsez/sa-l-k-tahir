import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Sayfa Konfigürasyonu
st.set_page_config(page_title="Akıllı Sağlık Paneli", page_icon="🩺", layout="wide")

# PROFESYONEL CSS (Sağ tarafı ve yazıları düzelten bölüm)
st.markdown("""
    <style>
    /* Bembeyaz Arka Plan Zorlaması */
    .stApp { background-color: #ffffff; }
    
    /* Üst Panel Tasarımı */
    .header-bar {
        background-color: #e30613;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(227, 6, 19, 0.2);
    }
    .header-text {
        color: white !important;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 700;
        letter-spacing: 2px;
        margin: 0;
        font-size: 24px;
    }

    /* Yazı Alanı ve Fontlar */
    .stTextArea label {
        color: #e30613 !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
    }
    
    /* Buton Tasarımı (Hover Efektli) */
    .stButton>button {
        background-color: #e30613 !important;
        color: white !important;
        border: none !important;
        height: 3.5rem !important;
        width: 100% !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2d2d2d !important;
        transform: scale(1.02);
    }

    /* Yan Panel Estetiği */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        border-right: 5px solid #e30613 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API ve Model (Senin canavar 2.5-flash)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Anahtarı bulunamadı!")

# 3. YAN PANEL (Sidebar)
with st.sidebar:
    st.markdown("<div style='text-align: center; padding: 20px;'>", unsafe_allow_html=True)
    try:
        st.image("logo.png", width=160)
    except:
        st.markdown("<h1 style='color:#e30613; font-size: 80px;'>🩺</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #2d2d2d;'>DİJİTAL SAĞLIK<br>ASİSTANI</h3>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("#### 🛠️ HIZLI İŞLEMLER")
    st.link_button("🏥 Randevu Sistemi", "https://mhrs.gov.tr/vatandas/#/")
    st.link_button("📑 E-Nabız Portalı", "https://enabiz.gov.tr/")
    
    st.write("---")
    st.caption(f"🗓️ Tarih: {datetime.now().strftime('%d.%m.%Y')}")
    st.caption("📍 KMÜ / Karaman Yerleşkesi")

# 4. ANA EKRAN (Üst Panel ve Giriş)
st.markdown("""
    <div class='header-bar'>
        <p class='header-text'>AKILLI SAĞLIK VE ANALİZ SİSTEMİ</p>
    </div>
    """, unsafe_allow_html=True)

# İçerik Alanı
col1, col2, col3 = st.columns([1, 6, 1]) # Ortalamak için kolon kullanıyoruz

with col2:
    st.markdown("### 📋 Şikayet Giriş Formu")
    st.write("Lütfen yaşadığınız belirtileri aşağıya detaylıca yazınız.")
    
    sikayet = st.text_area("Belirtileriniz:", placeholder="Örn: 2 gündür süren eklem ağrısı ve halsizlik...", height=180, label_visibility="collapsed")
    
    st.write("") # Boşluk
    
    if st.button("SİSTEM ANALİZİNİ BAŞLAT"):
        if sikayet:
            try:
                with st.spinner('Yapay zeka verileri tarıyor...'):
                    prompt = f"Sen bir sağlık triyaj asistanısın. Şu şikayeti profesyonel ve kısa bir rapor haline getir: '{sikayet}'. Hangi poliklinik seçilmeli?"
                    response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown("#### 🩺 Yapay Zeka Ön Değerlendirmesi")
                st.success(response.text)
                
                # Alt Yönlendirme
                st.info("💡 **Bilgi:** Analiz sonucuna göre randevunuzu yukarıdaki sistem üzerinden alabilirsiniz.")
            except Exception as e:
                st.error(f"Bir sorun oluştu: {e}")
        else:
            st.warning("Analiz için lütfen bir şikayet metni giriniz.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #999; font-size: 0.9rem;'>Bu portal Karaman KMÜ öğrencisi Tahir Sezen tarafından geliştirilmiştir. © 2026</p>", unsafe_allow_html=True)
