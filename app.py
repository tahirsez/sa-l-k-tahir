import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Akıllı Sağlık Asistanı", page_icon="🩺")

# 1. API Bağlantısı ve Akıllı Model Seçimi
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # 404 Hatasını önlemek için sırayla modelleri deniyoruz
        model_isimleri = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-2.0-flash']
        model_bulundu = False
        
        for isim in model_isimleri:
            try:
                model = genai.GenerativeModel(model_name=isim)
                # Küçük bir test yapalım (model gerçekten var mı?)
                model_bulundu = True
                aktif_model = isim
                break
            except:
                continue
        
        if not model_bulundu:
            st.error("Uygun bir yapay zeka modeli bulunamadı. Lütfen API anahtarınızı kontrol edin.")
    else:
        st.error("Secrets kutusunda GOOGLE_API_KEY bulunamadı!")
except Exception as e:
    st.error(f"Sistem hatası: {e}")

st.title("🩺 Akıllı Sağlık Yönlendirme")
st.write(f"Sistem Aktif (Model: {aktif_model if model_bulundu else 'Bağlanamadı'})")

sikayet = st.text_area("Şikayetiniz:", placeholder="Örn: Midemde yanma var...")

if st.button("Analiz Et"):
    if sikayet:
        try:
            with st.spinner('Yapay zeka analiz ediyor...'):
                response = model.generate_content(f"Bir sağlık asistanı olarak şu şikayeti değerlendir ve poliklinik öner: {sikayet}")
                st.success(response.text)
        except Exception as e:
            st.error(f"Üretim hatası: {e}")
    else:
        st.warning("Lütfen bir şikayet yazın.")
