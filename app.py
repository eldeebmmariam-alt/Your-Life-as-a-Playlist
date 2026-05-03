import streamlit as st
import pandas as pd
import time

# ============================================================
# TOPIC 1 — DATA STRUCTURES & EXPRESSIONS
# Covers: dictionaries, lists, string expressions
# ============================================================

# Dictionary: maps artist names to their info (loaded from Excel)
# List: stores quiz questions and answer options
# Expressions: used throughout for string formatting and conditions

PERSONA_DETAILS = {
    "the-life-of-the-party": {
        "name": "The Life of the Party",
        "emoji": "🎉",
        "description": "You don't just attend the function — you ARE the function. Your energy is infectious, your playlist converts skeptics, and somehow you know every word to songs you've never even heard. You live for the moments that become memories.",
        "anthem": '"As It Was" — Harry Styles',
        "traits": ["Crowd Magnetizer", "Vibes Architect", "Last One Standing"],
        "color": "#D85A30",
        "artists": ["Harry Styles", "Dua Lipa", "Doja Cat", "Burna Boy"],
        "dna": {"energy": 90, "extroversion": 95, "emotionality": 55},
    },
    "the-main-character": {
        "name": "The Main Character",
        "emoji": "🎬",
        "description": "Your playlist feels like a movie soundtrack and you are definitely the lead role. Every walk somewhere is a music video, every mundane moment deserves a cinematic score. Life is the stage and you've always known your cue.",
        "anthem": '"Starboy" — The Weeknd',
        "traits": ["Cinematic Thinker", "Moment Maximizer", "Effortlessly Iconic"],
        "color": "#C0392B",
        "artists": ["The Weeknd", "Beyoncé", "Drake", "Kendrick Lamar"],
        "dna": {"energy": 80, "extroversion": 85, "emotionality": 70},
    },
    "the-daydreamer": {
        "name": "The Daydreamer",
        "emoji": "☁️",
        "description": "You hear a song and immediately you're starring in a music video of your own life. You have dozens of unfinished playlists, a soft spot for melancholy bridges, and you feel everything three times more intensely than anyone around you.",
        "anthem": '"Liability" — Lorde',
        "traits": ["Serial Playlist Maker", "Deep Feeler", "Bridge Obsessive"],
        "color": "#7F77DD",
        "artists": ["Lorde", "Frank Ocean", "Lana Del Rey", "SZA"],
        "dna": {"energy": 45, "extroversion": 40, "emotionality": 92},
    },
    "the-chill-soul": {
        "name": "The Chill Soul",
        "emoji": "☕",
        "description": "You are the human equivalent of a Sunday morning. Your music doesn't need to be loud to be felt — it just needs to be real. People gravitate toward your energy because it costs nothing to be around you, and your playlists feel like exhaling.",
        "anthem": '"Best Part" — Daniel Caesar ft. H.E.R.',
        "traits": ["Comfort Curator", "Slow Burn Appreciator", "Quiet Confidence"],
        "color": "#5D8A6E",
        "artists": ["Daniel Caesar", "Mac Miller", "H.E.R.", "Jorja Smith"],
        "dna": {"energy": 35, "extroversion": 55, "emotionality": 78},
    },
    "the-lone-wolf": {
        "name": "The Lone Wolf",
        "emoji": "🐺",
        "description": "Music is your private universe. You have artists no one around you has heard of, and you prefer it that way. Late nights, headphones in, existing in your own cinematic world. The best concert you've attended was solo.",
        "anthem": '"Holocene" — Bon Iver',
        "traits": ["Underdog Advocate", "Solitude Enjoyer", "Hidden Depths"],
        "color": "#5F5E5A",
        "artists": ["Bon Iver", "Phoebe Bridgers", "Angel Olsen", "Grouper"],
        "dna": {"energy": 30, "extroversion": 20, "emotionality": 85},
    },
    "the-romantic": {
        "name": "The Romantic",
        "emoji": "🌹",
        "description": "You fall in love with songs the way others fall in love with people — completely and suddenly. Every playlist you've ever made is secretly a love letter. You believe deeply in the right song at the right moment.",
        "anthem": '"Make You Feel My Love" — Adele',
        "traits": ["Emotional Archivist", "Slow Dance Defender", "Lyric Memorizer"],
        "color": "#D4537E",
        "artists": ["Adele", "John Legend", "Giveon", "Sade"],
        "dna": {"energy": 40, "extroversion": 60, "emotionality": 97},
    },
    "the-old-soul": {
        "name": "The Old Soul",
        "emoji": "🎷",
        "description": "You were born in the wrong decade and you've fully accepted it. Vinyl over streaming. The classics are classics for a reason. You can explain in convincing detail exactly why they don't make 'em like they used to.",
        "anthem": '"What\'s Going On" — Marvin Gaye',
        "traits": ["Vinyl Evangelist", "Time Traveler", "Authenticity Guardian"],
        "color": "#BA7517",
        "artists": ["Marvin Gaye", "Aretha Franklin", "Stevie Wonder", "Bob Dylan"],
        "dna": {"energy": 50, "extroversion": 45, "emotionality": 80},
    },
    "the-hype-beast": {
        "name": "The Hype Beast",
        "emoji": "🔥",
        "description": "If it slaps, you found it first. Your speaker is always at full blast and your energy could power a small city. You live for the drop, the unexpected feature, and the freestyle that breaks the internet.",
        "anthem": '"HUMBLE." — Kendrick Lamar',
        "traits": ["First-to-Know", "Volume Maximalist", "Culture Mover"],
        "color": "#E24B4A",
        "artists": ["Kendrick Lamar", "Travis Scott", "Bad Bunny", "Central Cee"],
        "dna": {"energy": 97, "extroversion": 88, "emotionality": 50},
    },
    "the-overthinker": {
        "name": "The Overthinker",
        "emoji": "🌀",
        "description": "You've analyzed the bridge of a song you've never even shared with anyone. Music is a language you speak fluently and silently. You remember exactly where you were when you first heard That Song.",
        "anthem": '"Skinny Love" — Bon Iver',
        "traits": ["Pattern Finder", "Bridge Appreciator", "Emotional Archaeologist"],
        "color": "#378ADD",
        "artists": ["Tame Impala", "Radiohead", "Daft Punk", "Laufey"],
        "dna": {"energy": 55, "extroversion": 38, "emotionality": 88},
    },
    "the-free-spirit": {
        "name": "The Free Spirit",
        "emoji": "🌿",
        "description": "Genre is a cage and you refuse to be contained. From Afrobeats to folk to ambient electronic — your taste is a passport with stamps from everywhere. You'll try anything once and you almost always love it.",
        "anthem": '"American Pie" — Don McLean',
        "traits": ["Genre Nomad", "Vibe Chameleon", "Perpetually Surprised"],
        "color": "#1D9E75",
        "artists": ["Khruangbin", "Bombay Bicycle Club", "Vulfpeck", "Caetano Veloso"],
        "dna": {"energy": 65, "extroversion": 70, "emotionality": 65},
    },
    "the-nostalgist": {
        "name": "The Nostalgist",
        "emoji": "📼",
        "description": "A song can teleport you instantly. You have playlists named after specific years, former feelings, and childhood bedrooms. You believe the best music was made in one particular era and you can argue it convincingly.",
        "anthem": '"Mr. Brightside" — The Killers',
        "traits": ["Memory Keeper", "Era Defender", "Emotional Time Machine"],
        "color": "#534AB7",
        "artists": ["The Killers", "My Chemical Romance", "Arctic Monkeys", "Paramore"],
        "dna": {"energy": 68, "extroversion": 60, "emotionality": 85},
    },
    "the-rebel": {
        "name": "The Rebel",
        "emoji": "⚡",
        "description": "You play it loud and you play it proud. You push against the mainstream on principle, and your music taste doubles as an identity statement. You believe every truly great song should feel just a little bit dangerous.",
        "anthem": '"Smells Like Teen Spirit" — Nirvana',
        "traits": ["Status Quo Disruptor", "Volume at 11", "Art Purist"],
        "color": "#8B2252",
        "artists": ["Nirvana", "Tyler, The Creator", "Arctic Monkeys", "Bikini Kill"],
        "dna": {"energy": 88, "extroversion": 65, "emotionality": 60},
    },
    "the-trendsetter": {
        "name": "The Trendsetter",
        "emoji": "✨",
        "description": "You've already moved on from what's currently popular. Your ears are six months in the future. Artists you champion now will be mainstream eventually — and you'll stop listening to them exactly when that happens.",
        "anthem": '"Angel" — PinkPantheress',
        "traits": ["Taste Pioneer", "Cultural Forecaster", "Hype Resistant"],
        "color": "#0F6E56",
        "artists": ["PinkPantheress", "Charli XCX", "JPEGMAFIA", "Little Simz"],
        "dna": {"energy": 75, "extroversion": 70, "emotionality": 60},
    },
}

