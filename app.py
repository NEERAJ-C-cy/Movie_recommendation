import html
 
import requests
import streamlit as st
 
# =============================
# CONFIG
# =============================
API_BASE = "https://movie-recommendation-1-aey1.onrender.com" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"
 
st.set_page_config(
    page_title="CineMatch • Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
# =============================
# STYLES (dark cinematic theme)
# =============================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
 
:root {
    --bg: #0b0d14;
    --bg-soft: #131622;
    --card: #181c2b;
    --border: rgba(255,255,255,0.08);
    --text: #e8eaf2;
    --muted: #9aa0b4;
    --accent: #ff4d6d;
    --accent-2: #7c5cff;
}
 
html, body, [class*="css"], .stApp { font-family: 'Poppins', sans-serif; }
 
.stApp {
    background:
        radial-gradient(1200px 600px at 10% -10%, rgba(124,92,255,0.18), transparent 60%),
        radial-gradient(1000px 500px at 100% 0%, rgba(255,77,109,0.14), transparent 55%),
        var(--bg);
    color: var(--text);
}
 
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1400px; }
 
h1, h2, h3, h4, h5, p, label, span, div { color: var(--text); }
hr { border-color: var(--border) !important; }
 
/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10131f 0%, #0b0d14 100%);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text); }
 
/* ---------- Hero ---------- */
.hero {
    padding: 34px 38px;
    border-radius: 24px;
    background: linear-gradient(120deg, rgba(124,92,255,0.25), rgba(255,77,109,0.18)), var(--bg-soft);
    border: 1px solid var(--border);
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: "🎬";
    position: absolute; right: 30px; top: 6px;
    font-size: 110px; opacity: 0.10; transform: rotate(-12deg);
}
.hero h1 {
    margin: 0; font-size: 2.5rem; font-weight: 800; letter-spacing: -0.5px;
    background: linear-gradient(90deg, #fff, #ffb3c1 60%, #c4b5ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { margin: 8px 0 0 0; color: var(--muted); font-size: 1rem; }
 
/* ---------- Section headings ---------- */
.section-title {
    display: flex; align-items: center; gap: 12px;
    font-size: 1.35rem; font-weight: 700; margin: 1.4rem 0 0.2rem 0;
}
.section-title::before {
    content: ""; width: 5px; height: 26px; border-radius: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
}
.small-muted { color: var(--muted); font-size: 0.92rem; }
 
/* ---------- Inputs ---------- */
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
    background: var(--bg-soft) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    transition: all .2s ease;
}
div[data-baseweb="input"] > div:focus-within, div[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(255,77,109,0.18) !important;
}
input { color: var(--text) !important; font-size: 1rem !important; }
.stTextInput label p, .stSelectbox label p, .stSlider label p { color: var(--muted) !important; font-weight: 500; }
 
/* ---------- Buttons ---------- */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: var(--card);
    color: var(--text);
    font-weight: 600;
    padding: 0.45rem 0.8rem;
    transition: all .2s ease;
}
.stButton > button:hover {
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    border-color: transparent;
    color: #fff;
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(255,77,109,0.35);
}
.stButton > button:active { transform: translateY(0); }
 
/* ---------- Poster cards ---------- */
[data-testid="stImage"] img {
    border-radius: 16px;
    border: 1px solid var(--border);
    box-shadow: 0 8px 24px rgba(0,0,0,0.45);
    transition: transform .3s ease, box-shadow .3s ease, filter .3s ease;
}
[data-testid="stImage"] img:hover {
    transform: scale(1.04) translateY(-4px);
    box-shadow: 0 18px 40px rgba(255,77,109,0.30);
    filter: brightness(1.08);
}
.no-poster {
    height: 260px; display: flex; align-items: center; justify-content: center;
    border-radius: 16px; background: var(--card); border: 1px dashed var(--border);
    color: var(--muted); font-size: 0.9rem;
}
.movie-title {
    font-size: 0.9rem; font-weight: 600; line-height: 1.15rem; height: 2.3rem;
    overflow: hidden; margin: 4px 0 6px 0; color: var(--text);
}
 
