import streamlit as st
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchAgent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:          #0a0d12;
    --surface:     #111520;
    --border:      #1e2535;
    --accent:      #4f8ef7;
    --accent2:     #a78bfa;
    --success:     #34d399;
    --warn:        #fbbf24;
    --text:        #e2e8f0;
    --muted:       #64748b;
    --mono:        'Space Mono', monospace;
    --sans:        'DM Sans', sans-serif;
}

/* Global reset */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans);
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero header ── */
.hero {
    padding: 1rem 0 1rem;
    text-align: center;
}
.hero h1 {
    font-family: var(--mono);
    font-size: 2.2rem;
    letter-spacing: -1px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.hero p {
    color: var(--muted);
    font-size: 0.9rem;
    margin-top: 0.2rem;
    letter-spacing: 0.5px;
}

/* ── Input card ── */
.input-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
}

/* ── Step tracker ── */
.steps-row {
    display: flex;
    gap: 0;
    margin: 0.5rem 0 1rem 0;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--border);
}
.step-pill {
    flex: 1;
    text-align: center;
    padding: 0.7rem 0.5rem;
    font-family: var(--mono);
    font-size: 0.72rem;
    letter-spacing: 0.3px;
    background: var(--surface);
    color: var(--muted);
    border-right: 1px solid var(--border);
    transition: all .3s ease;
    position: relative;
}
.step-pill:last-child { border-right: none; }
.step-pill.active {
    background: rgba(79,142,247,.15);
    color: var(--accent);
}
.step-pill.done {
    background: rgba(52,211,153,.08);
    color: var(--success);
}
.step-pill .icon { font-size: 1rem; display: block; margin-bottom: 2px; }

/* ── Output section cards (kept for compatibility, though using native tabs now) ── */
.section-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    transition: border-color .2s;
}
.section-card:hover { border-color: #2d3a55; }
.section-title {
    font-family: var(--mono);
    font-size: 0.78rem;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-title .badge {
    font-size: 0.65rem;
    padding: 2px 8px;
    border-radius: 20px;
    background: rgba(79,142,247,.15);
    color: var(--accent);
    letter-spacing: 0.8px;
}
.section-body {
    font-size: 0.9rem;
    line-height: 1.6;
    color: #c4cfe3;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Critique card accent ── */
.section-card.critique { border-left: 3px solid var(--accent2); }
.section-card.critique .section-title { color: var(--accent2); }
.section-card.critique .badge { background: rgba(167,139,250,.15); color: var(--accent2); }

/* ── Custom Tabs Styling ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: var(--surface);
    padding: 8px;
    border-radius: 12px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    height: 40px;
    background-color: transparent;
    border-radius: 8px;
    color: var(--muted);
    font-family: var(--mono);
    font-size: 0.85rem;
    padding: 0 16px;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(79,142,247,0.15) !important;
    color: var(--accent) !important;
}

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input {
    background: #0d1018 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
    font-size: 1rem !important;
    padding: 0.7rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,.15) !important;
}
.stTextInput label { color: var(--muted) !important; font-size: 0.82rem !important; }

.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-family: var(--mono) !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px !important;
    transition: opacity .2s, transform .1s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    border-radius: 4px !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1rem 0 !important; }

/* ── Toast-like status ── */
.status-bar {
    background: rgba(79,142,247,.1);
    border: 1px solid rgba(79,142,247,.25);
    border-radius: 8px;
    padding: 0.65rem 1.1rem;
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--accent);
    margin: 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔬 ResearchAgent</h1>
    <p>Multi-agent pipeline · Search → Read → Write → Critique</p>
</div>
""", unsafe_allow_html=True)

# ── Chat History Initialization ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Render Chat History ──
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(msg["content"])
        elif "state" in msg:
            state = msg["state"]
            tab1, tab2, tab3, tab4 = st.tabs(["🌐 Search Results", "📄 Scraped Content", "✍️ Generated Report", "🔍 Critique"])
            with tab1: st.markdown(state.get("search_results", "—"))
            with tab2: st.markdown(state.get("scraped_content", "—"))
            with tab3: st.markdown(state.get("report", "—"))
            with tab4:
                st.info("💡 Review the generated report's critique below:")
                st.markdown(state.get("critique", "—"))
        else:
            st.markdown(msg.get("content", ""))

# ── Step tracker helper ──
STEPS = [
    ("🌐", "Search"),
    ("📄", "Reader"),
    ("✍️", "Writer"),
    ("🔍", "Critic"),
]

def render_steps(active: int):
    """active: 0-indexed step currently running, -1 = none, 4 = all done"""
    pills = ""
    for i, (icon, label) in enumerate(STEPS):
        cls = "done" if i < active else ("active" if i == active else "")
        pills += f'<div class="step-pill {cls}"><span class="icon">{icon if i >= active else "✓"}</span>{label}</div>'
    st.markdown(f'<div class="steps-row">{pills}</div>', unsafe_allow_html=True)

# ── Chat Input & Pipeline Execution ──
if prompt := st.chat_input("Enter a research topic or follow-up question..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Format chat history for the pipeline
        chat_history = ""
        for m in st.session_state.messages[:-1]: # exclude the current prompt
            role = m["role"].capitalize()
            content = m["content"] if m["role"] == "user" else m.get("state", {}).get("report", m.get("content", ""))
            chat_history += f"{role}: {content}\n\n"

        step_placeholder = st.empty()
        progress_bar = st.progress(0)
        status_placeholder = st.empty()
        
        try:
            from pipeline import research_pipeline
            def show_status(msg):
                status_placeholder.markdown(f'<div class="status-bar">⚡ {msg}</div>', unsafe_allow_html=True)

            with step_placeholder.container():
                render_steps(0)
            show_status("Search agent is scouring the web…")
            progress_bar.progress(10)

            # Run full pipeline
            state = research_pipeline(prompt, chat_history=chat_history)

            for i in range(1, 5):
                with step_placeholder.container():
                    render_steps(i)
                progress_bar.progress(i * 25)
                time.sleep(0.35)

            status_placeholder.empty()
            progress_bar.empty()
            step_placeholder.empty()

            tab1, tab2, tab3, tab4 = st.tabs(["🌐 Search Results", "📄 Scraped Content", "✍️ Generated Report", "🔍 Critique"])
            with tab1: st.markdown(state.get("search_results", "—"))
            with tab2: st.markdown(state.get("scraped_content", "—"))
            with tab3: st.markdown(state.get("report", "—"))
            with tab4:
                st.info("💡 Review the generated report's critique below:")
                st.markdown(state.get("critique", "—"))

            # Save to memory
            st.session_state.messages.append({"role": "assistant", "state": state})

        except Exception as e:
            st.error(f"Pipeline error: {e}")
