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

def get_persona_from_profile(profile):
    energy = profile["energy"]
    extroversion = profile["extroversion"]
    emotionality = profile["emotionality"]
    if energy >= 7 and extroversion >= 7:
        return "The Life of the Party"
    elif energy >= 7 and extroversion < 4:
        return "The Rebel"
    elif emotionality >= 7 and extroversion < 4:
        return "The Overthinker"
    elif emotionality >= 7 and extroversion >= 5:
        return "The Romantic"
    elif energy >= 5 and extroversion >= 5 and emotionality >= 5:
        return "The All-Rounder"
    elif energy < 4 and extroversion < 4:
        return "The Lone Wolf"
    elif extroversion >= 7 and emotionality >= 5:
        return "The Empath"
    elif energy >= 5 and emotionality < 4:
        return "The Hype Machine"
    else:
        return "The Free Spirit"

def format_result(persona, profile):
    energy = profile["energy"]
    emotionality = profile["emotionality"]
    descriptions = {
        "The Life of the Party": "You are the person everyone wants at their playlist. Music is not just something you listen to — it is something you perform.",
        "The Rebel":             "You do not follow trends, you ignore them. Your music taste is your identity and you wear it like armour.",
        "The Overthinker":       "You feel music in a way most people never will. Every lyric hits different at 2am.",
        "The Romantic":          "You believe music is the language of the heart. You have a song for every feeling you have ever had.",
        "The All-Rounder":       "Your playlist is a mood board of your entire personality. Genres are just suggestions to you.",
        "The Lone Wolf":         "You listen alone, feel deeply, and share rarely. Your music taste is your most private world.",
        "The Empath":            "You absorb the emotion of every song. Music is how you understand both yourself and other people.",
        "The Hype Machine":      "Good vibes only. Your playlist exists to get people moving and keep the energy high.",
        "The Free Spirit":       "You resist categories. Your music is as unpredictable and interesting as you are.",
    }
    base = descriptions.get(persona, "Your music taste is uniquely yours.")
    if energy >= 8:
        extra = " Your energy levels are off the charts."
    elif emotionality >= 8:
        extra = " You feel everything very deeply."
    elif energy <= 3:
        extra = " You appreciate the quiet and the slow burn."
    else:
        extra = " You have a balanced and open approach to music."
    return base + extra

# ============================================================
# PERSON 4 — CLASS + STREAMLIT UI
# ============================================================

class MusicPersona:
    def __init__(self, name, emoji, description, anthem, traits):
        self.name = name
        self.emoji = emoji
        self.description = description
        self.anthem = anthem
        self.traits = traits

PERSONA_DETAILS = {
    "The Life of the Party": {
        "emoji": "🎉",
        "anthem": '"As It Was" — Harry Styles',
        "traits": ["Crowd Magnetizer", "Vibes Architect", "Last One Standing"],
    },
    "The Rebel": {
        "emoji": "⚡",
        "anthem": '"Smells Like Teen Spirit" — Nirvana',
        "traits": ["Status Quo Disruptor", "Volume at 11", "Art Purist"],
    },
    "The Overthinker": {
        "emoji": "🌀",
        "anthem": '"Skinny Love" — Bon Iver',
        "traits": ["Pattern Finder", "Bridge Appreciator", "Emotional Archaeologist"],
    },
    "The Romantic": {
        "emoji": "🌹",
        "anthem": '"Make You Feel My Love" — Adele',
        "traits": ["Emotional Archivist", "Slow Dance Defender", "Lyric Memorizer"],
    },
    "The All-Rounder": {
        "emoji": "🎬",
        "anthem": '"Starboy" — The Weeknd',
        "traits": ["Cinematic Thinker", "Moment Maximizer", "Effortlessly Iconic"],
    },
    "The Lone Wolf": {
        "emoji": "🐺",
        "anthem": '"Holocene" — Bon Iver',
        "traits": ["Underdog Advocate", "Solitude Enjoyer", "Hidden Depths"],
    },
    "The Empath": {
        "emoji": "☕",
        "anthem": '"Best Part" — Daniel Caesar ft. H.E.R.',
        "traits": ["Comfort Curator", "Slow Burn Appreciator", "Quiet Confidence"],
    },
    "The Hype Machine": {
        "emoji": "🔥",
        "anthem": '"HUMBLE." — Kendrick Lamar',
        "traits": ["First-to-Know", "Volume Maximalist", "Culture Mover"],
    },
    "The Free Spirit": {
        "emoji": "🌿",
        "anthem": '"Banana Pancakes" — Jack Johnson',
        "traits": ["Genre Nomad", "Vibe Chameleon", "Perpetually Surprised"],
    },
}