/* ---------- Details page ---------- */
.detail-hero {
    border-radius: 24px; padding: 40px; min-height: 220px;
    border: 1px solid var(--border);
    background-size: cover; background-position: center;
    box-shadow: 0 24px 60px rgba(0,0,0,0.5);
    margin-bottom: 1.5rem;
}
.card {
    border: 1px solid var(--border); border-radius: 20px; padding: 22px;
    background: rgba(24,28,43,0.85); backdrop-filter: blur(8px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}
.movie-heading { font-size: 2.1rem; font-weight: 800; margin: 0 0 6px 0; line-height: 1.2; }
.chip {
    display: inline-block; padding: 5px 14px; margin: 4px 6px 4px 0; border-radius: 999px;
    font-size: 0.8rem; font-weight: 600; color: #fff;
    background: linear-gradient(90deg, rgba(255,77,109,0.85), rgba(124,92,255,0.85));
}
.meta-pill {
    display: inline-block; padding: 5px 14px; margin: 4px 6px 4px 0; border-radius: 999px;
    font-size: 0.8rem; font-weight: 500; color: var(--text);
    background: rgba(255,255,255,0.07); border: 1px solid var(--border);
}
.overview-title { font-size: 1.1rem; font-weight: 700; margin: 16px 0 6px 0; }
.overview-text { color: #c9cde0; line-height: 1.75; font-size: 0.98rem; }
 
/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 1px solid var(--border); }
.stTabs [data-baseweb="tab"] {
    background: var(--bg-soft); border-radius: 12px 12px 0 0; padding: 10px 20px;
    color: var(--muted); font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, rgba(255,77,109,0.25), rgba(124,92,255,0.25));
    color: #fff;
}
 
/* ---------- Alerts ---------- */
div[data-testid="stAlert"] { border-radius: 14px; border: 1px solid var(--border); }
 
