import streamlit as st
import google.generativeai as genai

# 1. Sayfa Ayarları ve Türkçe Başlık
st.set_page_config(page_title="T.C. Akıllı Sağlık Asistanı - Yönlendirme Sistemi", page_icon="🇹🇷")

# 2. API Anahtarınızı Buraya Girin (Eski anahtarınızı buraya yapıştırın)
GOOGLE_API_KEY = "AIzaSyCCjpXSLdvayD-5sy0EHC9YxkWdV9BQexo"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- SİDEBAR (KENAR ÇUBUĞU) TASARIMI ---
with st.sidebar:
    # Sanal bir logo simgesi ve kurum adı
    st.markdown("<h1 style='text-align: center; color: #d32f2f;'>🇹🇷</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>T.C. Sağlık Teknolojileri</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.8rem;'>Dijital Yönlendirme Sistemi</p>", unsafe_allow_html=True)
    st.write("---")
    
    # Bilgi Bölümleri
    st.header("Nasıl Çalışır?")
    st.write("Şikayetinizi ana ekrandaki kutuya yazın. Yapay zeka, belirtilerinizi analiz ederek sizi en uygun polikliniğe yönlendirecektir.")
    
    st.header("Önemli Not")
    st.warning("Bu sistem sadece ön yönlendirme amaçlıdır. Kesinlikle tıbbi tavsiye veya teşhis içermez.")
    
    st.write("---")
    st.header("Sanal İletişim")
    st.write("📧 destek@saglikasistani.gov.tr (Sanal e-posta)")
    st.write("📞 182 (MHRS - Sanal Bilgi)")

# --- ANA EKRAN TASARIMI ---

# Profesyonel Başlık ve Alt Başlık
st.markdown("<h1 style='color: #1565c0;'>🩺 Akıllı Hasta Yönlendirme Asistanı</h1>", unsafe_allow_html=True)
st.markdown("<h4>Lütfen şikayetinizi detaylı bir şekilde aşağıya yazınız.</h4>", unsafe_allow_html=True)

# Gerekli Yasal Uyarı
st.info("Bu asistan, şikayetlerinize göre gitmeniz gereken en uygun hastane bölümünü (polikliniği) önerir. Acil durumlarda lütfen zaman kaybetmeden 112 Acil Çağrı Merkezi'ni arayınız.")

# Kullanıcının şikayetini yazacağı kutucuk
sikayet = st.text_area("Şikayetiniz (Örn: Sol kolumda uyuşma var ve göğsümde sıkışma hissediyorum)", height=150)

# Gönder Butonu
gonder_butonu = st.button("Şikayetimi Analiz Et")

# Eğer butona basılırsa ve kutu boş değilse çalışır:
if gonder_butonu and sikayet:
    # Ekranda profesyonel bir yükleme simgesi
    with st.spinner('Belirtileriniz analiz ediliyor, lütfen bekleyiniz...'):
        
        # Yapay zekaya gizli talimatı gönderiyoruz
        gizli_talimat = f"Sen profesyonel bir sağlık asistanısın. Kullanıcının şikayeti şu: '{sikayet}'. Ona önce geçmiş olsun de. Belirtilerine göre olası çok genel 1-2 sebep söyle ama ASLA kesin teşhis koyma. Son olarak, hastaneden randevu alması için TAM OLARAK hangi bölüme (polikliniğe) gitmesi gerektiğini net bir şekilde söyle."
        
        try:
            cevap = model.generate_content(gizli_talimat)
            
            # Gelen cevabı ekranda şık bir mavi kutu içinde gösteriyoruz
            st.markdown("---")
            st.subheader("Asistanın Ön Değerlendirme ve Yönlendirmesi:")
            st.info(cevap.text)
            st.markdown("<p style='font-size: 0.8rem; color: gray;'>*Bu bir yapay zeka çıktısıdır, doktor muayenesi yerine geçmez.</p>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Bir hata oluştu: API anahtarınızı kontrol edin veya daha sonra tekrar deneyin.")

elif gonder_butonu and not sikayet:
    st.warning("Lütfen şikayetinizi yazdıktan sonra analiz butonuna basınız.")