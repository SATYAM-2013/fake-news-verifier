import streamlit as st
import requests
from utils.history import add_history, get_history

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Fake News Verifier",
    layout="centered"
)

# ---------------- Sidebar History ----------------
st.sidebar.title("🕘 Recent Checks")
history = get_history()

if history:
    for h in reversed(history):
        st.sidebar.markdown(
            f"**{h['time']}**  \n{h['claim']}  \n🟢 *{h['verdict']}*"
        )
else:
    st.sidebar.info("No history yet.")

# ---------------- Title ----------------
st.title("📰 Fake News Verification System")
st.caption("Hybrid AI + Fact-Check based verification")

# ---------------- Input ----------------
news = st.text_area(
    "Paste news text here:",
    height=130,
    placeholder="Example: WHO says COVID vaccines do not cause infertility"
)

# ---------------- Action ----------------
if st.button("Verify"):

    # Basic validation
    if not news.strip():
        st.warning("⚠️ Please enter a news claim.")
        st.stop()

    if len(news.split()) < 4:
        st.warning("⚠️ Please enter a complete sentence.")
        st.stop()

    # ---------------- Call FastAPI Backend ----------------
    with st.spinner("🔍 Verifying with backend AI..."):
        try:
            import os

            BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

            response = requests.post(
                f"{BACKEND_URL}/verify",
                json={"text": news},
                timeout=15
            )

        except requests.exceptions.RequestException:
            st.error("❌ Backend is not running. Start FastAPI first.")
            st.stop()

        if response.status_code != 200:
            st.error("❌ Backend error. Please try again.")
            st.stop()

        decision = response.json()

    verdict = decision.get("verdict", "Uncertain")
    reason = decision.get("reason", "")
    confidence = decision.get("confidence", 0)
    ml_label = decision.get("ml_label", "unknown")
    sources = decision.get("sources", [])

    # Save to history
    add_history(news, verdict)

    # ---------------- Final Verdict ----------------
    st.subheader("🔍 Final Verdict")

    if verdict.lower() == "fake news":
        st.error(f"❌ {verdict}")
    elif verdict.lower() == "likely true news":
        st.success(f"✅ {verdict}")
    else:
        st.warning(f"⚠️ {verdict}")

    st.write(reason)

    # ---------------- Explanation ----------------
    st.subheader("🧠 Explanation")
    st.markdown(
        f"""
- **AI Prediction:** `{ml_label.upper()}`
- **AI Confidence:** `{confidence * 100:.1f}%`
- **Fact-check sources found:** `{len(sources)}`
"""
    )

    # ---------------- Confidence Bar ----------------
    st.subheader("📊 AI Confidence")
    st.progress(min(max(confidence, 0), 1))

    # ---------------- Sources ----------------
    if sources:
        st.subheader("🔗 Fact-check Sources")
        for src in sorted(set(sources)):
            st.markdown(f"- [{src}]({src})")
    else:
        st.info("No external fact-check sources found.")

# ---------------- Footer ----------------
st.divider()
st.caption(
    "⚠️ This system assists in misinformation detection. "
    "Always verify important information from trusted outlets."
)
