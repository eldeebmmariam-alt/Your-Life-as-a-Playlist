import streamlit as st
import pandas as pd
import time

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

# ── 13 Personas ───────────────────────────────────────────────────────────────
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

GENRE_TO_PERSONA = {
    "Pop": "the-life-of-the-party", "Dance": "the-life-of-the-party",
    "K-Pop": "the-life-of-the-party", "Afrobeats": "the-life-of-the-party",
    "Reggaeton": "the-hype-beast", "Hip-Hop": "the-hype-beast",
    "Trap": "the-hype-beast", "Drill": "the-hype-beast", "Grime": "the-hype-beast",
    "R&B/Pop": "the-main-character", "Pop/R&B": "the-main-character",
    "R&B": "the-romantic", "Soul/Pop": "the-romantic",
    "Lo-fi": "the-chill-soul", "Neo Soul": "the-chill-soul",
    "Acoustic": "the-chill-soul", "Jazz/Pop": "the-chill-soul", "Soul/R&B": "the-chill-soul",
    "Indie Pop": "the-daydreamer", "Dream Pop": "the-daydreamer", "Electropop": "the-daydreamer",
    "Folk/Indie": "the-lone-wolf", "Shoegaze": "the-lone-wolf", "Ambient": "the-lone-wolf",
    "Classic Rock": "the-old-soul", "Jazz": "the-old-soul", "Blues": "the-old-soul", "Soul/Jazz": "the-old-soul",
    "Electronic/Hip-Hop": "the-overthinker", "Progressive": "the-overthinker",
    "Psychedelic Rock": "the-overthinker", "Art Rock": "the-overthinker", "Trip-hop": "the-overthinker",
    "Post-punk": "the-rebel", "Punk Rock": "the-rebel", "Grunge": "the-rebel",
    "Metal": "the-rebel", "Alternative Rock": "the-rebel",
    "Pop-Punk": "the-nostalgist", "Emo": "the-nostalgist", "Britpop": "the-nostalgist",
    "World": "the-free-spirit", "Folk/Pop": "the-free-spirit",
    "Reggae": "the-free-spirit", "Latin": "the-free-spirit",
    "Hyperpop": "the-trendsetter", "Experimental": "the-trendsetter",
    "Electronic": "the-trendsetter", "UK Rap": "the-trendsetter",
}

def genre_to_persona_id(genre):
    for key, pid in GENRE_TO_PERSONA.items():
        if key.lower() in genre.lower():
            return pid
    return "the-free-spirit"

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

