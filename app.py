import streamlit as st
import pandas as pd

# ============================================================
# PERSON 1 — DATA LOADING
# ============================================================

def load_artist_data(filepath):
    df = pd.read_excel(filepath, sheet_name="Artists")
    artist_data = {}
    for index, row in df.iterrows():
        artist = str(row["Artist"]).strip().lower()
        artist_data[artist] = {
            "name":    str(row["Artist"]).strip(),
            "genre":   str(row["Genre"]).strip(),
            "country": str(row["Country"]).strip(),
        }
    return artist_data

# ============================================================
# PERSON 2 — SEARCH LOGIC
# ============================================================

def search_artist(name, data):
    if name is None or name.strip() == "":
        return "Error: Please enter an artist name."
    name = name.strip().lower()
    if name in data:
        return data[name]
    possible_matches = []
    for artist_key in data:
        if name in artist_key or artist_key in name:
            possible_matches.append(data[artist_key]["name"])
    if possible_matches:
        return f"Artist not found. Did you mean: {', '.join(possible_matches[:5])}?"
    return "Artist not found. Please try again."

# ============================================================
# PERSON 3 — FUNCTIONS
# ============================================================

def build_user_profile(artist_names, data):
    genre_profiles = {
        "Rock":        {"energy": 3, "extroversion": 2, "emotionality": 1},
        "Rock/Pop":    {"energy": 2, "extroversion": 3, "emotionality": 2},
        "Pop":         {"energy": 2, "extroversion": 3, "emotionality": 2},
        "Hip-Hop":     {"energy": 3, "extroversion": 3, "emotionality": 2},
        "R&B":         {"energy": 1, "extroversion": 2, "emotionality": 3},
        "Soul":        {"energy": 1, "extroversion": 2, "emotionality": 3},
        "Jazz":        {"energy": 1, "extroversion": 1, "emotionality": 3},
        "Classical":   {"energy": 1, "extroversion": 1, "emotionality": 3},
        "Electronic":  {"energy": 3, "extroversion": 3, "emotionality": 1},
        "Metal":       {"energy": 3, "extroversion": 1, "emotionality": 2},
        "Country":     {"energy": 2, "extroversion": 2, "emotionality": 3},
        "Folk":        {"energy": 1, "extroversion": 1, "emotionality": 3},
        "Latin":       {"energy": 3, "extroversion": 3, "emotionality": 2},
    }
    profile = {"energy": 0, "extroversion": 0, "emotionality": 0}
    found_count = 0
    for name in artist_names:
        result = search_artist(name, data)
        if isinstance(result, dict):
            genre = result.get("genre", "")
            found_count += 1
            if genre in genre_profiles:
                for key in profile:
                    profile[key] += genre_profiles[genre][key]
            else:
                profile["energy"] += 1
                profile["extroversion"] += 1
                profile["emotionality"] += 1
    return profile, found_count

# ============================================================
# PERSON 4 — CLASS + STREAMLIT UI
# ============================================================

class MusicPersona:
    def __init__(self, name, emoji, description, anthem, traits, color, bg):
        self.name = name
        self.emoji = emoji
        self.description = description
        self.anthem = anthem
        self.traits = traits
        self.color = color
        self.bg = bg

