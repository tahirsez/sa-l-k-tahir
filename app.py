import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Dijital Sağlık Paneli", page_icon="🏥", layout="wide")

# MHRS Kurumsal CSS
st.markdown("""
    <style>
    :root { --mhrs-red: #e30613; }
    .main { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: white; border-right: 3px solid var(--mhrs-red); }
    .stButton>button {
        width: 100%; border-radius: 8px; background-color: var(--mhrs-red);
        color: white; font-weight: bold; height: 3.5rem;
    }
    .stButton>button:hover { background-color: #c40510; }
    </style>
    """, unsafe_allow_html=True)

# 2. API ve Model Bağlantısı
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Anahtarı bulunamadı!")

# 3. Sidebar (Logo ve Menü)
with st.sidebar:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    try:
        # Eğer logo.png yüklediysen bunu görür, yoksa emojiyi basar
        st.image("logo.png", width=160)
    except:
        st.markdown("<h1 style='color:#e30613;'>🏥</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#707070; margin-top:-10px;'>Sağlık Asistanı</h3>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("---")
    st.info(f"📅 {datetime.now().strftime('%d.%m.%Y')}\n\n📍 Karaman Yerleşkesi")
    st.write("---")
    st.link_button("🏥 MHRS Randevu Al", "https://mhrs.gov.tr/vatandas/#/")
    st.link_button("📋 E-Nabız Sistemi", "https://enabiz.gov.tr/")

# 4. Ana Ekran
st.markdown("<h1 style='text-align: center;'>T.C. Akıllı Sağlık Yönlendirme Sistemi</h1>", unsafe_allow_html=True)
st.write("---")

with st.container():
    st.markdown("### 📝 Şikayet Bildirimi")
    sikayet = st.text_area("Lütfen belirtilerinizi detaylıca açıklayınız:", 
                          placeholder="Örn: Şiddetli karın ağrısı ve bulantı...", height=120)
    
    if st.button("ANALİZ ET VE RANDEVU ÖNER"):
        if sikayet:
            # İŞTE BURASI HATA VEREN TRY-EXCEPT BLOĞU
            try:
                with st.spinner('Yapay zeka protokolleri kontrol ediliyor...'):
                    prompt = f"Sen profesyonel bir triyaj asistanısın. Şu şikayeti analiz et: '{sikayet}'. Hangi polikliniğe gidilmeli ve aciliyet derecesi nedir?"
                    response = model.generate_content(prompt)
                
                # Sonuç başarılıysa burayı çalıştırır
                st.markdown("### 📋 Değerlendirme Sonucu")
                st.success(response.text)
                
                st.info("💡 **Öneri:** Randevunuzu MHRS üzerinden hemen oluşturabilirsiniz.")
                st.link_button("👉 MHRS Sistemine Git", "https://mhrs.gov.tr/vatandas/#/")
                
            except Exception as e:
                # İşler ters giderse burayı çalıştırır (SyntaxError'u bu satır çözer)
                st.error(f"Analiz sırasında bir sorun oluştu: {e}")
        else:
            st.warning("Lütfen bir şikayet metni giriniz.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8rem;'>Bu uygulama KMÜ Otomotiv öğrencisi tarafından geliştirilmiştir.</p>", unsafe_allow_html=True)