# Dictionary: maps genre keywords to persona IDs
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

# List of dictionaries: each quiz question with its answer options
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
    {
        "question": "Someone plays a song you've never heard. You:",
        "options": [
            ("🎤 Immediately Shazam it and add it to three playlists.", "the-life-of-the-party", "the-trendsetter"),
            ("🧠 Listen in silence, analyzing every layer before saying a word.", "the-overthinker", "the-lone-wolf"),
            ("😢 Feel something in your chest before the first chorus even lands.", "the-romantic", "the-daydreamer"),
            ("🤷 Wait for the drop. If there's no drop, you're not interested.", "the-hype-beast", "the-rebel"),
        ]
    },
    {
        "question": "What does music actually do for you?",
        "options": [
            ("⚡ It charges me up. I need it to function at full capacity.", "the-hype-beast", "the-life-of-the-party"),
            ("🛡️ It's armor. It protects me from the noise of everything else.", "the-lone-wolf", "the-rebel"),
            ("🕰️ It time-travels me. A song can take me back to a specific Tuesday in 2015.", "the-nostalgist", "the-romantic"),
            ("🧭 It's a compass. It helps me figure out how I actually feel.", "the-overthinker", "the-chill-soul"),
        ]
    },
    {
        "question": "Pick your concert experience:",
        "options": [
            ("🏟️ Front row, screaming every word, sweaty and fully alive.", "the-life-of-the-party", "the-hype-beast"),
            ("🎭 Small venue, dim lights, artist who makes you feel seen.", "the-romantic", "the-daydreamer"),
            ("🎪 A festival lineup I built myself — 4 stages, no compromises.", "the-free-spirit", "the-trendsetter"),
            ("🎧 Honestly? I prefer the album alone. The live version always disappoints.", "the-lone-wolf", "the-overthinker"),
        ]
    },
]