# ── Persona background animations (all 13) ────────────────────────────────────
PERSONA_ANIMATIONS = {
    "the-life-of-the-party": {
        "class": "party-layer",
        "items": ["🎉", "✨", "🎊", "✨", "🎉", "🥳", "🎊", "✨", "🎉"],
        "css": """
            .party-layer { position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999; }
            .party-item { position:absolute;top:-10%;font-size:1.6rem;opacity:0;animation:partyFall 8s linear infinite; }
            .party-item:nth-child(1){left:8%;animation-delay:0s}
            .party-item:nth-child(2){left:18%;animation-delay:1s}
            .party-item:nth-child(3){left:30%;animation-delay:2s}
            .party-item:nth-child(4){left:42%;animation-delay:3s}
            .party-item:nth-child(5){left:54%;animation-delay:4s}
            .party-item:nth-child(6){left:65%;animation-delay:1.5s}
            .party-item:nth-child(7){left:75%;animation-delay:2.5s}
            .party-item:nth-child(8){left:85%;animation-delay:3.5s}
            .party-item:nth-child(9){left:93%;animation-delay:0.5s}
            @keyframes partyFall {
                0%{transform:translateY(0) rotate(0deg);opacity:0}
                10%{opacity:0.35}
                90%{opacity:0.2}
                100%{transform:translateY(110vh) rotate(360deg);opacity:0}
            }
        """,
        "item_class": "party-item"
    },
    "the-main-character": {
        "class": "main-layer",
        "items": ["⭐", "✨", "🌟", "✨", "⭐", "🌟", "✨", "⭐", "🌟"],
        "css": """
            .main-layer { position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999; }
            .main-item { position:absolute;font-size:1.8rem;opacity:0;animation:mainTwinkle 5s ease-in-out infinite; }
            .main-item:nth-child(1){top:10%;left:10%;animation-delay:0s}
            .main-item:nth-child(2){top:20%;left:80%;animation-delay:0.6s}
            .main-item:nth-child(3){top:38%;left:22%;animation-delay:1.2s}
            .main-item:nth-child(4){top:52%;left:70%;animation-delay:1.8s}
            .main-item:nth-child(5){top:68%;left:40%;animation-delay:2.4s}
            .main-item:nth-child(6){top:80%;left:15%;animation-delay:3s}
            .main-item:nth-child(7){top:15%;left:55%;animation-delay:3.6s}
            .main-item:nth-child(8){top:45%;left:88%;animation-delay:4.2s}
            .main-item:nth-child(9){top:75%;left:65%;animation-delay:0.3s}
            @keyframes mainTwinkle {
                0%,100%{transform:scale(0.7);opacity:0.05}
                50%{transform:scale(1.3);opacity:0.3}
            }
        """,
        "item_class": "main-item"
    },
    "the-daydreamer": {
        "class": "dream-layer",
        "items": ["☁️", "✨", "☁️", "🌙", "☁️", "✨", "☁️", "🌙", "☁️"],
        "css": """
            .dream-layer { position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999; }
            .dream-item { position:absolute;font-size:2rem;opacity:0;animation:dreamDrift 18s linear infinite; }
            .dream-item:nth-child(1){top:8%;left:-12%;animation-delay:0s}
            .dream-item:nth-child(2){top:22%;left:-18%;animation-delay:3s}
            .dream-item:nth-child(3){top:38%;left:-10%;animation-delay:6s}
            .dream-item:nth-child(4){top:54%;left:-15%;animation-delay:9s}
            .dream-item:nth-child(5){top:70%;left:-12%;animation-delay:12s}
            .dream-item:nth-child(6){top:15%;left:-20%;animation-delay:1.5s}
            .dream-item:nth-child(7){top:45%;left:-8%;animation-delay:4.5s}
            .dream-item:nth-child(8){top:62%;left:-18%;animation-delay:7.5s}
            .dream-item:nth-child(9){top:82%;left:-14%;animation-delay:10.5s}
            @keyframes dreamDrift {
                0%{transform:translateX(0);opacity:0}
                8%{opacity:0.25}
                90%{opacity:0.15}
                100%{transform:translateX(125vw);opacity:0}
            }
        """,
        "item_class": "dream-item"
    },
    "the-chill-soul": {
        "class": "chill-layer",
        "items": ["🍃", "☕", "✨", "🍃", "🌿", "✨", "☕", "🍃", "✨"],
        "css": """
            .chill-layer { position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999; }
            .chill-item { position:absolute;bottom:-80px;font-size:1.9rem;opacity:0;animation:chillFloat 12s linear infinite; }
            .chill-item:nth-child(1){left:6%;animation-delay:0s;animation-duration:12s}
            .chill-item:nth-child(2){left:16%;animation-delay:1s;animation-duration:14s}
            .chill-item:nth-child(3){left:28%;animation-delay:2s;animation-duration:11s}
            .chill-item:nth-child(4){left:40%;animation-delay:3s;animation-duration:13s}
            .chill-item:nth-child(5){left:52%;animation-delay:1.5s;animation-duration:15s}
            .chill-item:nth-child(6){left:64%;animation-delay:2.5s;animation-duration:12s}
            .chill-item:nth-child(7){left:74%;animation-delay:4s;animation-duration:14s}
            .chill-item:nth-child(8){left:84%;animation-delay:5s;animation-duration:11s}
            .chill-item:nth-child(9){left:92%;animation-delay:3.5s;animation-duration:13s}
            @keyframes chillFloat {
                0%{transform:translateY(0) rotate(0deg);opacity:0}
                12%{opacity:0.5}
                85%{opacity:0.25}
                100%{transform:translateY(-115vh) rotate(15deg);opacity:0}
            }
        """,
        "item_class": "chill-item"
    },
    "the-lone-wolf": {
        "class": "wolf-layer",
        "items": ["🌙", "⭐", "🌑", "✨", "🌙", "⭐", "🌑", "✨", "🌙"],
        "css": """
            .wolf-layer { position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999; }
            .wolf-item { position:absolute;font-size:1.6rem;opacity:0;animation:wolfPulse 7s ease-in-out infinite; }
            .wolf-item:nth-child(1){top:5%;left:5%;animation-delay:0s}
            .wolf-item:nth-child(2){top:15%;left:88%;animation-delay:1s}
            .wolf-item:nth-child(3){top:30%;left:12%;animation-delay:2s}
            .wolf-item:nth-child(4){top:48%;left:78%;animation-delay:3s}
            .wolf-item:nth-child(5){top:62%;left:25%;animation-delay:4s}
            .wolf-item:nth-child(6){top:75%;left:90%;animation-delay:5s}
            .wolf-item:nth-child(7){top:85%;left:45%;animation-delay:6s}
            .wolf-item:nth-child(8){top:35%;left:55%;animation-delay:0.5s}
            .wolf-item:nth-child(9){top:55%;left:8%;animation-delay:1.5s}
            @keyframes wolfPulse {
                0%,100%{transform:scale(0.8);opacity:0.04}
                50%{transform:scale(1.2);opacity:0.22}
            }
        """,
        "item_class": "wolf-item"
    },
    "the-romantic": {
        "class": "romantic-layer",
        "items": ["💖", "🦋", "💕", "✨", "💗", "🦋", "💖", "💕", "✨"],
        "css": """
            .romantic-layer { position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999; }
            .romantic-item { position:absolute;bottom:-80px;font-size:1.9rem;opacity:0;animation:romanticRise 11s linear infinite; }
            .romantic-item:nth-child(1){left:8%;animation-delay:0s}
            .romantic-item:nth-child(2){left:20%;animation-delay:1.5s}
            .romantic-item:nth-child(3){left:33%;animation-delay:3s}
            .romantic-item:nth-child(4){left:46%;animation-delay:4.5s}
            .romantic-item:nth-child(5){left:59%;animation-delay:6s}
            .romantic-item:nth-child(6){left:70%;animation-delay:7.5s}
            .romantic-item:nth-child(7){left:80%;animation-delay:9s}
            .romantic-item:nth-child(8){left:88%;animation-delay:2s}
            .romantic-item:nth-child(9){left:14%;animation-delay:5s}
            @keyframes romanticRise {
                0%{transform:translateY(0) scale(1);opacity:0}
                15%{opacity:0.35}
                100%{transform:translateY(-115vh) scale(1.2);opacity:0}
            }
        """,
        "item_class": "romantic-item"
    },
    "the-old-soul": {
        "class": "oldsoul-layer",
        "items": ["🎷", "📻", "🎶", "✨", "🎷", "📻", "🎶", "✨", "🎷"],
        "css": """
            .oldsoul-layer { position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999; }
            .oldsoul-item { position:absolute;font-size:1.7rem;opacity:0;animation:oldSoulSway 9s ease-in-out infinite; }
            .oldsoul-item:nth-child(1){top:8%;left:8%;animation-delay:0s}
            .oldsoul-item:nth-child(2){top:20%;left:82%;animation-delay:1s}
            .oldsoul-item:nth-child(3){top:36%;left:18%;animation-delay:2s}
            .oldsoul-item:nth-child(4){top:52%;left:72%;animation-delay:3s}
            .oldsoul-item:nth-child(5){top:66%;left:35%;animation-delay:4s}
            .oldsoul-item:nth-child(6){top:78%;left:88%;animation-delay:5s}
            .oldsoul-item:nth-child(7){top:42%;left:55%;animation-delay:6s}
            .oldsoul-item:nth-child(8){top:14%;left:45%;animation-delay:7s}
            .oldsoul-item:nth-child(9){top:85%;left:22%;animation-delay:8s}
            @keyframes oldSoulSway {
                0%,100%{transform:rotate(-8deg) scale(0.85);opacity:0.05}
                50%{transform:rotate(8deg) scale(1.1);opacity:0.22}
            }
        """,
        "item_class": "oldsoul-item"
    },
    "the-hype-beast": {
        "class": "hype-layer",
        "items": ["🔥", "⚡", "💥", "🔥", "⚡", "💥", "🔥", "⚡", "💥"],
        "css": """
            .hype-layer { position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999; }
            .hype-item { position:absolute;top:-10%;font-size:1.7rem;opacity:0;animation:hypeFall 6s linear infinite; }
            .hype-item:nth-child(1){left:6%;animation-delay:0s}
            .hype-item:nth-child(2){left:16%;animation-delay:0.7s}
            .hype-item:nth-child(3){left:28%;animation-delay:1.4s}
            .hype-item:nth-child(4){left:40%;animation-delay:2.1s}
            .hype-item:nth-child(5){left:52%;animation-delay:2.8s}
            .hype-item:nth-child(6){left:64%;animation-delay:3.5s}
            .hype-item:nth-child(7){left:74%;animation-delay:4.2s}
            .hype-item:nth-child(8){left:84%;animation-delay:4.9s}
            .hype-item:nth-child(9){left:92%;animation-delay:0.35s}
            @keyframes hypeFall {
                0%{transform:translateY(0) rotate(0deg) scale(0.8);opacity:0}
                8%{opacity:0.4}
                90%{opacity:0.25}
                100%{transform:translateY(110vh) rotate(720deg) scale(1.2);opacity:0}
            }
        """,
        "item_class": "hype-item"
    },
    "the-overthinker": {
        "class": "think-layer",
        "items": ["🌀", "🌙", "💭", "✨", "🌀", "🌙", "💭", "✨", "🌀"],
        "css": """
            .think-layer { position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999; }
            .think-item { position:absolute;font-size:1.7rem;opacity:0;animation:thinkSpin 8s ease-in-out infinite; }
            .think-item:nth-child(1){top:10%;left:12%;animation-delay:0s}
            .think-item:nth-child(2){top:24%;left:80%;animation-delay:1s}
            .think-item:nth-child(3){top:40%;left:20%;animation-delay:2s}
            .think-item:nth-child(4){top:56%;left:68%;animation-delay:3s}
            .think-item:nth-child(5){top:70%;left:32%;animation-delay:4s}
            .think-item:nth-child(6){top:82%;left:82%;animation-delay:5s}
            .think-item:nth-child(7){top:18%;left:50%;animation-delay:6s}
            .think-item:nth-child(8){top:46%;left:90%;animation-delay:7s}
            .think-item:nth-child(9){top:64%;left:5%;animation-delay:0.5s}
            @keyframes thinkSpin {
                0%,100%{transform:rotate(0deg) scale(0.8);opacity:0.04}
                50%{transform:rotate(360deg) scale(1.2);opacity:0.25}
            }
        """,
        "item_class": "think-item"
    },
    "the-free-spirit": {
        "class": "spirit-layer",
        "items": ["🌿", "🌈", "✨", "🌍", "🌿", "🦋", "✨", "🌿", "🌈"],
        "css": """
            .spirit-layer { position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999; }
            .spirit-item { position:absolute;bottom:-80px;font-size:1.9rem;opacity:0;animation:spiritFloat 13s linear infinite; }
            .spirit-item:nth-child(1){left:5%;animation-delay:0s;animation-duration:13s}
            .spirit-item:nth-child(2){left:15%;animation-delay:1.5s;animation-duration:15s}
            .spirit-item:nth-child(3){left:27%;animation-delay:3s;animation-duration:12s}
            .spirit-item:nth-child(4){left:40%;animation-delay:4.5s;animation-duration:14s}
            .spirit-item:nth-child(5){left:53%;animation-delay:6s;animation-duration:16s}
            .spirit-item:nth-child(6){left:65%;animation-delay:7.5s;animation-duration:13s}
            .spirit-item:nth-child(7){left:76%;animation-delay:2s;animation-duration:15s}
            .spirit-item:nth-child(8){left:86%;animation-delay:5s;animation-duration:12s}
            .spirit-item:nth-child(9){left:93%;animation-delay:8s;animation-duration:14s}
            @keyframes spiritFloat {
                0%{transform:translateY(0) translateX(0) rotate(0deg);opacity:0}
                10%{opacity:0.35}
                50%{transform:translateY(-55vh) translateX(20px) rotate(10deg);opacity:0.25}
                100%{transform:translateY(-115vh) translateX(-15px) rotate(-5deg);opacity:0}
            }
        """,
        "item_class": "spirit-item"
    },
    "the-nostalgist": {
        "class": "nostalgia-layer",
        "items": ["📼", "💿", "🕰️", "✨", "📼", "💿", "🕰️", "✨", "📼"],
        "css": """
            .nostalgia-layer { position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999; }
            .nostalgia-item { position:absolute;font-size:1.7rem;opacity:0;animation:nostalgiaFade 10s ease-in-out infinite; }
            .nostalgia-item:nth-child(1){top:8%;left:8%;animation-delay:0s}
            .nostalgia-item:nth-child(2){top:22%;left:78%;animation-delay:1.1s}
            .nostalgia-item:nth-child(3){top:38%;left:15%;animation-delay:2.2s}
            .nostalgia-item:nth-child(4){top:55%;left:68%;animation-delay:3.3s}
            .nostalgia-item:nth-child(5){top:70%;left:30%;animation-delay:4.4s}
            .nostalgia-item:nth-child(6){top:82%;left:85%;animation-delay:5.5s}
            .nostalgia-item:nth-child(7){top:16%;left:50%;animation-delay:6.6s}
            .nostalgia-item:nth-child(8){top:44%;left:88%;animation-delay:7.7s}
            .nostalgia-item:nth-child(9){top:62%;left:5%;animation-delay:8.8s}
            @keyframes nostalgiaFade {
                0%,100%{transform:scale(0.85) rotate(-5deg);opacity:0.04}
                50%{transform:scale(1.1) rotate(5deg);opacity:0.22}
            }
        """,
        "item_class": "nostalgia-item"
    },
    "the-rebel": {
        "class": "rebel-layer",
        "items": ["⚡", "🔥", "🎸", "⚡", "🔥", "🎸", "⚡", "🔥", "🎸"],
        "css": """
            .rebel-layer { position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999; }
            .rebel-item { position:absolute;top:-10%;font-size:1.7rem;opacity:0;animation:rebelCrash 7s linear infinite; }
            .rebel-item:nth-child(1){left:5%;animation-delay:0s}
            .rebel-item:nth-child(2){left:16%;animation-delay:0.8s}
            .rebel-item:nth-child(3){left:28%;animation-delay:1.6s}
            .rebel-item:nth-child(4){left:40%;animation-delay:2.4s}
            .rebel-item:nth-child(5){left:52%;animation-delay:3.2s}
            .rebel-item:nth-child(6){left:64%;animation-delay:4s}
            .rebel-item:nth-child(7){left:74%;animation-delay:4.8s}
            .rebel-item:nth-child(8){left:84%;animation-delay:5.6s}
            .rebel-item:nth-child(9){left:92%;animation-delay:6.4s}
            @keyframes rebelCrash {
                0%{transform:translateY(0) rotate(0deg);opacity:0}
                6%{opacity:0.38}
                88%{opacity:0.2}
                100%{transform:translateY(110vh) rotate(180deg);opacity:0}
            }
        """,
        "item_class": "rebel-item"
    },
    "the-trendsetter": {
        "class": "trend-layer",
        "items": ["✨", "🚀", "💿", "⚡", "✨", "🪩", "🚀", "✨", "💿"],
        "css": """
            .trend-layer { position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999; }
            .trend-item { position:absolute;bottom:-80px;font-size:2rem;opacity:0;animation:trendRise 9s linear infinite; }
            .trend-item:nth-child(1){left:6%;animation-delay:0s;animation-duration:9s}
            .trend-item:nth-child(2){left:16%;animation-delay:1s;animation-duration:11s}
            .trend-item:nth-child(3){left:28%;animation-delay:2s;animation-duration:10s}
            .trend-item:nth-child(4){left:40%;animation-delay:3s;animation-duration:12s}
            .trend-item:nth-child(5){left:52%;animation-delay:1.5s;animation-duration:9.5s}
            .trend-item:nth-child(6){left:64%;animation-delay:2.5s;animation-duration:11.5s}
            .trend-item:nth-child(7){left:76%;animation-delay:4s;animation-duration:10.5s}
            .trend-item:nth-child(8){left:88%;animation-delay:5s;animation-duration:12s}
            .trend-item:nth-child(9){left:95%;animation-delay:3.5s;animation-duration:9s}
            @keyframes trendRise {
                0%{transform:translateY(0) rotate(0deg) scale(0.7);opacity:0}
                10%{opacity:0.5}
                50%{transform:translateY(-50vh) rotate(30deg) scale(1);opacity:0.35}
                100%{transform:translateY(-115vh) rotate(70deg) scale(1.2);opacity:0}
            }
        """,
        "item_class": "trend-item"
    },
}