QUIZ_QUESTIONS = [
    {
        "question": "It's Saturday night. Where are you?",
        "options": [
            ("Packed house party. I'm on the aux and I'm not giving it up.", "The Life of the Party", "The Hype Machine"),
            ("Headphones in, deep in a new album I just discovered.", "The Overthinker", "The Lone Wolf"),
            ("Late-night drive, windows down, no particular destination.", "The Free Spirit", "The Lone Wolf"),
            ("Movie night watching something from a decade I wasn't alive for.", "The Overthinker", "The Romantic"),
        ]
    },
    {
        "question": "How do you actually find new music?",
        "options": [
            ("TikTok and Reels. If it's going viral, I probably heard it first.", "The Hype Machine", "The Life of the Party"),
            ("Spotify rabbit holes at 2am. One song leads to another for hours.", "The Overthinker", "The Lone Wolf"),
            ("Concerts, local scenes, friends who actually have taste.", "The Life of the Party", "The Rebel"),
            ("Old records and recommendations from people born before 1970.", "The Romantic", "The Overthinker"),
        ]
    },
    {
        "question": "The aux cord is yours. You:",
        "options": [
            ("Already have the perfect curated playlist loaded and ready.", "The All-Rounder", "The Life of the Party"),
            ("Spend 10 minutes agonizing over the perfect opening track.", "The Overthinker", "The Romantic"),
            ("Play what YOU want. It's your turn. Everyone will come around.", "The Rebel", "The Lone Wolf"),
            ("Ask what everyone's feeling first and build the vibe from there.", "The Empath", "The Free Spirit"),
        ]
    },
    {
        "question": "Pick the feeling that hits hardest:",
        "options": [
            ("An entire crowd singing the same lyrics at the exact same time.", "The Life of the Party", "The Hype Machine"),
            ("A song captures something you've never been able to put into words.", "The Overthinker", "The Romantic"),
            ("Discovering a 30-year-old track that sounds like it was made for right now.", "The Romantic", "The Overthinker"),
            ("A new artist drops something completely unlike anything before.", "The Rebel", "The Free Spirit"),
        ]
    },
    {
        "question": "Your friends would describe you as:",
        "options": [
            ("Unpredictable. In the best possible way.", "The Rebel", "The Free Spirit"),
            ("Deep. Sometimes too deep for a Tuesday.", "The Romantic", "The Overthinker"),
            ("Chill. Being around you just feels easy.", "The Empath", "The Free Spirit"),
            ("The one who always has the best songs.", "The Life of the Party", "The Hype Machine"),
        ]
    },
    {
        "question": "Your playlist is basically:",
        "options": [
            ("A cinematic hype reel for my main character moments.", "The All-Rounder", "The Hype Machine"),
            ("Songs I've had for years and still haven't finished with.", "The Romantic", "The Lone Wolf"),
            ("A deliberate emotional journey with a beginning, middle, and end.", "The Overthinker", "The Romantic"),
            ("Whatever's experimental and fascinating to me this week.", "The Rebel", "The Free Spirit"),
        ]
    },
    {
        "question": "Pick the lyric energy that lives rent-free in your head:",
        "options": [
            ('"We came alive in the city lights" — loud, electric, present.', "The Life of the Party", "The Hype Machine"),
            ('"Running from something I can\'t name" — restless, searching.', "The Lone Wolf", "The Free Spirit"),
            ('"Remember when we were young and nothing could stop us" — pure ache.', "The Romantic", "The Overthinker"),
            ('"Nobody sees it quite the way that I do" — singular and precise.', "The Overthinker", "The Rebel"),
        ]
    },
]

def get_persona_from_quiz(scores):
    if not scores:
        return "The Free Spirit"
    return max(scores, key=scores.get)