# ── 13 Personas — directly from Master Personas sheet ────────────────────────
PERSONA_DETAILS = {
    "the-life-of-the-party": {
        "name": "The Life of the Party", "emoji": "🎉",
        "description": "You don't just attend the function — you ARE the function. Your energy is infectious, your playlist converts skeptics, and somehow you know every word to songs you've never even heard. You live for the moments that become memories.",
        "anthem": '"As It Was" — Harry Styles',
        "traits": ["Crowd Magnetizer", "Vibes Architect", "Last One Standing"],
        "color": "#D85A30", "bg": "#FFF0EB",
    },
    "the-main-character": {
        "name": "The Main Character", "emoji": "🎬",
        "description": "Your playlist feels like a movie soundtrack and you are definitely the lead role. Every walk somewhere is a music video, every mundane moment deserves a cinematic score. Life is the stage and you've always known your cue.",
        "anthem": '"Starboy" — The Weeknd',
        "traits": ["Cinematic Thinker", "Moment Maximizer", "Effortlessly Iconic"],
        "color": "#C0392B", "bg": "#FDECEA",
    },
    "the-daydreamer": {
        "name": "The Daydreamer", "emoji": "☁️",
        "description": "You hear a song and immediately you're starring in a music video of your own life. You have dozens of unfinished playlists, a soft spot for melancholy bridges, and you feel everything three times more intensely than anyone around you.",
        "anthem": '"Liability" — Lorde',
        "traits": ["Serial Playlist Maker", "Deep Feeler", "Bridge Obsessive"],
        "color": "#7F77DD", "bg": "#F0EFFD",
    },
    "the-chill-soul": {
        "name": "The Chill Soul", "emoji": "☕",
        "description": "You are the human equivalent of a Sunday morning. Your music doesn't need to be loud to be felt — it just needs to be real. People gravitate toward your energy because it costs nothing to be around you, and your playlists feel like exhaling.",
        "anthem": '"Best Part" — Daniel Caesar ft. H.E.R.',
        "traits": ["Comfort Curator", "Slow Burn Appreciator", "Quiet Confidence"],
        "color": "#5D8A6E", "bg": "#EBF5EF",
    },
    "the-lone-wolf": {
        "name": "The Lone Wolf", "emoji": "🐺",
        "description": "Music is your private universe. You have artists no one around you has heard of, and you prefer it that way. Late nights, headphones in, existing in your own cinematic world. The best concert you've attended was solo.",
        "anthem": '"Holocene" — Bon Iver',
        "traits": ["Underdog Advocate", "Solitude Enjoyer", "Hidden Depths"],
        "color": "#5F5E5A", "bg": "#F2F2F0",
    },
    "the-romantic": {
        "name": "The Romantic", "emoji": "🌹",
        "description": "You fall in love with songs the way others fall in love with people — completely and suddenly. Every playlist you've ever made is secretly a love letter. You believe deeply in the right song at the right moment.",
        "anthem": '"Make You Feel My Love" — Adele',
        "traits": ["Emotional Archivist", "Slow Dance Defender", "Lyric Memorizer"],
        "color": "#D4537E", "bg": "#FDEEF4",
    },
    "the-old-soul": {
        "name": "The Old Soul", "emoji": "🎷",
        "description": "You were born in the wrong decade and you've fully accepted it. Vinyl over streaming. The classics are classics for a reason. You can explain in convincing detail exactly why they don't make 'em like they used to.",
        "anthem": '"What\'s Going On" — Marvin Gaye',
        "traits": ["Vinyl Evangelist", "Time Traveler", "Authenticity Guardian"],
        "color": "#BA7517", "bg": "#FDF3E3",
    },
    "the-hype-beast": {
        "name": "The Hype Beast", "emoji": "🔥",
        "description": "If it slaps, you found it first. Your speaker is always at full blast and your energy could power a small city. You live for the drop, the unexpected feature, and the freestyle that breaks the internet.",
        "anthem": '"HUMBLE." — Kendrick Lamar',
        "traits": ["First-to-Know", "Volume Maximalist", "Culture Mover"],
        "color": "#E24B4A", "bg": "#FEF0F0",
    },
    "the-overthinker": {
        "name": "The Overthinker", "emoji": "🌀",
        "description": "You've analyzed the bridge of a song you've never even shared with anyone. Music is a language you speak fluently and silently. You remember exactly where you were when you first heard That Song. You probably have a playlist for every possible situation.",
        "anthem": '"Skinny Love" — Bon Iver',
        "traits": ["Pattern Finder", "Bridge Appreciator", "Emotional Archaeologist"],
        "color": "#378ADD", "bg": "#EBF4FF",
    },
    "the-free-spirit": {
        "name": "The Free Spirit", "emoji": "🌿",
        "description": "Genre is a cage and you refuse to be contained. From Afrobeats to folk to ambient electronic — your taste is a passport with stamps from everywhere. You'll try anything once and you almost always love it.",
        "anthem": '"American Pie" — Don McLean',
        "traits": ["Genre Nomad", "Vibe Chameleon", "Perpetually Surprised"],
        "color": "#1D9E75", "bg": "#E8F8F2",
    },
    "the-nostalgist": {
        "name": "The Nostalgist", "emoji": "📼",
        "description": "A song can teleport you instantly. You have playlists named after specific years, former feelings, and childhood bedrooms. You believe the best music was made in one particular era and you can argue it convincingly.",
        "anthem": '"Mr. Brightside" — The Killers',
        "traits": ["Memory Keeper", "Era Defender", "Emotional Time Machine"],
        "color": "#534AB7", "bg": "#EEEDF9",
    },
    "the-rebel": {
        "name": "The Rebel", "emoji": "⚡",
        "description": "You play it loud and you play it proud. You push against the mainstream on principle, and your music taste doubles as an identity statement. You believe every truly great song should feel just a little bit dangerous.",
        "anthem": '"Smells Like Teen Spirit" — Nirvana',
        "traits": ["Status Quo Disruptor", "Volume at 11", "Art Purist"],
        "color": "#8B2252", "bg": "#F9EBF3",
    },
    "the-trendsetter": {
        "name": "The Trendsetter", "emoji": "✨",
        "description": "You've already moved on from what's currently popular. Your ears are six months in the future. Artists you champion now will be mainstream eventually — and you'll stop listening to them exactly when that happens.",
        "anthem": '"Angel" — PinkPantheress',
        "traits": ["Taste Pioneer", "Cultural Forecaster", "Hype Resistant"],
        "color": "#0F6E56", "bg": "#E8F5EF",
    },
}