/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-thumb { background: #2a2f45; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
</style>
""",
    unsafe_allow_html=True,
)
 
# =============================
# STATE + ROUTING (single-file pages)
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"  # home | details
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None
 
qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass
 
 
def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()
 
 
def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()
 
 
# =============================
# UI HELPERS
# =============================
def section_title(text: str, subtitle: str | None = None):
    st.markdown(f"<div class='section-title'>{text}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='small-muted'>{subtitle}</div>", unsafe_allow_html=True)
        st.write("")
 
 
# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)  # short cache for autocomplete
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"
 
 
def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return
 
    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols, gap="medium")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1
 
            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")
 
            with colset[c]:
                if poster:
                    st.image(poster, use_container_width=True)
                else:
                    st.markdown(
                        "<div class='no-poster'>🖼️ No poster</div>",
                        unsafe_allow_html=True,
                    )
 
                st.markdown(
                    f"<div class='movie-title' title='{html.escape(title, quote=True)}'>{html.escape(title)}</div>",
                    unsafe_allow_html=True,
                )
 
                if st.button(
                    "▶ Open",
                    key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}",
                    use_container_width=True,
                ):
                    if tmdb_id:
                        goto_details(tmdb_id)
 
        st.write("")
 
 
def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards
 
 
# =============================
# IMPORTANT: Robust TMDB search parsing
# Supports BOTH API shapes:
# 1) raw TMDB: {"results":[{id,title,poster_path,...}]}
# 2) list cards: [{tmdb_id,title,poster_url,...}]
# =============================
def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Returns:
      suggestions: list[(label, tmdb_id)]
      cards: list[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()
 
    # A) If API returns dict with 'results'
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )
 
    # B) If API returns already as list
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            # might be {tmdb_id,title,poster_url}
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []
 
    # Word-match filtering (contains)
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
 
    # If nothing matched, fallback to raw list (so never blank)
    final_list = matched if matched else raw_items
 
    # Suggestions = top 10 labels
    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))
 
    # Cards = top N
    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards
 
 
# =============================
# SIDEBAR
# =============================
CATEGORY_LABELS = {
    "trending": "🔥 Trending",
    "popular": "⭐ Popular",
    "top_rated": "🏆 Top Rated",
    "now_playing": "🎞️ Now Playing",
    "upcoming": "🗓️ Upcoming",
}
 
with st.sidebar:
    st.markdown("## 🎬 CineMatch")
    st.markdown(
        "<div class='small-muted'>Discover your next favourite movie</div>",
        unsafe_allow_html=True,
    )
    st.write("")
    if st.button("🏠  Home", use_container_width=True):
        goto_home()
 
    st.markdown("---")
    st.markdown("### 🎛️ Home Feed")
    home_category = st.selectbox(
        "Category",
        list(CATEGORY_LABELS.keys()),
        index=0,
        format_func=lambda k: CATEGORY_LABELS[k],
    )
    grid_cols = st.slider("Grid columns", 4, 8, 6)
 
    st.markdown("---")
    st.markdown(
        "<div class='small-muted'>Powered by TMDB • TF-IDF & Genre-based recommendations</div>",
        unsafe_allow_html=True,
    )
 
# =============================
# HEADER
# =============================
st.markdown(
    """
<div class='hero'>
    <h1>Movie Recommender</h1>
    <p>Search a title → pick a suggestion → explore details & smart recommendations.</p>
</div>
""",
    unsafe_allow_html=True,
)
 
# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    typed = st.text_input(
        "🔍 Search by movie title (keyword)",
        placeholder="Type: avenger, batman, love...",
    )
 
    # SEARCH MODE (Autocomplete + word-match results)
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters for suggestions.")
        else:
            with st.spinner("Searching movies..."):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})
 
            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )
 
                # Dropdown
                if suggestions:
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("✨ Suggestions", labels, index=0)
 
                    if selected != "-- Select a movie --":
                        # map label -> id
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword.")
 
                section_title("Results", f"Showing matches for “{html.escape(typed.strip())}”")
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")
 
        st.stop()
 
    # HOME FEED MODE
    section_title(
        CATEGORY_LABELS[home_category],
        "Hand-picked from TMDB — click a poster's button to see details",
    )
 
    with st.spinner("Loading movies..."):
        home_cards, err = api_get_json(
            "/home", params={"category": home_category, "limit": 24}
        )
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()
 
    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")
 
# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()
 
    # Top bar
    a, b = st.columns([4, 1])
    with a:
        section_title("📄 Movie Details")
    with b:
        st.write("")
        if st.button("← Back to Home", use_container_width=True):
            goto_home()
 
    # Details (your FastAPI safe route)
    with st.spinner("Loading details..."):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()
 
    # Backdrop as hero banner
    if data.get("backdrop_url"):
        backdrop = html.escape(data["backdrop_url"], quote=True)
        st.markdown(
            f"""
<div class='detail-hero' style="background-image:
    linear-gradient(90deg, rgba(11,13,20,0.92) 10%, rgba(11,13,20,0.35) 100%),
    url('{backdrop}');">
    <div class='movie-heading'>{html.escape(data.get('title',''))}</div>
</div>
""",
            unsafe_allow_html=True,
        )
 
    # Layout: Poster LEFT, Details RIGHT
    left, right = st.columns([1, 2.4], gap="large")
 
    with left:
        if data.get("poster_url"):
            st.image(data["poster_url"], use_container_width=True)
        else:
            st.markdown("<div class='no-poster'>🖼️ No poster</div>", unsafe_allow_html=True)
 
    with right:
        release = data.get("release_date") or "-"
        genre_names = [g["name"] for g in data.get("genres", [])]
        chips = "".join(f"<span class='chip'>{html.escape(g)}</span>" for g in genre_names)
        chips = chips or "<span class='meta-pill'>-</span>"
        overview = html.escape(data.get("overview") or "No overview available.")
 
        st.markdown(
            f"""
<div class='card'>
    <div class='movie-heading'>{html.escape(data.get('title',''))}</div>
    <span class='meta-pill'>📅 Release: {html.escape(str(release))}</span>
    <div style='margin-top:8px'>{chips}</div>
    <div class='overview-title'>Overview</div>
    <div class='overview-text'>{overview}</div>
</div>
""",
            unsafe_allow_html=True,
        )
 
    st.divider()
    section_title("✅ Recommendations", "Movies you might enjoy next")
 
    # Recommendations (TF-IDF + Genre) via your bundle endpoint
    title = (data.get("title") or "").strip()
    if title:
        with st.spinner("Finding similar movies..."):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
            )
 
        if not err2 and bundle:
            tab1, tab2 = st.tabs(["🔎 Similar Movies (TF-IDF)", "🎭 More Like This (Genre)"])
 
            with tab1:
                st.write("")
                poster_grid(
                    to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                    cols=grid_cols,
                    key_prefix="details_tfidf",
                )
 
            with tab2:
                st.write("")
                poster_grid(
                    bundle.get("genre_recommendations", []),
                    cols=grid_cols,
                    key_prefix="details_genre",
                )
        else:
            st.info("Showing Genre recommendations (fallback).")
            with st.spinner("Loading genre recommendations..."):
                genre_only, err3 = api_get_json(
                    "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
                )
            if not err3 and genre_only:
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")
 