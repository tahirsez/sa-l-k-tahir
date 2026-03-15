import streamlit as st
import google.generativeai as genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="T.C. Akıllı Sağlık Asistanı", page_icon="🩺", layout="centered")

# 2. API ve Model Bağlantısı
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Senin anahtarınla çalışan en güncel model:
        model = genai.GenerativeModel('gemini-2.5-flash')
    else:
        st.error("Hata: API anahtarı sisteme tanımlanmamış!")
except Exception as e:
    st.error(f"Sistem bağlantı hatası: {e}")

# 3. Görsel Tasarım (Sidebar)
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #d32f2f;'>TR</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>T.C. Sağlık Teknolojileri</h3>", unsafe_allow_html=True)
    st.write("---")
    st.warning("ÖNEMLİ: Bu sistem sadece ön bilgilendirme amaçlıdır. Acil durumlarda 112'yi arayınız.")

# 4. Ana Ekran
st.title("🩺 Akıllı Sağlık Yönlendirme Asistanı")
st.info("Lütfen şikayetinizi aşağıya detaylıca yazınız.")

sikayet = st.text_area("Şikayetiniz:", placeholder="Örn: Midemde yanma var ve başım dönüyor...")

if st.button("Analiz Et"):
    if sikayet:
        try:
            with st.spinner('Yapay zeka analiz ediyor, lütfen bekleyin...'):
                prompt = f"Sen profesyonel bir sağlık asistanısın. Kullanıcının şu şikayetini analiz et: '{sikayet}'. Hangi polikliniğe gitmesi gerektiğini kısa ve net bir şekilde öner."
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader("Asistanın Önerisi:")
                st.success(response.text)
        except Exception as e:
            st.error("Analiz sırasında bir hata oluştu. Lütfen tekrar deneyin.")
    else:
        st.warning("Lütfen önce bir şikayet yazın.")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.8rem; color: gray;'>Bu proje KMÜ Otomotiv Teknolojisi öğrencisi tarafından geliştirilmiştir.</p>", unsafe_allow_html=True)