# ── Genre → Persona ID mapping (from Genre Mapping sheet) ────────────────────
GENRE_TO_PERSONA = {
    "Pop": "the-life-of-the-party",
    "Dance": "the-life-of-the-party",
    "K-Pop": "the-life-of-the-party",
    "Afrobeats": "the-life-of-the-party",
    "Reggaeton": "the-hype-beast",
    "Hip-Hop": "the-hype-beast",
    "Trap": "the-hype-beast",
    "Drill": "the-hype-beast",
    "Grime": "the-hype-beast",
    "R&B/Pop": "the-main-character",
    "Pop/R&B": "the-main-character",
    "R&B": "the-romantic",
    "Soul/Pop": "the-romantic",
    "Lo-fi": "the-chill-soul",
    "Neo Soul": "the-chill-soul",
    "Acoustic": "the-chill-soul",
    "Jazz/Pop": "the-chill-soul",
    "Soul/R&B": "the-chill-soul",
    "Indie Pop": "the-daydreamer",
    "Dream Pop": "the-daydreamer",
    "Electropop": "the-daydreamer",
    "Folk/Indie": "the-lone-wolf",
    "Shoegaze": "the-lone-wolf",
    "Ambient": "the-lone-wolf",
    "Classic Rock": "the-old-soul",
    "Jazz": "the-old-soul",
    "Blues": "the-old-soul",
    "Soul/Jazz": "the-old-soul",
    "Electronic/Hip-Hop": "the-overthinker",
    "Progressive": "the-overthinker",
    "Psychedelic Rock": "the-overthinker",
    "Art Rock": "the-overthinker",
    "Trip-hop": "the-overthinker",
    "Post-punk": "the-rebel",
    "Punk Rock": "the-rebel",
    "Grunge": "the-rebel",
    "Metal": "the-rebel",
    "Alternative Rock": "the-rebel",
    "Pop-Punk": "the-nostalgist",
    "Emo": "the-nostalgist",
    "Britpop": "the-nostalgist",
    "World": "the-free-spirit",
    "Folk/Pop": "the-free-spirit",
    "Reggae": "the-free-spirit",
    "Latin": "the-free-spirit",
    "Hyperpop": "the-trendsetter",
    "Experimental": "the-trendsetter",
    "Electronic": "the-trendsetter",
    "UK Rap": "the-trendsetter",
}

