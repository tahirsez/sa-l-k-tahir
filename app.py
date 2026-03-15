import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Sayfa Ayarları ve Tema
st.set_page_config(page_title="T.C. Akıllı Sağlık Sistemi", page_icon="🏥", layout="wide")

# Özel CSS ile Profesyonel Görünüm
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #d32f2f; color: white; height: 3em; font-weight: bold; }
    .stTextArea>div>div>textarea { border-radius: 15px; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e7d32,#1b5e20); color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Bağlantısı
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Anahtarı bulunamadı!")

# Session State (Geçmişi tutmak için)
if 'gecmis' not in st.session_state:
    st.session_state.gecmis = []

# 3. Yan Panel (Sidebar)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/tr/b/b2/T.C._Sa%C4%9Fl%C4%B1k_Bakanl%C4%B1%C4%9Fe_Logo.png", width=100)
    st.title("Sistem Bilgileri")
    st.info(f"Tarih: {datetime.now().strftime('%d/%m/%Y')}")
    st.write("---")
    if st.button("Sohbeti Sıfırla"):
        st.session_state.gecmis = []
        st.rerun()

# 4. Ana Ekran Başlıkları
col1, col2 = st.columns([1, 4])
with col1:
    st.write("") # Boşluk
with col2:
    st.title("🩺 Dijital Sağlık ve Yönlendirme Paneli")
    st.caption("Yapay Zeka Destekli Ön Analiz Sistemi")

# 5. Kullanıcı Giriş Alanı
with st.container():
    st.write("---")
    sikayet = st.text_area("Lütfen yaşadığınız belirtileri detaylıca anlatın:", 
                          placeholder="Örn: 2 gündür süren şiddetli karın ağrısı, bulantı ve yüksek ateş...",
                          height=150)
    
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        analiz_et = st.button("🚀 Kapsamlı Analiz Yap")

# 6. Analiz Süreci ve Sonuç
if analiz_et and sikayet:
    try:
        with st.spinner('Tıbbi veritabanı taranıyor ve analiz ediliyor...'):
            # Daha profesyonel bir prompt (komut)
            prompt = f"""
            Sen uzman bir triyaj (hasta sınıflandırma) asistanısın. 
            Aşağıdaki belirtileri analiz et: '{sikayet}'
            Cevabını şu formatta ver:
            1. OLASI BÖLÜM: (Hangi poliklinik?)
            2. ACİLİYET: (10 üzerinden bir puan ver ve nedenini açıkla)
            3. ÖNERİLEN ADIMLAR: (Kısa ve öz tavsiyeler)
            4. UYARI: (Mutlaka tıbbi tavsiye olmadığını belirt)
            """
            response = model.generate_content(prompt)
            sonuc = response.text
            
            # Geçmişe ekle
            st.session_state.gecmis.append({"zaman": datetime.now().strftime("%H:%M"), "soru": sikayet, "cevap": sonuc})
            
            # Ekrana Yazdır
            st.subheader("📋 Analiz Raporu")
            st.success(sonuc)
            
            # Raporu İndirme Butonu
            st.download_button(label="📄 Raporu İndir (.txt)", 
                             data=sonuc, 
                             file_name=f"saglik_raporu_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                             mime="text/plain")
            
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")

# 7. Geçmiş Bölümü (History)
if st.session_state.gecmis:
    st.write("---")
    st.subheader("📜 Önceki Analizleriniz")
    for item in reversed(st.session_state.gecmis):
        with st.expander(f"Saat {item['zaman']} - {item['soru'][:30]}..."):
            st.write(item['cevap'])

# Footer
st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>Bu uygulama yapay zeka teknolojisi kullanılarak KMÜ öğrencisi tarafından geliştirilmiştir.</p>", unsafe_allow_html=True)