# ============================================================
# TOPIC 1 — DATA STRUCTURES (continued)
# Genre profiles stored as nested dictionaries
# ============================================================
GENRE_PROFILES = {
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

# ============================================================
# TOPIC 1 — PERSON 1: DATA LOADING
# Uses: pandas DataFrame, dictionary, for loop (Topic 2)
# ============================================================
def load_artist_data(filepath):
    df = pd.read_excel(filepath, sheet_name="Artists")
    artist_data = {}                          # empty dictionary
    for _, row in df.iterrows():              # for loop over rows
        artist = str(row["Artist"]).strip().lower()
        artist_data[artist] = {               # store as dict entry
            "name":    str(row["Artist"]).strip(),
            "genre":   str(row["Genre"]).strip(),
            "country": str(row["Country"]).strip(),
        }
    return artist_data

# ============================================================
# TOPIC 2 — FLOW CONTROL
# PERSON 2: SEARCH LOGIC
# Uses: if / elif / else, for loop, while-style retry logic
# ============================================================
def search_artist(name, data):
    # if/else: check for empty input first
    if name is None or name.strip() == "":
        return "Error: Please enter an artist name."

    name = name.strip().lower()

    # if: direct match check
    if name in data:
        return data[name]

    # for loop: search for partial matches
    possible_matches = []
    for artist_key in data:
        if name in artist_key or artist_key in name:
            possible_matches.append(data[artist_key]["name"])

    # if/else: return suggestion or failure message
    if possible_matches:
        return f"Artist not found. Did you mean: {', '.join(possible_matches[:5])}?"
    else:
        return "Artist not found. Please try again."


# ============================================================
# TOPIC 3 — FUNCTIONS
# PERSON 3: CORE QUIZ LOGIC
# Each function has a clear input → process → return structure
# ============================================================

def load_data(filepath):
    """Function 1: Load and return the artist database."""
    return load_artist_data(filepath)


def get_artist_info_safe(artist_name, data):
    """Function 2: Return artist info dict or an error string."""
    result = search_artist(artist_name, data)
    if isinstance(result, dict):
        return result
    else:
        return {"error": result}


def build_user_profile(artist_names, data):
    """
    Function 3: Build a personality profile from a list of artist names.
    Returns a profile dict with energy, extroversion, emotionality scores.
    """
    profile = {"energy": 0, "extroversion": 0, "emotionality": 0}
    found_count = 0

    for name in artist_names:                     # for loop over artists
        result = search_artist(name, data)
        if isinstance(result, dict):              # if artist was found
            genre = result.get("genre", "")
            found_count += 1
            if genre in GENRE_PROFILES:           # if genre is known
                for key in profile:               # nested for loop
                    profile[key] += GENRE_PROFILES[genre][key]
            else:
                profile["energy"] += 1
                profile["extroversion"] += 1
                profile["emotionality"] += 1

    return profile, found_count


def genre_to_persona_id(genre):
    """Function 4: Map a genre string to a persona ID using keyword matching."""
    for key, pid in GENRE_TO_PERSONA.items():    # for loop over genre map
        if key.lower() in genre.lower():          # if keyword found in genre
            return pid
    return "the-free-spirit"                      # default fallback


def merge_and_decide(artist_scores, quiz_scores):
    """
    Function 5: Combine artist scores (40%) and quiz scores (60%).
    Returns the persona ID with the highest combined score.
    """
    all_ids = set(list(artist_scores.keys()) + list(quiz_scores.keys()))
    final = {}

    for pid in all_ids:                           # for loop over all persona IDs
        a = artist_scores.get(pid, 0)
        q = quiz_scores.get(pid, 0)
        final[pid] = (a * 0.4) + (q * 0.6)      # weighted expression

    if final:
        return max(final, key=final.get)          # return highest scoring persona
    else:
        return "the-free-spirit"


def format_result(persona_id):
    """Function 6: Look up full persona details and return a formatted string."""
    p = PERSONA_DETAILS.get(persona_id, PERSONA_DETAILS["the-free-spirit"])
    return f"{p['emoji']} {p['name']}: {p['description']}"


# ============================================================
# TOPIC 4 — CLASSES
# PERSON 4: MusicPersona CLASS
# Wraps all result data into one object with attributes
# ============================================================
class MusicPersona:
    """
    Represents a user's music personality result.
    Attributes store all the data needed to display the result.
    """
    def __init__(self, persona_id, artist_names_found):
        # Look up the persona details from the data dictionary
        p = PERSONA_DETAILS.get(persona_id, PERSONA_DETAILS["the-free-spirit"])

        # Assign all attributes
        self.persona_id      = persona_id
        self.name            = p["name"]
        self.emoji           = p["emoji"]
        self.description     = p["description"]
        self.anthem          = p["anthem"]
        self.traits          = p["traits"]          # list
        self.color           = p["color"]
        self.artists         = p["artists"]         # list
        self.dna             = p["dna"]             # dict
        self.artist_sources  = artist_names_found   # list of what user typed

    def get_traits_string(self):
        """Method: returns traits joined as a readable string."""
        return " · ".join(self.traits)

    def get_share_text(self):
        """Method: returns a copyable text summary for sharing."""
        return (
            f"🎵 My music persona is {self.name} {self.emoji}\n\n"
            f"{self.description}\n\n"
            f"🎶 My anthem: {self.anthem}\n\n"
            f"My traits: {self.get_traits_string()}\n\n"
            f"Find yours at yourlifeasaplaylist.streamlit.app"
        )

    def __repr__(self):
        return f"MusicPersona(name={self.name!r}, persona_id={self.persona_id!r})"


# ============================================================
# ANIMATIONS — background effects per persona (all 13)
# ============================================================
PERSONA_ANIMATIONS = {
    "the-life-of-the-party": {"items": ["🎉","✨","🎊","✨","🎉","🥳","🎊","✨","🎉"], "anim": "partyFall", "dir": "top", "css": "@keyframes partyFall{0%{transform:translateY(0) rotate(0deg);opacity:0}10%{opacity:0.35}90%{opacity:0.2}100%{transform:translateY(110vh) rotate(360deg);opacity:0}}"},
    "the-main-character":    {"items": ["⭐","✨","🌟","✨","⭐","🌟","✨","⭐","🌟"], "anim": "mainTwinkle", "dir": "fixed", "css": "@keyframes mainTwinkle{0%,100%{transform:scale(0.7);opacity:0.05}50%{transform:scale(1.3);opacity:0.3}}"},
    "the-daydreamer":        {"items": ["☁️","✨","☁️","🌙","☁️","✨","☁️","🌙","☁️"], "anim": "dreamDrift", "dir": "left", "css": "@keyframes dreamDrift{0%{transform:translateX(0);opacity:0}8%{opacity:0.25}90%{opacity:0.15}100%{transform:translateX(125vw);opacity:0}}"},
    "the-chill-soul":        {"items": ["🍃","☕","✨","🍃","🌿","✨","☕","🍃","✨"], "anim": "chillFloat", "dir": "bottom", "css": "@keyframes chillFloat{0%{transform:translateY(0);opacity:0}12%{opacity:0.5}85%{opacity:0.25}100%{transform:translateY(-115vh);opacity:0}}"},
    "the-lone-wolf":         {"items": ["🌙","⭐","🌑","✨","🌙","⭐","🌑","✨","🌙"], "anim": "wolfPulse", "dir": "fixed", "css": "@keyframes wolfPulse{0%,100%{transform:scale(0.8);opacity:0.04}50%{transform:scale(1.2);opacity:0.22}}"},
    "the-romantic":          {"items": ["💖","🦋","💕","✨","💗","🦋","💖","💕","✨"], "anim": "romanticRise", "dir": "bottom", "css": "@keyframes romanticRise{0%{transform:translateY(0);opacity:0}15%{opacity:0.35}100%{transform:translateY(-115vh);opacity:0}}"},
    "the-old-soul":          {"items": ["🎷","📻","🎶","✨","🎷","📻","🎶","✨","🎷"], "anim": "oldSoulSway", "dir": "fixed", "css": "@keyframes oldSoulSway{0%,100%{transform:rotate(-8deg) scale(0.85);opacity:0.05}50%{transform:rotate(8deg) scale(1.1);opacity:0.22}}"},
    "the-hype-beast":        {"items": ["🔥","⚡","💥","🔥","⚡","💥","🔥","⚡","💥"], "anim": "hypeFall", "dir": "top", "css": "@keyframes hypeFall{0%{transform:translateY(0) rotate(0deg) scale(0.8);opacity:0}8%{opacity:0.4}90%{opacity:0.25}100%{transform:translateY(110vh) rotate(720deg) scale(1.2);opacity:0}}"},
    "the-overthinker":       {"items": ["🌀","🌙","💭","✨","🌀","🌙","💭","✨","🌀"], "anim": "thinkSpin", "dir": "fixed", "css": "@keyframes thinkSpin{0%,100%{transform:rotate(0deg) scale(0.8);opacity:0.04}50%{transform:rotate(360deg) scale(1.2);opacity:0.25}}"},
    "the-free-spirit":       {"items": ["🌿","🌈","✨","🌍","🌿","🦋","✨","🌿","🌈"], "anim": "spiritFloat", "dir": "bottom", "css": "@keyframes spiritFloat{0%{transform:translateY(0);opacity:0}10%{opacity:0.35}100%{transform:translateY(-115vh);opacity:0}}"},
    "the-nostalgist":        {"items": ["📼","💿","🕰️","✨","📼","💿","🕰️","✨","📼"], "anim": "nostalgiaFade", "dir": "fixed", "css": "@keyframes nostalgiaFade{0%,100%{transform:scale(0.85) rotate(-5deg);opacity:0.04}50%{transform:scale(1.1) rotate(5deg);opacity:0.22}}"},
    "the-rebel":             {"items": ["⚡","🔥","🎸","⚡","🔥","🎸","⚡","🔥","🎸"], "anim": "rebelCrash", "dir": "top", "css": "@keyframes rebelCrash{0%{transform:translateY(0) rotate(0deg);opacity:0}6%{opacity:0.38}88%{opacity:0.2}100%{transform:translateY(110vh) rotate(180deg);opacity:0}}"},
    "the-trendsetter":       {"items": ["✨","🚀","💿","⚡","✨","🪩","🚀","✨","💿"], "anim": "trendRise", "dir": "bottom", "css": "@keyframes trendRise{0%{transform:translateY(0) scale(0.7);opacity:0}10%{opacity:0.5}100%{transform:translateY(-115vh) scale(1.2);opacity:0}}"},
}

POSITIONS = [("8%","6%"),("15%","82%"),("28%","18%"),("44%","72%"),("60%","35%"),("72%","88%"),("38%","55%"),("82%","20%"),("50%","92%")]

def render_persona_animation(persona_id):
    anim = PERSONA_ANIMATIONS.get(persona_id)
    if not anim:
        return
    uid = persona_id.replace("-", "_")
    items_html = ""
    for i, item in enumerate(anim["items"]):
        delay = i * 0.9
        duration = 8 + (i % 3) * 2
        if anim["dir"] == "top":
            pos = f"top:-10%;left:{10 + i*10}%;"
        elif anim["dir"] == "bottom":
            pos = f"bottom:-80px;left:{5 + i*10}%;"
        elif anim["dir"] == "left":
            top, _ = POSITIONS[i]
            pos = f"top:{top};left:-15%;"
        else:
            top, left = POSITIONS[i]
            pos = f"top:{top};left:{left};"
        items_html += f'<div style="position:absolute;{pos}font-size:1.8rem;opacity:0;animation:{anim["anim"]} {duration}s ease-in-out {delay}s infinite;">{item}</div>'
    st.markdown(f'<style>#{uid}_layer{{position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999;}}{anim["css"]}</style><div id="{uid}_layer">{items_html}</div>', unsafe_allow_html=True)


def dna_bar(label, value, color):
    """Helper function: renders a single DNA progress bar as HTML."""
    return f"""
    <div style="margin-bottom:0.9rem;">
        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
            <span style="font-size:0.82rem;color:rgba(255,255,255,0.7);">{label}</span>
            <span style="font-size:0.82rem;color:{color};font-weight:600;">{value}%</span>
        </div>
        <div style="background:rgba(255,255,255,0.1);border-radius:50px;height:8px;overflow:hidden;">
            <div style="width:{value}%;background:linear-gradient(90deg,{color}88,{color});height:100%;border-radius:50px;"></div>
        </div>
    </div>"""


def restart():
    """Helper function: clears all session state to restart the quiz."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]


# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Your Life as a Playlist", page_icon="🎵", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Inter:wght@400;500;600&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);min-height:100vh;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:white!important;}
p,label,.stMarkdown{color:#e0e0e0!important;}
.hero-title{font-family:'Playfair Display',serif;font-size:3rem;font-weight:700;color:white;text-align:center;line-height:1.2;margin-bottom:0.4rem;}
.hero-sub{font-size:1.05rem;color:#b0b0cc;text-align:center;margin-bottom:2rem;}
.step-badge{display:block;text-align:center;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);border-radius:50px;padding:6px 20px;font-size:0.82rem;color:#c0c0e0;margin:0 auto 1.5rem auto;width:fit-content;}
.question-card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:1.75rem 2rem 1rem 2rem;margin-bottom:1.25rem;}
.question-text{font-family:'Playfair Display',serif;font-size:1.55rem;color:white;line-height:1.4;}
.progress-dots{display:flex;justify-content:center;gap:8px;margin-bottom:1.25rem;}
.dot{width:9px;height:9px;border-radius:50%;background:rgba(255,255,255,0.18);}
.dot.active{background:white;} .dot.done{background:rgba(255,255,255,0.55);}
.stButton>button{background:rgba(255,255,255,0.07)!important;border:1px solid rgba(255,255,255,0.18)!important;border-radius:14px!important;color:white!important;font-size:0.95rem!important;font-family:'Inter',sans-serif!important;padding:0.75rem 1.2rem!important;width:100%!important;text-align:left!important;transition:all 0.2s ease!important;margin-bottom:0.5rem!important;}
.stButton>button:hover{background:rgba(255,255,255,0.16)!important;border-color:rgba(255,255,255,0.38)!important;transform:translateX(5px)!important;}
div[data-baseweb="input"]>div{background:rgba(255,255,255,0.92)!important;border:1px solid rgba(255,255,255,0.3)!important;border-radius:12px!important;}
div[data-baseweb="input"] input{color:#1a1a2e!important;-webkit-text-fill-color:#1a1a2e!important;caret-color:#1a1a2e!important;background:transparent!important;font-size:1rem!important;}
div[data-baseweb="input"] input::placeholder{color:rgba(26,26,46,0.4)!important;-webkit-text-fill-color:rgba(26,26,46,0.4)!important;}
.stTextInput>label{color:#c0c0e0!important;font-size:0.9rem!important;}
.loading-screen{text-align:center;padding:3rem 1rem;}
.loading-msg{font-family:'Playfair Display',serif;font-size:1.4rem;color:white;margin:1rem 0;opacity:0.9;}
.loading-dots{display:inline-flex;gap:8px;margin-top:1.5rem;}
.loading-dot{width:10px;height:10px;border-radius:50%;background:rgba(167,139,250,0.8);animation:loadBounce 1.2s ease-in-out infinite;}
.loading-dot:nth-child(2){animation-delay:0.2s;background:rgba(244,114,182,0.8);}
.loading-dot:nth-child(3){animation-delay:0.4s;background:rgba(167,139,250,0.8);}
@keyframes loadBounce{0%,80%,100%{transform:scale(0.7);opacity:0.5;}40%{transform:scale(1.2);opacity:1;}}
.result-card{border-radius:24px;padding:2.5rem 2rem;text-align:center;margin:1rem 0;animation:resultReveal 0.6s ease forwards;}
@keyframes resultReveal{from{opacity:0;transform:translateY(20px) scale(0.97);}to{opacity:1;transform:translateY(0) scale(1);}}
.result-emoji{font-size:4.5rem;display:block;margin-bottom:0.5rem;}
.result-name{font-family:'Playfair Display',serif;font-size:2.6rem;font-weight:700;margin-bottom:1rem;}
.result-desc{font-size:1.05rem;line-height:1.75;margin-bottom:1.5rem;opacity:0.92;}
.anthem-box{background:rgba(0,0,0,0.18);border-radius:12px;padding:0.9rem 1.4rem;margin-bottom:1.4rem;font-size:0.95rem;}
.trait-pill{display:inline-block;background:rgba(0,0,0,0.15);border-radius:50px;padding:5px 16px;margin:4px;font-size:0.82rem;font-weight:500;}
.section-title{font-family:'Playfair Display',serif;font-size:1.2rem;color:white;margin:1.5rem 0 0.75rem 0;}
.artist-chip{display:inline-block;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);border-radius:50px;padding:6px 16px;margin:4px;font-size:0.85rem;color:#e0e0e0;}
.intro-stat{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);border-radius:16px;padding:1.2rem;text-align:center;}
.intro-stat-num{font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;color:white;}
.intro-stat-label{font-size:0.8rem;color:#b0b0cc;margin-top:2px;}
.persona-preview-pill{display:inline-block;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:50px;padding:5px 14px;margin:3px;font-size:0.8rem;color:#c8c8e8;}
.stProgress>div>div{background:rgba(255,255,255,0.1)!important;border-radius:10px!important;}
.stProgress>div>div>div{background:linear-gradient(90deg,#a78bfa,#f472b6)!important;border-radius:10px!important;}
footer{visibility:hidden;}#MainMenu{visibility:hidden;}header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── Session state defaults (Topic 2: flow control) ────────────────────────────
defaults = {
    "step": "intro",
    "artist_scores": {},
    "quiz_scores": {},
    "quiz_step": 0,
    "artist_names_found": [],
    "celebrated": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

@st.cache_data
def get_data():
    return load_data("database_artists.xlsx")

data = get_data()

# ═══════════════════════════════════════════════════════════════
# TOPIC 2 — FLOW CONTROL: step routing using if/elif/else
# Each screen is a separate state, controlled by conditions
# ═══════════════════════════════════════════════════════════════

# ── INTRO ─────────────────────────────────────────────────────
if st.session_state.step == "intro":
    st.markdown('<div class="hero-title">🎵 Your Life<br><em>as a Playlist</em></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Find out which music persona you actually are.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="intro-stat"><div class="intro-stat-num">13</div><div class="intro-stat-label">possible personas</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="intro-stat"><div class="intro-stat-num">10</div><div class="intro-stat-label">quiz questions</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="intro-stat"><div class="intro-stat-num">600+</div><div class="intro-stat-label">artists in our database</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-bottom:1.5rem;">
        <span style="font-size:1rem;color:rgba(255,255,255,0.38);letter-spacing:0.05em;font-style:italic;">
            We'll reveal your music identity at the end.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="question-card" style="text-align:center;">
        <div style="font-size:1rem;color:rgba(255,255,255,0.75);line-height:1.8;">
            Tell us your top 3 artists.<br>
            Answer 10 questions about how you experience music.<br>
            We combine both to reveal your true music identity.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Let's find my sound →", use_container_width=True):
        st.session_state.step = "artists"
        st.rerun()

# ── STEP 1: ARTIST INPUT ──────────────────────────────────────
elif st.session_state.step == "artists":
    st.markdown('<div class="hero-title">🎵 Your Life<br>as a Playlist</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">✦ Step 1 of 2 — Your top artists</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="question-card">
        <div class="question-text">Which artists define your soundtrack?</div>
        <div style="font-size:0.9rem;color:rgba(255,255,255,0.5);margin-top:0.5rem;">Enter up to 3. At least 1 is required.</div>
    </div>
    """, unsafe_allow_html=True)

    artist1 = st.text_input("Artist #1", placeholder="e.g. Taylor Swift")
    artist2 = st.text_input("Artist #2 (optional)", placeholder="e.g. Kendrick Lamar")
    artist3 = st.text_input("Artist #3 (optional)", placeholder="e.g. Adele")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Next — Take the quiz →", use_container_width=True):
        artists = [a for a in [artist1, artist2, artist3] if a.strip()]

        # Flow control: check if input is empty
        if not artists:
            st.warning("Please enter at least one artist.")
        else:
            artist_scores = {}
            found_names = []

            # for loop: process each artist input
            for name in artists:
                result = search_artist(name, data)
                if isinstance(result, dict):           # if artist found
                    pid = genre_to_persona_id(result.get("genre", ""))
                    artist_scores[pid] = artist_scores.get(pid, 0) + 3
                    found_names.append(name)

            # Flow control: check if any artists were found
            if not found_names:
                st.error("None of those artists were found. Try checking the spelling.")
                st.stop()
            else:
                st.session_state.artist_scores = artist_scores
                st.session_state.artist_names_found = found_names
                st.session_state.step = "quiz"
                st.rerun()