def render_persona_animation(persona_id):
    anim = PERSONA_ANIMATIONS.get(persona_id)
    if not anim:
        return
    items_html = "".join([f'<div class="{anim["item_class"]}">{item}</div>' for item in anim["items"]])
    st.markdown(f"""
    <style>{anim["css"]}</style>
    <div class="{anim["class"]}">{items_html}</div>
    """, unsafe_allow_html=True)

def merge_and_decide(artist_scores, quiz_scores):
    all_ids = set(list(artist_scores.keys()) + list(quiz_scores.keys()))
    final = {}
    for pid in all_ids:
        final[pid] = (artist_scores.get(pid, 0) * 0.4) + (quiz_scores.get(pid, 0) * 0.6)
    return max(final, key=final.get) if final else "the-free-spirit"

def restart():
    for key in ["step", "artist_scores", "quiz_scores", "quiz_step", "artist_names_found", "celebrated"]:
        if key in st.session_state:
            del st.session_state[key]

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

h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: white !important; }
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

/* Input fields — light background for readability */
div[data-baseweb="input"] > div {
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 12px !important;
}

div[data-baseweb="input"] input {
    color: #1a1a2e !important;
    -webkit-text-fill-color: #1a1a2e !important;
    caret-color: #1a1a2e !important;
    background: transparent !important;
    font-size: 1rem !important;
}

