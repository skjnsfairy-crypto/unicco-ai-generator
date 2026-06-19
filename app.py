import streamlit as st
import google.generativeai as genai
import json

# ----------------------------
# Konfigurasi halaman
# ----------------------------
st.set_page_config(
    page_title="Unicco Cookies - AI Content Generator",
    page_icon="🍪",
    layout="centered"
)

# ----------------------------
# Konstanta
# ----------------------------
PRODUK_OPTIONS = [
    "Soft cookies coklat",
    "Cookie bites",
    "Giant cookie",
    "Cookie tart",
    "Muffin cookie",
]

MOOD_OPTIONS = [
    "Testimoni & trust",
    "Highlight produk",
    "Promo / diskon",
    "Edukasi (penyimpanan, masa simpan)",
    "Relatable / FYP",
]

PLATFORM_OPTIONS = ["Instagram", "TikTok", "Facebook"]

STYLE_GUIDE = {
    "Instagram": "gaya santai, hangat, bisa pakai emoji secukupnya, caption 2-4 kalimat plus call to action ringan",
    "TikTok": "gaya gen-z, catchy, ngikutin tren bahasa kekinian, caption singkat dan punchy, cocok untuk hook video",
    "Facebook": "gaya lebih hangat dan informatif, sedikit lebih panjang, cocok untuk audiens ibu rumah tangga, tetap ramah",
}

# ----------------------------
# Fungsi pemanggilan AI
# ----------------------------
def generate_content_ideas(api_key, produk, mood, platform):

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    Kamu adalah Digital Marketing Specialist untuk UMKM Unicco Cookies.

    Produk: {produk}
    Tema: {mood}
    Platform: {platform}

    Gaya bahasa:
    {STYLE_GUIDE[platform]}

    Buatkan 3 ide konten beserta caption.

    Balas HANYA dalam format JSON:

    [
      {{
        "ide": "judul ide",
        "caption": "caption lengkap"
      }}
    ]

    Tepat 3 item.
    """

    response = model.generate_content(prompt)

    text = response.text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")

    return json.loads(text)


# ----------------------------
# UI
# ----------------------------
st.title("🍪 AI Content Idea & Caption Generator")
st.caption("Prototype untuk Unicco Cookies — bagian dari solusi rekomendasi AI pemasaran")

api_key_input = st.secrets["GEMINI_API_KEY"]

st.subheader("1. Masukkan detail konten")

col1, col2 = st.columns(2)
with col1:
    produk = st.selectbox("Jenis produk", PRODUK_OPTIONS)
with col2:
    platform = st.selectbox("Platform target", PLATFORM_OPTIONS)

mood = st.radio("Mood / tema konten", MOOD_OPTIONS)

st.subheader("2. Generate")
generate_clicked = st.button("✨ Generate ide & caption", type="primary", use_container_width=True)

if generate_clicked:

    if not api_key_input:
        st.error("Masukkan Gemini API Key terlebih dahulu.")
    else:

        try:
            with st.spinner("AI sedang membuat ide konten..."):

                ideas = generate_content_ideas(
                    api_key_input,
                    produk,
                    mood,
                    platform
                )

                st.session_state["ideas"] = ideas
                st.session_state["last_platform"] = platform

        except Exception as e:
            st.error(f"Error: {e}")

# ----------------------------
# Tampilkan hasil
# ----------------------------
if "ideas" in st.session_state:
    st.subheader("3. Hasil")
    st.caption(f"3 varian untuk {st.session_state['last_platform']} — pilih, edit ringan, lalu posting")

    for i, item in enumerate(st.session_state["ideas"], start=1):
        with st.container(border=True):
            st.markdown(f"**{i}. {item['ide']}**")
            st.write(item["caption"])
            st.code(item["caption"], language=None)