# ── STEP 2: QUIZ ──────────────────────────────────────────────
elif st.session_state.step == "quiz":
    q_idx = st.session_state.quiz_step
    total = len(QUIZ_QUESTIONS)

    st.markdown('<div class="hero-title">🎵 Your Life<br>as a Playlist</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="step-badge">✦ Step 2 of 2 — Question {q_idx + 1} of {total}</div>', unsafe_allow_html=True)

    # for loop: build progress dots
    dots = "".join([
        f'<div class="dot {"done" if i < q_idx else "active" if i == q_idx else ""}"></div>'
        for i in range(total)
    ])
    st.markdown(f'<div class="progress-dots">{dots}</div>', unsafe_allow_html=True)
    st.progress(q_idx / total)

    q = QUIZ_QUESTIONS[q_idx]
    st.markdown(f'<div class="question-card"><div class="question-text">{q["question"]}</div></div>', unsafe_allow_html=True)

    # for loop: display answer buttons
    for i, (option_text, p1, p2) in enumerate(q["options"]):
        if st.button(option_text, key=f"q{q_idx}_opt{i}", use_container_width=True):
            st.session_state.quiz_scores[p1] = st.session_state.quiz_scores.get(p1, 0) + 2
            st.session_state.quiz_scores[p2] = st.session_state.quiz_scores.get(p2, 0) + 1

            # if/else: check if quiz is finished
            if q_idx + 1 >= total:
                st.session_state.step = "loading"
            else:
                st.session_state.quiz_step += 1
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Start over"):
        restart()
        st.rerun()