div[data-baseweb="input"] input::placeholder {
    color: rgba(26,26,46,0.4) !important;
    -webkit-text-fill-color: rgba(26,26,46,0.4) !important;
}

.stTextInput > label { color: #c0c0e0 !important; font-size: 0.9rem !important; }

/* Loading screen */
.loading-screen {
    text-align: center;
    padding: 3rem 1rem;
}

.loading-msg {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: white;
    margin: 1rem 0;
    opacity: 0.9;
}

.loading-dots {
    display: inline-flex;
    gap: 8px;
    margin-top: 1.5rem;
}

.loading-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(167,139,250,0.8);
    animation: loadBounce 1.2s ease-in-out infinite;
}

.loading-dot:nth-child(2) { animation-delay: 0.2s; background: rgba(244,114,182,0.8); }
.loading-dot:nth-child(3) { animation-delay: 0.4s; background: rgba(167,139,250,0.8); }

@keyframes loadBounce {
    0%,80%,100% { transform: scale(0.7); opacity: 0.5; }
    40%         { transform: scale(1.2); opacity: 1; }
}

/* Result card */
.result-card {
    border-radius: 24px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin: 1rem 0;
    animation: resultReveal 0.6s ease forwards;
}

@keyframes resultReveal {
    from { opacity: 0; transform: translateY(20px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
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

.artist-note { opacity: 0.6; font-size: 0.82rem; margin-top: 1.2rem; }

.stProgress > div > div { background: rgba(255,255,255,0.1) !important; border-radius: 10px !important; }
.stProgress > div > div > div { background: linear-gradient(90deg, #a78bfa, #f472b6) !important; border-radius: 10px !important; }

footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
defaults = {
    "step": "artists",
    "artist_scores": {},
    "quiz_scores": {},
    "quiz_step": 0,
    "artist_names_found": [],
    "celebrated": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

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
        <div class="question-text">Which artists define your soundtrack?</div>
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
                for name in artists:
                    result = search_artist(name, data)
                    if isinstance(result, dict):
                        pid = genre_to_persona_id(result.get("genre", ""))
                        artist_scores[pid] = artist_scores.get(pid, 0) + 3
            else:
                st.error("None of those artists were found. Try checking the spelling.")
                st.stop()

            st.session_state.artist_scores = artist_scores
            st.session_state.artist_names_found = [
                a for a in artists if isinstance(search_artist(a, data), dict)
            ]
            st.session_state.step = "quiz"
            st.rerun()

# ═══════════════════════════════════════════════════════════════
# STEP 2 — QUIZ
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == "quiz":
    q_idx = st.session_state.quiz_step
    total = len(QUIZ_QUESTIONS)

    st.markdown('<div class="hero-title">🎵 Your Life<br>as a Playlist</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="step-badge">✦ Step 2 of 2 — Question {q_idx + 1} of {total}</div>', unsafe_allow_html=True)

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
        if st.button(option_text, key=f"q{q_idx}_opt{i}", use_container_width=True):
            st.session_state.quiz_scores[p1] = st.session_state.quiz_scores.get(p1, 0) + 2
            st.session_state.quiz_scores[p2] = st.session_state.quiz_scores.get(p2, 0) + 1
            if q_idx + 1 >= total:
                st.session_state.step = "loading"   # ← go to loading step first
            else:
                st.session_state.quiz_step += 1
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Start over"):
        restart()
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# STEP 2.5 — LOADING SCREEN (fixed: its own step so it renders)
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == "loading":

    st.markdown('<div class="hero-title">🎵 Your Life<br>as a Playlist</div>', unsafe_allow_html=True)

    messages = [
        ("🎧", "Analyzing your artists..."),
        ("✨", "Reading your playlist energy..."),
        ("🎼", "Matching your music personality..."),
        ("💿", "Revealing your identity..."),
    ]

    placeholder = st.empty()

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
        time.sleep(0.85)

    placeholder.empty()
    st.session_state.step = "result"
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

    # One-time celebration
    if not st.session_state.celebrated:
        if persona_id in ("the-life-of-the-party", "the-hype-beast"):
            st.balloons()
        elif persona_id == "the-daydreamer":
            st.snow()
        st.session_state.celebrated = True

    # Continuous background animation
    render_persona_animation(persona_id)

    traits_html = "".join([f'<span class="trait-pill">{t}</span>' for t in p["traits"]])
    artist_note = ""
    if st.session_state.artist_names_found:
        artist_note = f'<p class="artist-note">Based on your artists: {", ".join(st.session_state.artist_names_found)} — combined with your quiz answers.</p>'

    st.markdown('<div class="hero-title">🎵 Your Result</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Your music identity has been revealed.</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card" style="background:linear-gradient(135deg,{p['color']}22,{p['color']}44);border:2px solid {p['color']}55;">
        <span class="result-emoji">{p['emoji']}</span>
        <div class="result-name" style="color:{p['color']};">{p['name']}</div>
        <div class="result-desc" style="color:white;">{p['description']}</div>
        <div class="anthem-box" style="color:{p['color']};">
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
