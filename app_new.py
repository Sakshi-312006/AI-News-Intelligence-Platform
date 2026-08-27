import streamlit as st

from modules.extractor import extract_article
from modules.classifier import predict_category
from modules.sentiment import analyze_sentiment
from modules.keyword_extractor import extract_keywords
from modules.ner import extract_entities
from modules.summarizer import summarize_article
from modules.qa import answer_question


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI News Intelligence Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# DARK FRONTEND
# ============================================================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 15% 15%, rgba(30,95,255,.12), transparent 30%),
        radial-gradient(circle at 85% 25%, rgba(190,40,255,.10), transparent 30%),
        #02050d;
    color: #f7f8ff;
}
#MainMenu, footer { visibility: hidden; }
section[data-testid="stSidebar"] { display: none; }

.main .block-container {
    max-width: 1450px;
    padding: 1.5rem 2.5rem 2.5rem;
}

.main-title {
    text-align:center;
    font-size:50px;
    font-weight:850;
    line-height:1.1;
    margin:5px 0;
    background:linear-gradient(90deg,#2d8cff,#8d42ff,#ec42d1);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.main-subtitle {
    text-align:center;
    font-size:21px;
    font-weight:600;
    color:#f2f4ff !important;
}
.main-description {
    text-align:center;
    font-size:15px;
    color:#9da8bc !important;
    margin-bottom:25px;
}



div[data-baseweb="input"],
div[data-baseweb="textarea"] {
    background:#050a14 !important;
}
div[data-baseweb="input"] input,
textarea {
    color:#f4f6ff !important;
    background:#050a14 !important;
    caret-color:#fff !important;
}
div[data-baseweb="input"] input::placeholder,
textarea::placeholder {
    color:#657188 !important;
}
[data-testid="stRadio"] label { color:#e7ebf5 !important; }

.stButton > button {
    width:100%;
    min-height:45px;
    border-radius:9px;
    background:linear-gradient(90deg,#237cff,#8742ff,#d83cc7);
    border:1px solid rgba(120,120,255,.35);
    color:#fff !important;
    font-weight:700;
}
.stButton > button p,
.stButton > button span { color:#fff !important; }
.stButton > button:hover {
    border-color:#8e6cff;
    box-shadow:0 0 22px rgba(90,90,255,.28);
}

.cap-card {
    background:linear-gradient(145deg,rgba(7,14,27,.92),rgba(3,8,17,.98));
    border:1px solid rgba(65,85,125,.30);
    border-radius:11px;
    padding:12px 14px;
    min-height:58px;
}
.cap-title { font-size:13px; font-weight:700; color:#fff !important; }
.cap-text { font-size:10px; color:#8995aa !important; margin-top:2px; }

.success-box {
    text-align:center;
    background:linear-gradient(145deg,rgba(9,38,31,.82),rgba(3,18,18,.92));
    border:1px solid rgba(41,219,146,.35);
    border-radius:14px;
    padding:19px;
    margin:5px 0 24px;
}
.success-title { color:#55f0a7 !important; font-size:21px; font-weight:800; }
.success-subtitle { color:#a7b4c8 !important; font-size:13px; margin-top:4px; }

.section-heading {
    text-align:center;
    font-size:20px;
    font-weight:800;
    color:#f3f5ff !important;
    margin:10px 0 17px;
}

.feature-card {
    background:linear-gradient(145deg,rgba(11,20,36,.96),rgba(5,10,20,.98));
    border:1px solid rgba(73,93,130,.27);
    border-radius:12px;
    padding:19px;
    min-height:150px;
    margin-bottom:7px;
}
.feature-icon { font-size:29px; margin-bottom:8px; }
.feature-title { color:#fff !important; font-size:17px; font-weight:800; }
.feature-description { color:#9ba7bc !important; font-size:12px; line-height:1.45; margin-top:6px; }

.result-card {
    background:linear-gradient(145deg,rgba(10,18,32,.96),rgba(4,9,18,.98));
    border:1px solid rgba(72,92,128,.30);
    border-radius:13px;
    padding:22px;
    margin-bottom:18px;
}
.result-label { color:#8e9ab0 !important; font-size:12px; margin-bottom:6px; }
.result-value { color:#fff !important; font-size:27px; font-weight:800; }

[data-testid="stMetricValue"] { color:#fff !important; }
[data-testid="stMetricLabel"] { color:#a0acc0 !important; }
hr { border-color:rgba(91,107,140,.25) !important; }

[data-testid="stDownloadButton"] button {
    width:100%;
    min-height:50px;
    border-radius:9px;
    background:linear-gradient(90deg,#7b35ff,#d737c9) !important;
    color:#fff !important;
    border:1px solid rgba(220,90,230,.40) !important;
    font-weight:800;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "page": "Home",
    "article_text": "",
    "article_title": "",
    "article_url": "",
    "classification": None,
    "sentiment": None,
    "keywords": [],
    "entities": [],
    "summary": "",
    "last_question": "",
    "last_answer": "",
    "analysis_complete": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_analysis():
    for key, value in defaults.items():
        st.session_state[key] = value
    st.session_state.page = "Home"


def run_analysis(article_text):
    with st.spinner("Running preprocessing and NLP analysis..."):

        print("\n===== SENTIMENT INPUT DEBUG =====")
        print("Characters:", len(article_text))
        print("Words:", len(article_text.split()))

        print("\nFIRST 1000 CHARACTERS:")
        print(article_text[:1000])

        print("\nLAST 500 CHARACTERS:")
        print(article_text[-500:])

        classification = predict_category(article_text)
        sentiment = analyze_sentiment(article_text)

        print("\n===== FINAL SENTIMENT RESULT =====")
        print(sentiment)

        keywords = extract_keywords(article_text, top_n=10)
        entities = extract_entities(article_text)

    st.session_state.classification = classification
    st.session_state.sentiment = sentiment
    st.session_state.keywords = keywords
    st.session_state.entities = entities
    st.session_state.analysis_complete = True


def build_report():
    classification = st.session_state.classification or {}
    sentiment = st.session_state.sentiment or {}
    scores = sentiment.get("scores", {})

    lines = [
        "AI NEWS INTELLIGENCE PLATFORM",
        "=" * 60,
        "",
        "ARTICLE INFORMATION",
        "-" * 60,
        f"Title: {st.session_state.article_title}",
        f"URL: {st.session_state.article_url or 'User-provided article text'}",
        "",
        "NEWS CATEGORY",
        "-" * 60,
        f"Category: {classification.get('category', 'Not available')}",
        f"Confidence: {classification.get('confidence', 0) * 100:.2f}%",
        "",
        "SENTIMENT ANALYSIS",
        "-" * 60,
        f"Overall Sentiment: {sentiment.get('sentiment', 'Not available')}",
        f"Sentiment Strength: {sentiment.get('sentiment_strength', 0):.3f}",
        f"Compound Score: {sentiment.get('compound', 0):.3f}",
        f"Positive: {scores.get('pos', 0):.3f}",
        f"Neutral: {scores.get('neu', 0):.3f}",
        f"Negative: {scores.get('neg', 0):.3f}",
        "",
        "KEYWORDS",
        "-" * 60,
    ]

    if st.session_state.keywords:
        for word, score in st.session_state.keywords:
            lines.append(f"{word} - {score:.4f}")
    else:
        lines.append("No keywords available.")

    lines += ["", "NAMED ENTITIES", "-" * 60]

    if st.session_state.entities:
        for entity in st.session_state.entities:
            lines.append(
                f"{entity.get('text','')} | "
                f"{entity.get('label','')} | "
                f"{entity.get('description','')}"
            )
    else:
        lines.append("No named entities detected.")

    lines += [
        "",
        "AI INSIGHTS",
        "-" * 60,
        st.session_state.summary if st.session_state.summary
        else "AI summary has not been generated yet.",
        "",
        "ASK AI",
        "-" * 60,
    ]

    if st.session_state.last_answer:
        lines += [
            f"Question: {st.session_state.last_question}",
            f"Answer: {st.session_state.last_answer}",
        ]
    else:
        lines.append("No Ask AI question has been submitted yet.")

    return "\n".join(lines)


# ============================================================
# PAGE 1 — INPUT
# ============================================================

def show_home():

    st.markdown('<div class="main-title">🧠 AI News Intelligence</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">Advanced News Analytics Platform</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="main-description">'
        'Extract, Analyze, Understand, Get AI-Powered Insights from any news article.'
        '</div>',
        unsafe_allow_html=True
    )

    

    input_method = st.radio(
        "Input Method",
        ["🔗 Enter Article URL", "📝 Enter Article Text"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if input_method == "🔗 Enter Article URL":
        url = st.text_input(
            "Enter Article URL",
            placeholder="https://example.com/news/article",
            key="home_url"
        )
        text = ""
    else:
        text = st.text_area(
            "Enter Article Text",
            placeholder="Paste your article text here...",
            height=180,
            key="home_text"
        )
        url = ""

    
    st.write("")

    if st.button("🚀 Analyze Article", use_container_width=True):

        if url.strip():

            try:
                with st.spinner("Extracting article..."):
                    article = extract_article(url.strip())

                extracted_text = article.get("text", "")
                extracted_title = article.get("title", "")

                if not extracted_text:
                    st.error(
                        "Could not extract article text. "
                        "Please try the Article Text option."
                    )
                    return

                st.session_state.article_text = extracted_text
                st.session_state.article_title = extracted_title or "Untitled Article"
                st.session_state.article_url = url.strip()

            except Exception as e:
                st.error(f"Article extraction failed: {e}")
                return

        elif text.strip():

            st.session_state.article_text = text.strip()
            st.session_state.article_title = "User Provided Article"
            st.session_state.article_url = ""

        else:
            st.warning("Please enter an article URL or article text.")
            return

        try:
            run_analysis(st.session_state.article_text)
            st.session_state.page = "Dashboard"
            st.rerun()
        except Exception as e:
            st.error(f"Analysis failed: {e}")

    st.write("")

    c1, c2, c3, c4 = st.columns(4)
    capability_data = [
        ("🧠", "AI Powered", "Advanced AI Models"),
        ("💬", "NLP Analysis", "Deep Text Understanding"),
        ("＋", "Real-time", "Instant Results"),
        ("✦", "Secure", "Your Privacy Matters"),
    ]

    for col, (icon, title, text) in zip([c1, c2, c3, c4], capability_data):
        with col:
            st.markdown(
                f"""
                <div class="cap-card">
                    <div class="cap-title">{icon} {title}</div>
                    <div class="cap-text">{text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# PAGE 2 — DASHBOARD
# ============================================================

def show_dashboard():

    st.markdown(
        """
        <div class="success-box">
            <div class="success-title">✓ Analysis Completed Successfully!</div>
            <div class="success-subtitle">
                Your article has been analyzed using the existing AI/NLP pipeline.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-heading">Explore Analysis Features</div>',
        unsafe_allow_html=True
    )

    features = [
        ("🏷️", "News Category", "View predicted category and confidence score.", "Category"),
        ("😊", "Sentiment Analysis", "Analyze sentiment and emotion of the article.", "Sentiment"),
        ("🔑", "Keywords", "Explore important keywords extracted from the article.", "Keywords"),
        ("👥", "Named Entities", "Identify people, organizations, locations and more.", "Entities"),
        ("🤖", "AI Insights", "Get an AI-powered concise summary of the article.", "AI Insights"),
        ("💬", "Ask AI", "Ask questions and get AI-powered answers.", "Ask AI"),
    ]

    for row in range(2):
        cols = st.columns(3)

        for col, feature in zip(cols, features[row * 3:(row + 1) * 3]):
            icon, title, description, page_name = feature

            with col:
                st.markdown(
                    f"""
                    <div class="feature-card">
                        <div class="feature-icon">{icon}</div>
                        <div class="feature-title">{title}</div>
                        <div class="feature-description">{description}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    f"Open {title}  →",
                    key=f"feature_{page_name}",
                    use_container_width=True
                ):
                    st.session_state.page = page_name
                    st.rerun()

        st.write("")

    st.divider()
    left, right = st.columns(2)

    with left:
        if st.button("↻  Analyze Another Article",
                     key="analyze_another",
                     use_container_width=True):
            reset_analysis()
            st.rerun()

    with right:
        st.download_button(
            "⇩  Download Report",
            data=build_report(),
            file_name="AI_News_Intelligence_Report.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ============================================================
# INDIVIDUAL FEATURE PAGES
# ============================================================

def back_to_dashboard():
    if st.button("← Back to Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()


def show_category():
    back_to_dashboard()
    st.markdown(
        '<div class="main-title" style="font-size:42px;">🏷️ News Category</div>',
        unsafe_allow_html=True
    )

    result = st.session_state.classification or {}
    category = result.get("category", "Not available")
    confidence = result.get("confidence", 0)

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">Predicted Category</div>
            <div class="result-value">{category}</div>
            <br>
            <div class="result-label">Confidence Score</div>
            <div class="result-value">{confidence * 100:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_sentiment():
    back_to_dashboard()

    st.markdown(
        '<div class="main-title" style="font-size:42px;">😊 Sentiment Analysis</div>',
        unsafe_allow_html=True
    )

    sentiment = st.session_state.sentiment or {}

    overall = sentiment.get("sentiment", "Not available")
    strength = sentiment.get("sentiment_strength", 0)

    # Main sentiment result
    if overall == "Positive":
        st.success("🟢 Positive")

    elif overall == "Negative":
        st.error("🔴 Negative")

    else:
        st.info("⚪ Neutral")

    # Sentiment strength
    st.metric(
        "Sentiment Strength",
        f"{strength * 100:.1f}%"
    )
    
def show_keywords():
    back_to_dashboard()
    st.markdown(
        '<div class="main-title" style="font-size:42px;">🔑 Keywords</div>',
        unsafe_allow_html=True
    )

    keywords = st.session_state.keywords or []

    if not keywords:
        st.info("No keywords were detected.")
        return

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    for word, score in keywords:
        st.markdown(f"**{word}** — `{score:.4f}`")
    st.markdown("</div>", unsafe_allow_html=True)


def show_entities():
    back_to_dashboard()
    st.markdown(
        '<div class="main-title" style="font-size:42px;">👥 Named Entities</div>',
        unsafe_allow_html=True
    )

    entities = st.session_state.entities or []

    if not entities:
        st.info("No named entities detected.")
        return

    rows = [
        {
            "Entity": e.get("text", ""),
            "Type": e.get("label", ""),
            "Description": e.get("description", ""),
        }
        for e in entities
    ]

    st.dataframe(rows, use_container_width=True, hide_index=True)


def show_ai_insights():
    back_to_dashboard()
    st.markdown(
        '<div class="main-title" style="font-size:42px;">🤖 AI Insights</div>',
        unsafe_allow_html=True
    )

    st.write("Generate an AI-powered concise summary of the analyzed article.")

    if st.button("✨ Generate AI Summary", use_container_width=True):
        with st.spinner("Generating the summary..."):
            try:
                st.session_state.summary = summarize_article(
                    st.session_state.article_text
                )
            except Exception as e:
                st.error(f"Summary generation failed: {e}")

    if st.session_state.summary:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">AI Generated Summary</div>
                <div style="color:#e6eaf4 !important;line-height:1.7;">
                    {st.session_state.summary}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def show_ask_ai():
    back_to_dashboard()
    st.markdown(
        '<div class="main-title" style="font-size:42px;">💬 Ask AI</div>',
        unsafe_allow_html=True
    )

    st.write("Ask questions about the analyzed article.")

    question = st.text_input(
        "Your question",
        placeholder="What is the main issue discussed?",
        key="question_input"
    )

    if st.button("💬 Get Answer", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("AI is analyzing the article..."):
                try:
                    answer = answer_question(
                        st.session_state.article_text,
                        question
                    )
                    st.session_state.last_question = question
                    st.session_state.last_answer = answer
                except Exception as e:
                    st.error(f"Question answering failed: {e}")

    if st.session_state.last_answer:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">AI Answer</div>
                <div style="color:#e6eaf4 !important;line-height:1.7;">
                    {st.session_state.last_answer}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ROUTER
# ============================================================

if st.session_state.page == "Home":
    show_home()
elif st.session_state.page == "Dashboard":
    show_dashboard()
elif st.session_state.page == "Category":
    show_category()
elif st.session_state.page == "Sentiment":
    show_sentiment()
elif st.session_state.page == "Keywords":
    show_keywords()
elif st.session_state.page == "Entities":
    show_entities()
elif st.session_state.page == "AI Insights":
    show_ai_insights()
elif st.session_state.page == "Ask AI":
    show_ask_ai()