def genre_to_persona_id(genre):
    for key, pid in GENRE_TO_PERSONA.items():
        if key.lower() in genre.lower():
            return pid
    return "the-free-spirit"

# ── Quiz questions — exactly from Quiz Questions. sheet ───────────────────────
QUIZ_QUESTIONS = [
    {
        "question": "It's Saturday night. Where are you?",
        "options": [
            ("🎊 Packed house party. I'm on the aux and I'm not giving it up.", "the-life-of-the-party", "the-hype-beast"),
            ("🎧 Headphones in, deep in a new album I just discovered.", "the-daydreamer", "the-overthinker"),
            ("🚗 Late-night drive, windows down, no particular destination.", "the-lone-wolf", "the-free-spirit"),
            ("🎬 Movie night watching something from a decade I wasn't alive for.", "the-nostalgist", "the-old-soul"),
        ]
    },
    {
        "question": "How do you actually find new music?",
        "options": [
            ("📱 TikTok and Reels. If it's going viral, I probably heard it first.", "the-trendsetter", "the-hype-beast"),
            ("🌙 Spotify rabbit holes at 2am. One song leads to another for hours.", "the-overthinker", "the-daydreamer"),
            ("🎤 Concerts, local scenes, friends who actually have taste.", "the-life-of-the-party", "the-rebel"),
            ("📻 Old records and recommendations from people born before 1970.", "the-old-soul", "the-nostalgist"),
        ]
    },
    {
        "question": "The aux cord is yours. You:",
        "options": [
            ("✅ Already have the perfect curated playlist loaded and ready.", "the-trendsetter", "the-main-character"),
            ("😩 Spend 10 minutes agonizing over the perfect opening track.", "the-overthinker", "the-daydreamer"),
            ("😤 Play what YOU want. It's your turn. Everyone will come around.", "the-rebel", "the-lone-wolf"),
            ("🤝 Ask what everyone's feeling first and build the vibe from there.", "the-chill-soul", "the-free-spirit"),
        ]
    },
    {
        "question": "Pick the feeling that hits hardest:",
        "options": [
            ("🙌 An entire crowd singing the same lyrics at the exact same time.", "the-life-of-the-party", "the-hype-beast"),
            ("💭 A song captures something you've never been able to put into words.", "the-overthinker", "the-romantic"),
            ("⏳ Discovering a 30-year-old track that sounds like it was made for right now.", "the-old-soul", "the-nostalgist"),
            ("🚀 A new artist drops something completely unlike anything before.", "the-trendsetter", "the-free-spirit"),
        ]
    },
    {
        "question": "Your friends would describe you as:",
        "options": [
            ("🎲 Unpredictable. In the best possible way.", "the-rebel", "the-trendsetter"),
            ("🌊 Deep. Sometimes too deep for a Tuesday.", "the-romantic", "the-daydreamer"),
            ("😌 Chill. Being around you just feels easy.", "the-chill-soul", "the-free-spirit"),
            ("🌟 Iconic. You just have a thing about you.", "the-main-character", "the-life-of-the-party"),
        ]
    },
    {
        "question": "Your playlist is basically:",
        "options": [
            ("🎬 A cinematic hype reel for my main character moments.", "the-main-character", "the-hype-beast"),
            ("📼 Songs I've had for years and still haven't finished with.", "the-nostalgist", "the-old-soul"),
            ("🎼 A deliberate emotional journey with a beginning, middle, and end.", "the-overthinker", "the-romantic"),
            ("🔭 Whatever's experimental and fascinating to me this week.", "the-trendsetter", "the-rebel"),
        ]
    },
    {
        "question": "How do you use music in your daily life?",
        "options": [
            ("🔊 It's always on — loud, matching my energy at every moment.", "the-hype-beast", "the-life-of-the-party"),
            ("🌿 Background texture — soft, warm, barely there but always felt.", "the-chill-soul", "the-lone-wolf"),
            ("💙 It's how I process everything — feelings, memories, ideas.", "the-romantic", "the-daydreamer"),
            ("🔍 It's research. I'm always hunting the next thing worth listening to.", "the-trendsetter", "the-overthinker"),
        ]
    },
]