# ── LOADING SCREEN ────────────────────────────────────────────
elif st.session_state.step == "loading":
    st.markdown('<div class="hero-title">🎵 Your Life<br>as a Playlist</div>', unsafe_allow_html=True)

    # List of loading messages
    messages = [
        ("🎧", "Analyzing your artists..."),
        ("✨", "Reading your playlist energy..."),
        ("🎼", "Matching your music personality..."),
        ("💿", "Revealing your identity..."),
    ]

    placeholder = st.empty()

    # for loop: cycle through loading messages
    for emoji, msg in messages:
        placeholder.markdown(f"""
        <div class="loading-screen">
            <div style="font-size:3.5rem;margin-bottom:1rem;">{emoji}</div>
            <div class="loading-msg">{msg}</div>
            <div class="loading-dots">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.9)

    placeholder.empty()
    st.session_state.step = "result"
    st.rerun()

# ── RESULT ────────────────────────────────────────────────────
elif st.session_state.step == "result":

    # TOPIC 3: call merge_and_decide function to get winning persona
    persona_id = merge_and_decide(
        st.session_state.artist_scores,
        st.session_state.quiz_scores
    )

    # TOPIC 4: instantiate the MusicPersona class with the result
    persona = MusicPersona(
        persona_id=persona_id,
        artist_names_found=st.session_state.artist_names_found
    )

    # One-time celebration using if/elif
    if not st.session_state.celebrated:
        if persona.persona_id in ("the-life-of-the-party", "the-hype-beast"):
            st.balloons()
        elif persona.persona_id == "the-daydreamer":
            st.snow()
        st.session_state.celebrated = True

    # Render background animation for this persona
    render_persona_animation(persona.persona_id)

    # Build HTML from class attributes (Topic 4 in use)
    traits_html = "".join([
        f'<span class="trait-pill">{t}</span>' for t in persona.traits
    ])

    artist_note = ""
    if persona.artist_sources:
        artist_note = f'<p style="opacity:0.6;font-size:0.82rem;margin-top:1.2rem;">Based on: {", ".join(persona.artist_sources)} — combined with your quiz answers.</p>'

    st.markdown('<div class="hero-title">🎵 Your Result</div>', unsafe_allow_html=True)

    # ── Music DNA — reads from persona.dna dictionary ──────────
    st.markdown('<div class="section-title">🧬 Your Music DNA</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:1.5rem;">
        {dna_bar("Energy", persona.dna["energy"], persona.color)}
        {dna_bar("Extroversion", persona.dna["extroversion"], persona.color)}
        {dna_bar("Emotionality", persona.dna["emotionality"], persona.color)}
    </div>
    """, unsafe_allow_html=True)

    # ── Artists you'd vibe with — reads from persona.artists list
    st.markdown('<div class="section-title">🎤 Artists you\'d vibe with</div>', unsafe_allow_html=True)
    # for loop: build artist chips from persona.artists list
    artists_html = "".join([
        f'<span class="artist-chip">♪ {a}</span>' for a in persona.artists
    ])
    st.markdown(f'<div style="text-align:center;">{artists_html}</div>', unsafe_allow_html=True)

    # ── Shareable card ─────────────────────────────────────────
    st.markdown('<div class="section-title">📸 Your shareable card</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.85rem;color:rgba(255,255,255,0.5);margin-bottom:0.75rem;">Screenshot this and share it!</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:linear-gradient(145deg,#0f0c29,{persona.color}55,#0f0c29);border:2px solid {persona.color}88;border-radius:24px;padding:2.5rem 2rem;text-align:center;max-width:420px;margin:0 auto;">
        <div style="font-size:0.75rem;letter-spacing:0.18em;text-transform:uppercase;color:{persona.color};margin-bottom:1rem;font-weight:600;">Your Life as a Playlist</div>
        <div style="font-size:4rem;margin-bottom:0.5rem;">{persona.emoji}</div>
        <div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;color:{persona.color};margin-bottom:0.75rem;line-height:1.2;">{persona.name}</div>
        <div style="font-size:0.85rem;color:rgba(255,255,255,0.75);line-height:1.65;margin-bottom:1.25rem;padding:0 0.5rem;">{persona.description[:120]}...</div>
        <div style="background:rgba(0,0,0,0.3);border-radius:10px;padding:0.75rem 1rem;margin-bottom:1.25rem;font-size:0.85rem;color:{persona.color};">🎶 <strong>{persona.anthem}</strong></div>
        <div style="font-size:0.75rem;color:rgba(255,255,255,0.5);margin-bottom:0.5rem;">{persona.get_traits_string()}</div>
        <div style="margin-top:1rem;font-size:0.7rem;color:rgba(255,255,255,0.3);letter-spacing:0.1em;">yourlifeasaplaylist.streamlit.app</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Copy text — uses persona.get_share_text() method ───────
    st.markdown("<br>", unsafe_allow_html=True)
    st.code(persona.get_share_text(), language=None)
    st.markdown('<p style="font-size:0.8rem;color:rgba(255,255,255,0.4);text-align:center;margin-top:-0.5rem;">↑ Copy this to share your result in chats</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Take it again", use_container_width=True):
        restart()
        st.rerun()
