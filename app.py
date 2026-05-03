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

def get_persona(profile):
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

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Your Life as a Playlist", page_icon="🎵", layout="centered")

st.title("🎵 Your Life as a Playlist")
st.markdown("Enter up to 3 of your favorite artists and discover your music persona.")

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_artist_data("database_artists.xlsx")

data = get_data()

# ── Inputs ────────────────────────────────────────────────────────────────────
artist1 = st.text_input("Favorite artist #1", placeholder="e.g. Taylor Swift")
artist2 = st.text_input("Favorite artist #2 (optional)", placeholder="e.g. Kendrick Lamar")
artist3 = st.text_input("Favorite artist #3 (optional)", placeholder="e.g. Adele")

# ── On button click ───────────────────────────────────────────────────────────
if st.button("Find my persona 🎵"):
    artists = [a for a in [artist1, artist2, artist3] if a.strip()]

    if not artists:
        st.warning("Please enter at least one artist.")
    else:
        profile, found = build_user_profile(artists, data)

        if found == 0:
            st.error("None of those artists were found. Try checking the spelling.")
        else:
            persona_name = get_persona(profile)
            description = format_result(persona_name, profile)
            details = PERSONA_DETAILS.get(persona_name, {
                "emoji": "🎵", "anthem": "Unknown", "traits": []
            })

            persona = MusicPersona(
                name=persona_name,
                emoji=details["emoji"],
                description=description,
                anthem=details["anthem"],
                traits=details["traits"]
            )

            st.markdown("---")
            st.markdown(f"## {persona.emoji} {persona.name}")
            st.markdown(persona.description)
            st.markdown(f"**Your anthem:** *{persona.anthem}*")
            st.markdown("**Your traits:** " + " · ".join(persona.traits))