def merge_and_decide(artist_scores, quiz_scores):
    """Merge artist scores (40%) and quiz scores (60%) to find winning persona."""
    all_ids = set(list(artist_scores.keys()) + list(quiz_scores.keys()))
    final = {}
    for pid in all_ids:
        final[pid] = (artist_scores.get(pid, 0) * 0.4) + (quiz_scores.get(pid, 0) * 0.6)
    return max(final, key=final.get) if final else "the-free-spirit"

def restart():
    st.session_state.step = "artists"
    st.session_state.artist_scores = {}
    st.session_state.quiz_scores = {}
    st.session_state.quiz_step = 0
    st.session_state.artist_names_found = []

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Your Life as a Playlist", page_icon="🎵", layout="centered")

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: white !important;
}

p, label, .stMarkdown { color: #e0e0e0 !important; }

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: white;
    text-align: center;
    line-height: 1.2;
    margin-bottom: 0.4rem;
}

.hero-sub {
    font-size: 1.05rem;
    color: #b0b0cc;
    text-align: center;
    margin-bottom: 2rem;
}

.step-badge {
    display: block;
    text-align: center;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 50px;
    padding: 6px 20px;
    font-size: 0.82rem;
    color: #c0c0e0;
    margin: 0 auto 1.5rem auto;
    width: fit-content;
}

.question-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 1.75rem 2rem 1rem 2rem;
    margin-bottom: 1.25rem;
}

.question-text {
    font-family: 'Playfair Display', serif;
    font-size: 1.55rem;
    color: white;
    line-height: 1.4;
}

.progress-dots {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-bottom: 1.25rem;
}

.dot { width: 9px; height: 9px; border-radius: 50%; background: rgba(255,255,255,0.18); }
.dot.active { background: white; }
.dot.done { background: rgba(255,255,255,0.55); }

.stButton > button {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 14px !important;
    color: white !important;
    font-size: 0.95rem !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.75rem 1.2rem !important;
    width: 100% !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
    margin-bottom: 0.5rem !important;
}

.stButton > button:hover {
    background: rgba(255,255,255,0.16) !important;
    border-color: rgba(255,255,255,0.38) !important;
    transform: translateX(5px) !important;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
}