def display_result(persona_name):
    details = PERSONA_DETAILS.get(persona_name, {
        "emoji": "🎵", "anthem": "Unknown", "traits": []
    })
    st.markdown("---")
    st.markdown(f"## {details['emoji']} {persona_name}")
    st.markdown(f"*{details['anthem']}*")
    cols = st.columns(3)
    for i, trait in enumerate(details["traits"]):
        cols[i].metric("", trait)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Your Life as a Playlist", page_icon="🎵", layout="centered")
st.title("🎵 Your Life as a Playlist")

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_artist_data("database_artists.xlsx")

data = get_data()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🎤 Artist Quiz", "❓ Personality Quiz"])

# ── TAB 1: ARTIST INPUT ───────────────────────────────────────────────────────
with tab1:
    st.markdown("Enter up to 3 of your favorite artists and discover your music persona.")

    artist1 = st.text_input("Favorite artist #1", placeholder="e.g. Taylor Swift")
    artist2 = st.text_input("Favorite artist #2 (optional)", placeholder="e.g. Kendrick Lamar")
    artist3 = st.text_input("Favorite artist #3 (optional)", placeholder="e.g. Adele")

    if st.button("Find my persona 🎵", key="artist_btn"):
        artists = [a for a in [artist1, artist2, artist3] if a.strip()]
        if not artists:
            st.warning("Please enter at least one artist.")
        else:
            profile, found = build_user_profile(artists, data)
            if found == 0:
                st.error("None of those artists were found. Try checking the spelling.")
            else:
                persona_name = get_persona_from_profile(profile)
                description = format_result(persona_name, profile)
                details = PERSONA_DETAILS.get(persona_name, {
                    "emoji": "🎵", "anthem": "Unknown", "traits": []
                })
                st.markdown("---")
                st.markdown(f"## {details['emoji']} {persona_name}")
                st.markdown(description)
                st.markdown(f"**Your anthem:** *{details['anthem']}*")
                st.markdown("**Your traits:** " + " · ".join(details["traits"]))

# ── TAB 2: PERSONALITY QUIZ ───────────────────────────────────────────────────
with tab2:
    st.markdown("Answer 7 questions and find out which music persona you are.")

    if "quiz_scores" not in st.session_state:
        st.session_state.quiz_scores = {}
    if "quiz_step" not in st.session_state:
        st.session_state.quiz_step = 0
    if "quiz_done" not in st.session_state:
        st.session_state.quiz_done = False

    if st.button("Start over 🔄", key="reset_btn"):
        st.session_state.quiz_scores = {}
        st.session_state.quiz_step = 0
        st.session_state.quiz_done = False

    if st.session_state.quiz_done:
        persona_name = get_persona_from_quiz(st.session_state.quiz_scores)
        details = PERSONA_DETAILS.get(persona_name, {
            "emoji": "🎵", "anthem": "Unknown", "traits": []
        })
        description = format_result(persona_name, {"energy": 5, "extroversion": 5, "emotionality": 5})
        st.markdown("---")
        st.markdown(f"## {details['emoji']} {persona_name}")
        st.markdown(description)
        st.markdown(f"**Your anthem:** *{details['anthem']}*")
        st.markdown("**Your traits:** " + " · ".join(details["traits"]))

    elif st.session_state.quiz_step < len(QUIZ_QUESTIONS):
        q_idx = st.session_state.quiz_step
        q = QUIZ_QUESTIONS[q_idx]

        st.markdown(f"**Question {q_idx + 1} of {len(QUIZ_QUESTIONS)}**")
        st.progress((q_idx) / len(QUIZ_QUESTIONS))
        st.markdown(f"### {q['question']}")

        for i, (option_text, p1, p2) in enumerate(q["options"]):
            if st.button(option_text, key=f"q{q_idx}_opt{i}"):
                st.session_state.quiz_scores[p1] = st.session_state.quiz_scores.get(p1, 0) + 2
                st.session_state.quiz_scores[p2] = st.session_state.quiz_scores.get(p2, 0) + 1
                if q_idx + 1 >= len(QUIZ_QUESTIONS):
                    st.session_state.quiz_done = True
                else:
                    st.session_state.quiz_step += 1
                st.rerun()