.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.3) !important; }
.stTextInput > label { color: #c0c0e0 !important; font-size: 0.9rem !important; }

.result-card {
    border-radius: 24px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin: 1rem 0;
}

.result-emoji { font-size: 4.5rem; display: block; margin-bottom: 0.5rem; }

.result-name {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.result-desc {
    font-size: 1.05rem;
    line-height: 1.75;
    margin-bottom: 1.5rem;
    opacity: 0.92;
}

.anthem-box {
    background: rgba(0,0,0,0.18);
    border-radius: 12px;
    padding: 0.9rem 1.4rem;
    margin-bottom: 1.4rem;
    font-size: 0.95rem;
}

.trait-pill {
    display: inline-block;
    background: rgba(0,0,0,0.15);
    border-radius: 50px;
    padding: 5px 16px;
    margin: 4px;
    font-size: 0.82rem;
    font-weight: 500;
}

.artist-note {
    opacity: 0.55;
    font-size: 0.82rem;
    margin-top: 1.2rem;
}

.stProgress > div > div {
    background: rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #a78bfa, #f472b6) !important;
    border-radius: 10px !important;
}

footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = "artists"
if "artist_scores" not in st.session_state:
    st.session_state.artist_scores = {}
if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {}
if "quiz_step" not in st.session_state:
    st.session_state.quiz_step = 0
if "artist_names_found" not in st.session_state:
    st.session_state.artist_names_found = []

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_artist_data("database_artists.xlsx")

data = get_data()

# ═══════════════════════════════════════════════════════════════
# STEP 1 — ARTIST INPUT
# ═══════════════════════════════════════════════════════════════
if st.session_state.step == "artists":

    st.markdown('<div class="hero-title">🎵 Your Life<br>as a Playlist</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Discover your music personality in 2 steps.</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">✦ Step 1 of 2 — Your top artists</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="question-card">
        <div class="question-text">Who do you actually listen to?</div>
    </div>
    """, unsafe_allow_html=True)

    artist1 = st.text_input("Artist #1", placeholder="e.g. Taylor Swift")
    artist2 = st.text_input("Artist #2 (optional)", placeholder="e.g. Kendrick Lamar")
    artist3 = st.text_input("Artist #3 (optional)", placeholder="e.g. Adele")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Next — Take the quiz →"):
        artists = [a for a in [artist1, artist2, artist3] if a.strip()]
        if not artists:
            st.warning("Please enter at least one artist.")
        else:
            profile, found = build_user_profile(artists, data)
            artist_scores = {}
            if found > 0:
                # Map each found artist's genre to a persona and add points
                for name in artists:
                    result = search_artist(name, data)
                    if isinstance(result, dict):
                        pid = genre_to_persona_id(result.get("genre", ""))
                        artist_scores[pid] = artist_scores.get(pid, 0) + 3
            else:
                st.error("None of those artists were found. Try checking the spelling.")
                st.stop()

            st.session_state.artist_scores = artist_scores
            st.session_state.artist_names_found = [a for a in artists if isinstance(search_artist(a, data), dict)]
            st.session_state.step = "quiz"
            st.rerun()

# ═══════════════════════════════════════════════════════════════
# STEP 2 — QUIZ (7 questions from the Excel)
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == "quiz":
    q_idx = st.session_state.quiz_step
    total = len(QUIZ_QUESTIONS)

    st.markdown('<div class="hero-title">🎵 Your Life<br>as a Playlist</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="step-badge">✦ Step 2 of 2 — Question {q_idx + 1} of {total}</div>', unsafe_allow_html=True)

    # Progress dots
    dots = "".join([
        f'<div class="dot {"done" if i < q_idx else "active" if i == q_idx else ""}"></div>'
        for i in range(total)
    ])
    st.markdown(f'<div class="progress-dots">{dots}</div>', unsafe_allow_html=True)
    st.progress(q_idx / total)

    q = QUIZ_QUESTIONS[q_idx]

    st.markdown(f"""
    <div class="question-card">
        <div class="question-text">{q['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    for i, (option_text, p1, p2) in enumerate(q["options"]):
        if st.button(option_text, key=f"q{q_idx}_opt{i}"):
            st.session_state.quiz_scores[p1] = st.session_state.quiz_scores.get(p1, 0) + 2
            st.session_state.quiz_scores[p2] = st.session_state.quiz_scores.get(p2, 0) + 1
            if q_idx + 1 >= total:
                st.session_state.step = "result"
            else:
                st.session_state.quiz_step += 1
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Start over"):
        restart()
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# STEP 3 — RESULT
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == "result":

    persona_id = merge_and_decide(
        st.session_state.artist_scores,
        st.session_state.quiz_scores
    )
    p = PERSONA_DETAILS.get(persona_id, PERSONA_DETAILS["the-free-spirit"])

    traits_html = "".join([f'<span class="trait-pill">{t}</span>' for t in p["traits"]])
    artist_note = ""
    if st.session_state.artist_names_found:
        artist_note = f'<p class="artist-note">Based on your artists: {", ".join(st.session_state.artist_names_found)} — combined with your quiz answers.</p>'

    st.markdown('<div class="hero-title">🎵 Your Result</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Your music identity has been revealed.</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card" style="background: linear-gradient(135deg, {p['color']}25, {p['color']}45); border: 2px solid {p['color']}55;">
        <span class="result-emoji">{p['emoji']}</span>
        <div class="result-name" style="color: {p['color']};">{p['name']}</div>
        <div class="result-desc" style="color: white;">{p['description']}</div>
        <div class="anthem-box" style="color: {p['color']};">
            🎶 Your anthem: <strong>{p['anthem']}</strong>
        </div>
        <div>{traits_html}</div>
        {artist_note}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Take it again", use_container_width=True):
        restart()
        st.rerun()
