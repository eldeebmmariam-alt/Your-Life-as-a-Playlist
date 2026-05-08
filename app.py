import streamlit as st
import pandas as pd
import time
import io
import os
from PIL import Image, ImageDraw, ImageFont

# ============================================================
# TOPIC 1 — DATA STRUCTURES & EXPRESSIONS
# ============================================================

PERSONA_DETAILS = {
    "the-life-of-the-party": {
        "name": "The Life of the Party", "emoji": "🎉", "color": "#D85A30",
        "description": "You don't just attend the function — you ARE the function. Your energy is infectious, your playlist converts skeptics, and somehow you know every word to songs you've never even heard. You live for the moments that become memories.",
        "anthem": "As It Was — Harry Styles",
        "traits": ["Crowd Magnetizer", "Vibes Architect", "Last One Standing"],
        "artists": ["Harry Styles", "Dua Lipa", "Doja Cat", "Burna Boy"],
        "dna": {"energy": 90, "extroversion": 95, "emotionality": 55},
        "recs": [
            {"title": "Miracle", "artist": "Calvin Harris ft. Ellie Goulding", "why": "Built for the moment the whole room locks in."},
            {"title": "Adore You", "artist": "Harry Styles", "why": "The song that makes strangers feel like friends."},
            {"title": "Temperature", "artist": "Sean Paul", "why": "Criminally underrated. Still hits harder than most things this decade."},
        ],
    },
    "the-main-character": {
        "name": "The Main Character", "emoji": "🎬", "color": "#C0392B",
        "description": "Your playlist feels like a movie soundtrack and you are definitely the lead role. Every walk somewhere is a music video, every mundane moment deserves a cinematic score. Life is the stage and you've always known your cue.",
        "anthem": "Starboy — The Weeknd",
        "traits": ["Cinematic Thinker", "Moment Maximizer", "Effortlessly Iconic"],
        "artists": ["The Weeknd", "Beyonce", "Drake", "Kendrick Lamar"],
        "dna": {"energy": 80, "extroversion": 85, "emotionality": 70},
        "recs": [
            {"title": "Pursuit of Happiness", "artist": "Kid Cudi", "why": "The anthem for anyone living entirely on their own terms."},
            {"title": "Come Alive", "artist": "Janelle Monae", "why": "A song that turns any commute into a movie scene."},
            {"title": "Power", "artist": "Kanye West", "why": "Because you don't enter a room — you arrive."},
        ],
    },
    "the-daydreamer": {
        "name": "The Daydreamer", "emoji": "☁️", "color": "#7F77DD",
        "description": "You hear a song and immediately you're starring in a music video of your own life. You have dozens of unfinished playlists, a soft spot for melancholy bridges, and you feel everything three times more intensely than anyone around you.",
        "anthem": "Liability — Lorde",
        "traits": ["Serial Playlist Maker", "Deep Feeler", "Bridge Obsessive"],
        "artists": ["Lorde", "Frank Ocean", "Lana Del Rey", "SZA"],
        "dna": {"energy": 45, "extroversion": 40, "emotionality": 92},
        "recs": [
            {"title": "Self Control", "artist": "Frank Ocean", "why": "Three minutes of feeling everything at once."},
            {"title": "White Ferrari", "artist": "Frank Ocean", "why": "The song that feels like a memory you haven't made yet."},
            {"title": "Buzzcut Season", "artist": "Lorde", "why": "For when the world feels too loud and too quiet simultaneously."},
        ],
    },
    "the-chill-soul": {
        "name": "The Chill Soul", "emoji": "☕", "color": "#5D8A6E",
        "description": "You are the human equivalent of a Sunday morning. Your music doesn't need to be loud to be felt — it just needs to be real. People gravitate toward your energy because it costs nothing to be around you, and your playlists feel like exhaling.",
        "anthem": "Best Part — Daniel Caesar ft. H.E.R.",
        "traits": ["Comfort Curator", "Slow Burn Appreciator", "Quiet Confidence"],
        "artists": ["Daniel Caesar", "Mac Miller", "H.E.R.", "Jorja Smith"],
        "dna": {"energy": 35, "extroversion": 55, "emotionality": 78},
        "recs": [
            {"title": "Spiked", "artist": "Cautious Clay", "why": "Smooth and warm like a song that fits any afternoon."},
            {"title": "Small Worlds", "artist": "Mac Miller", "why": "Gentle and wise — exactly the kind of music you treasure."},
            {"title": "On and On", "artist": "Erykah Badu", "why": "Timeless soul that rewards patient listening."},
        ],
    },
    "the-global-ear": {
        "name": "The Global Ear", "emoji": "🌍", "color": "#C47A2B",
        "description": "Language is never a barrier for you — it's just another instrument. You had an Afrobeats phase before it went mainstream, you know a Brazilian artist your friends can't pronounce, and your Spotify Wrapped reads like a passport. You don't just listen to music from around the world — you feel it.",
        "anthem": "Essence — Wizkid ft. Tems",
        "traits": ["Culturally Fluent", "Language-Blind Listener", "World Music Pioneer"],
        "artists": ["Wizkid", "Rosalia", "Burna Boy", "Amr Diab"],
        "dna": {"energy": 70, "extroversion": 72, "emotionality": 75},
        "recs": [
            {"title": "Nonku", "artist": "Msaki", "why": "South African soul so beautiful it bypasses language entirely."},
            {"title": "Tuyo", "artist": "Rodrigo Amarante", "why": "You may know it from Narcos — the full album will change you."},
            {"title": "Formidable", "artist": "Stromae", "why": "Belgian French-language pop that rewired how a generation thinks about music."},
        ],
    },
    "the-romantic": {
        "name": "The Romantic", "emoji": "🌹", "color": "#D4537E",
        "description": "You fall in love with songs the way others fall in love with people — completely and suddenly. Every playlist you've ever made is secretly a love letter. You believe deeply in the right song at the right moment.",
        "anthem": "Make You Feel My Love — Adele",
        "traits": ["Emotional Archivist", "Slow Dance Defender", "Lyric Memorizer"],
        "artists": ["Adele", "John Legend", "Giveon", "Sade"],
        "dna": {"energy": 40, "extroversion": 60, "emotionality": 97},
        "recs": [
            {"title": "The Night Will Always Win", "artist": "Manchester Orchestra", "why": "A love song that hits differently at 2am."},
            {"title": "Slow Burn", "artist": "Kacey Musgraves", "why": "For the kind of love that builds quietly and lasts."},
            {"title": "Naked as We Came", "artist": "Iron and Wine", "why": "The most tender song you will hear all year."},
        ],
    },
    "the-old-soul": {
        "name": "The Old Soul", "emoji": "🎷", "color": "#BA7517",
        "description": "You were born in the wrong decade and you've fully accepted it. Vinyl over streaming. The classics are classics for a reason. You can explain in convincing detail exactly why they don't make them like they used to.",
        "anthem": "Whats Going On — Marvin Gaye",
        "traits": ["Vinyl Evangelist", "Time Traveler", "Authenticity Guardian"],
        "artists": ["Marvin Gaye", "Aretha Franklin", "Stevie Wonder", "Bob Dylan"],
        "dna": {"energy": 50, "extroversion": 45, "emotionality": 80},
        "recs": [
            {"title": "Since I Fell for You", "artist": "Nina Simone", "why": "A performance so honest it makes modern music feel manufactured."},
            {"title": "People Get Ready", "artist": "Curtis Mayfield", "why": "Soul music in its purest and most powerful form."},
            {"title": "God Only Knows", "artist": "The Beach Boys", "why": "Widely considered the most perfect song ever written."},
        ],
    },
    "the-hype-beast": {
        "name": "The Hype Beast", "emoji": "🔥", "color": "#E24B4A",
        "description": "If it slaps, you found it first. Your speaker is always at full blast and your energy could power a small city. You live for the drop, the unexpected feature, and the freestyle that breaks the internet.",
        "anthem": "HUMBLE. — Kendrick Lamar",
        "traits": ["First-to-Know", "Volume Maximalist", "Culture Mover"],
        "artists": ["Kendrick Lamar", "Travis Scott", "Bad Bunny", "Central Cee"],
        "dna": {"energy": 97, "extroversion": 88, "emotionality": 50},
        "recs": [
            {"title": "PRIDE.", "artist": "Kendrick Lamar", "why": "The most overlooked track on DAMN. and arguably the deepest."},
            {"title": "Yamborghini High", "artist": "A$AP Mob ft. Juicy J", "why": "Pure sonic aggression. You will understand immediately."},
            {"title": "NEW MAGIC WAND", "artist": "Tyler, The Creator", "why": "Proves Tyler operates on a completely different level."},
        ],
    },
    "the-overthinker": {
        "name": "The Overthinker", "emoji": "🌀", "color": "#378ADD",
        "description": "You've analyzed the bridge of a song you've never even shared with anyone. Music is a language you speak fluently and silently. You remember exactly where you were when you first heard That Song.",
        "anthem": "Skinny Love — Bon Iver",
        "traits": ["Pattern Finder", "Bridge Appreciator", "Emotional Archaeologist"],
        "artists": ["Tame Impala", "Radiohead", "Daft Punk", "Laufey"],
        "dna": {"energy": 55, "extroversion": 38, "emotionality": 88},
        "recs": [
            {"title": "Motion Picture Soundtrack", "artist": "Radiohead", "why": "Ends Kid A with a silence that says more than lyrics could."},
            {"title": "Let Down", "artist": "Radiohead", "why": "The bridge alone is worth the entire runtime."},
            {"title": "Retrograde", "artist": "James Blake", "why": "A song that feels like it is reading your journal."},
        ],
    },
    "the-nostalgist": {
        "name": "The Nostalgist", "emoji": "📼", "color": "#534AB7",
        "description": "A song can teleport you instantly. You have playlists named after specific years, former feelings, and childhood bedrooms. You believe the best music was made in one particular era and you can argue it convincingly.",
        "anthem": "Mr. Brightside — The Killers",
        "traits": ["Memory Keeper", "Era Defender", "Emotional Time Machine"],
        "artists": ["The Killers", "My Chemical Romance", "Arctic Monkeys", "Paramore"],
        "dna": {"energy": 68, "extroversion": 60, "emotionality": 85},
        "recs": [
            {"title": "The Funeral", "artist": "Band of Horses", "why": "Every listen feels like the end of something you loved."},
            {"title": "Lua", "artist": "Bright Eyes", "why": "A song that freezes a specific kind of lonely in amber."},
            {"title": "Such Great Heights", "artist": "The Postal Service", "why": "2003 wrapped into 4 minutes. Sounds like being young."},
        ],
    },
    "the-rebel": {
        "name": "The Rebel", "emoji": "⚡", "color": "#8B2252",
        "description": "You play it loud and you play it proud. You push against the mainstream on principle, and your music taste doubles as an identity statement. You believe every truly great song should feel just a little bit dangerous.",
        "anthem": "Smells Like Teen Spirit — Nirvana",
        "traits": ["Status Quo Disruptor", "Volume at 11", "Art Purist"],
        "artists": ["Nirvana", "Tyler The Creator", "Arctic Monkeys", "Bikini Kill"],
        "dna": {"energy": 88, "extroversion": 65, "emotionality": 60},
        "recs": [
            {"title": "Neighborhood #1 (Tunnels)", "artist": "Arcade Fire", "why": "Anthemic, raw, and completely uncompromising."},
            {"title": "Maps", "artist": "Yeah Yeah Yeahs", "why": "Karen O's vocal alone is an act of rebellion."},
            {"title": "Obstacle 1", "artist": "Interpol", "why": "Cold, angular, and impossible to ignore."},
        ],
    },
    "the-trendsetter": {
        "name": "The Trendsetter", "emoji": "✨", "color": "#0F6E56",
        "description": "You've already moved on from what's currently popular. Your ears are six months in the future. Artists you champion now will be mainstream eventually — and you'll stop listening to them exactly when that happens.",
        "anthem": "Angel — PinkPantheress",
        "traits": ["Taste Pioneer", "Cultural Forecaster", "Hype Resistant"],
        "artists": ["PinkPantheress", "Charli XCX", "JPEGMAFIA", "Little Simz"],
        "dna": {"energy": 75, "extroversion": 70, "emotionality": 60},
        "recs": [
            {"title": "Vroom Vroom", "artist": "Charli XCX", "why": "Told us where pop was going — back in 2016."},
            {"title": "Rebound", "artist": "JPEGMAFIA", "why": "Challenging and brilliant — exactly your speed."},
            {"title": "Venom", "artist": "Little Simz", "why": "Lyrically untouchable. Everything mainstream rap wishes it was."},
        ],
    },
}

GENRE_TO_PERSONA = {
    "Pop": "the-life-of-the-party", "Dance": "the-life-of-the-party",
    "K-Pop": "the-life-of-the-party", "Afrobeats": "the-life-of-the-party",
    "Reggaeton": "the-hype-beast", "Hip-Hop": "the-hype-beast",
    "Trap": "the-hype-beast", "Drill": "the-hype-beast", "Grime": "the-hype-beast",
    "R&B/Pop": "the-main-character", "Pop/R&B": "the-main-character", "Cinematic": "the-main-character",
    "R&B": "the-romantic", "Soul/Pop": "the-romantic", "Ballad": "the-romantic",
    "Lo-fi": "the-chill-soul", "Neo Soul": "the-chill-soul", "Acoustic": "the-chill-soul",
    "Jazz/Pop": "the-chill-soul", "Soul/R&B": "the-chill-soul", "Jazz/R&B": "the-chill-soul",
    "Indie Pop": "the-daydreamer", "Dream Pop": "the-daydreamer", "Electropop": "the-daydreamer",
    "Folk/Pop": "the-daydreamer", "Alt-Pop": "the-daydreamer",
    "Folk/Indie": "the-global-ear", "Shoegaze": "the-global-ear", "Ambient": "the-global-ear",
    "Reggae": "the-global-ear", "Latin": "the-global-ear", "World": "the-global-ear",
    "Arabic": "the-global-ear", "Turkish": "the-global-ear", "Post-rock": "the-global-ear",
    "Classic Rock": "the-old-soul", "Jazz": "the-old-soul", "Blues": "the-old-soul",
    "Motown": "the-old-soul", "Soul/Jazz": "the-old-soul", "Funk/Soul": "the-old-soul",
    "Electronic/Hip-Hop": "the-overthinker", "Progressive": "the-overthinker",
    "Psychedelic Rock": "the-overthinker", "Art Rock": "the-overthinker", "Trip-hop": "the-overthinker",
    "Post-punk": "the-rebel", "Punk Rock": "the-rebel", "Grunge": "the-rebel",
    "Ska": "the-rebel", "Metal": "the-rebel", "Alternative Rock": "the-rebel",
    "2000s Alt": "the-nostalgist", "Pop-Punk": "the-nostalgist",
    "Emo": "the-nostalgist", "Britpop": "the-nostalgist",
    "Hyperpop": "the-trendsetter", "Experimental": "the-trendsetter",
    "Electronic": "the-trendsetter", "UK Rap": "the-trendsetter", "PC Music": "the-trendsetter",
}

QUIZ_QUESTIONS = [
    {
        "question": "Be honest — what does your Spotify Wrapped say about you?",
        "options": [
            ("🎊 Top 0.1% of a festival headliner. I have no regrets.", "the-life-of-the-party", "the-hype-beast"),
            ("🌍 Five different languages, three continents. My friends were confused.", "the-global-ear", "the-daydreamer"),
            ("🎧 Same songs on repeat. I found what works and I stay loyal.", "the-nostalgist", "the-chill-soul"),
            ("🔭 A bunch of artists you've never heard of. That's kind of the point.", "the-trendsetter", "the-overthinker"),
        ]
    },
    {
        "question": "A song comes on shuffle that you completely forgot existed. You:",
        "options": [
            ("💥 Turn it up immediately. This was always a masterpiece.", "the-hype-beast", "the-life-of-the-party"),
            ("😭 Get hit by a memory you were not prepared for.", "the-nostalgist", "the-romantic"),
            ("🧠 Start analyzing why it hit different back then versus now.", "the-overthinker", "the-daydreamer"),
            ("📱 Send it to someone with zero context and wait for their reaction.", "the-life-of-the-party", "the-global-ear"),
        ]
    },
    {
        "question": "The aux cord is yours at a gathering. Your move:",
        "options": [
            ("✅ I had a playlist ready before I even left the house.", "the-trendsetter", "the-main-character"),
            ("😩 I spend too long choosing the opener. The opening track sets the entire tone.", "the-overthinker", "the-daydreamer"),
            ("😤 Play exactly what I want. They'll thank me in five minutes.", "the-rebel", "the-hype-beast"),
            ("🤝 Quick read of the room first — then I build the vibe from what people need.", "the-chill-soul", "the-global-ear"),
        ]
    },
    {
        "question": "Someone says they only listen to music in English. You:",
        "options": [
            ("🤦 Immediately play them something that changes their mind.", "the-global-ear", "the-trendsetter"),
            ("🙂 Respect it — everyone has their comfort zone.", "the-chill-soul", "the-daydreamer"),
            ("🎸 Same energy as someone who only eats one cuisine. Limiting.", "the-rebel", "the-overthinker"),
            ("🤷 Honestly I get it. I'm also very loyal to what I already know.", "the-nostalgist", "the-old-soul"),
        ]
    },
    {
        "question": "Pick the feeling that hits the hardest:",
        "options": [
            ("🙌 An entire crowd screaming the same lyrics at the exact same time.", "the-life-of-the-party", "the-hype-beast"),
            ("💭 A song puts words to something you felt but could never describe.", "the-overthinker", "the-romantic"),
            ("🌍 A track in a language you don't speak, yet you feel every single word.", "the-global-ear", "the-daydreamer"),
            ("⏳ Finding an old record that sounds like it was made for you.", "the-old-soul", "the-nostalgist"),
        ]
    },
    {
        "question": "Your playlist tells a story. What kind?",
        "options": [
            ("🎬 A cinematic rise — from the intro to the moment everything clicks.", "the-main-character", "the-hype-beast"),
            ("📼 A specific era of my life I keep returning to. You had to be there.", "the-nostalgist", "the-old-soul"),
            ("🌐 No theme, no genre, no rules. Every track is from a different world.", "the-global-ear", "the-daydreamer"),
            ("🎼 A carefully mapped emotional arc. The order is not random.", "the-overthinker", "the-romantic"),
        ]
    },
    {
        "question": "How do you actually find new music?",
        "options": [
            ("📱 The algorithm, niche feeds, and internet rabbit holes. I stay plugged in.", "the-trendsetter", "the-hype-beast"),
            ("🌙 Late-night Spotify spirals where one artist leads to ten more.", "the-overthinker", "the-daydreamer"),
            ("🌍 Friends, YouTube deep dives, discoveries abroad.", "the-global-ear", "the-daydreamer"),
            ("📻 Record stores, old interviews, and recommendations from people with niche taste.", "the-old-soul", "the-nostalgist"),
        ]
    },
    {
        "question": "A friend asks you to describe your music taste in one sentence:",
        "options": [
            ("🔥 Whatever's mainstream right now? You definitely know my top played from 6 months ago.", "the-trendsetter", "the-hype-beast"),
            ("☕ Warm, real, and nothing that requires explaining.", "the-chill-soul", "the-romantic"),
            ("🌍 Honestly it's easier to tell you what I don't listen to.", "the-global-ear", "the-daydreamer"),
            ("🌀 I'd need a whiteboard, a timeline, and 20 minutes.", "the-overthinker", "the-daydreamer"),
        ]
    },
    {
        "question": "What does music actually do for you?",
        "options": [
            ("⚡ It's fuel. I can't function at full capacity without it.", "the-hype-beast", "the-life-of-the-party"),
            ("🕰️ It's a time machine. One song and I'm instantly somewhere specific.", "the-nostalgist", "the-romantic"),
            ("🌍 It's a passport. Music takes me to places I've never physically been.", "the-global-ear", "the-daydreamer"),
            ("🧭 It's therapy. It helps me figure out what I'm actually feeling.", "the-overthinker", "the-chill-soul"),
        ]
    },
    {
        "question": "Pick the concert experience that's actually you:",
        "options": [
            ("🏟️ Front row, every lyric memorized, completely unhinged in the best way.", "the-life-of-the-party", "the-hype-beast"),
            ("🌍 A festival where half the artists are from scenes I have never heard before.", "the-global-ear", "the-daydreamer"),
            ("🎭 Intimate venue, fifty people, artist plays something unreleased.", "the-romantic", "the-overthinker"),
            ("🎧 Studio album with headphones. Live versions can ruin the magic.", "the-nostalgist", "the-old-soul"),
        ]
    },
    {
        "question": "If you could be born into any musical era, which would you choose?",
        "options": [
            ("📻 Pre-1950s. Jazz clubs, big bands, a time when musicians were treated like royalty.", "the-old-soul", "the-romantic"),
            ("🕰️ The 60s-70s. Woodstock, Motown, the birth of everything. I would have been right there.", "the-old-soul", "the-nostalgist"),
            ("🌃 The 80s-90s. When genres were exploding and nothing felt polished yet.", "the-nostalgist", "the-rebel"),
            ("🚀 Right now. No other era has had access to this much music from everywhere at once.", "the-global-ear", "the-daydreamer"),
        ]
    },
]

GENRE_PROFILES = {
    "Rock": {"energy": 3, "extroversion": 2, "emotionality": 1},
    "Rock/Pop": {"energy": 2, "extroversion": 3, "emotionality": 2},
    "Pop": {"energy": 2, "extroversion": 3, "emotionality": 2},
    "Hip-Hop": {"energy": 3, "extroversion": 3, "emotionality": 2},
    "R&B": {"energy": 1, "extroversion": 2, "emotionality": 3},
    "Soul": {"energy": 1, "extroversion": 2, "emotionality": 3},
    "Jazz": {"energy": 1, "extroversion": 1, "emotionality": 3},
    "Classical": {"energy": 1, "extroversion": 1, "emotionality": 3},
    "Electronic": {"energy": 3, "extroversion": 3, "emotionality": 1},
    "Metal": {"energy": 3, "extroversion": 1, "emotionality": 2},
    "Country": {"energy": 2, "extroversion": 2, "emotionality": 3},
    "Folk": {"energy": 1, "extroversion": 1, "emotionality": 3},
    "Latin": {"energy": 3, "extroversion": 3, "emotionality": 2},
}

PERSONA_ANIMATIONS = {
    "the-life-of-the-party": {"items": ["🎉","✨","🎊","✨","🎉","🥳","🎊","✨","🎉"], "anim": "partyFall", "dir": "top"},
    "the-main-character":    {"items": ["⭐","✨","🌟","✨","⭐","🌟","✨","⭐","🌟"], "anim": "mainTwinkle", "dir": "fixed"},
    "the-daydreamer":        {"items": ["☁️","✨","☁️","🌙","☁️","✨","☁️","🌙","☁️"], "anim": "dreamDrift", "dir": "left"},
    "the-chill-soul":        {"items": ["🍃","☕","✨","🍃","🌿","✨","☕","🍃","✨"], "anim": "chillFloat", "dir": "bottom"},
    "the-global-ear":        {"items": ["🌍","✈️","🌐","🎵","🌍","✈️","🌐","🎵","🌍"], "anim": "globalFloat", "dir": "bottom"},
    "the-romantic":          {"items": ["💖","🦋","💕","✨","💗","🦋","💖","💕","✨"], "anim": "romanticRise", "dir": "bottom"},
    "the-old-soul":          {"items": ["🎷","📻","🎶","✨","🎷","📻","🎶","✨","🎷"], "anim": "oldSoulSway", "dir": "fixed"},
    "the-hype-beast":        {"items": ["🔥","⚡","💥","🔥","⚡","💥","🔥","⚡","💥"], "anim": "hypeFall", "dir": "top"},
    "the-overthinker":       {"items": ["🌀","🌙","💭","✨","🌀","🌙","💭","✨","🌀"], "anim": "thinkSpin", "dir": "fixed"},
    "the-nostalgist":        {"items": ["📼","💿","🕰️","✨","📼","💿","🕰️","✨","📼"], "anim": "nostalgiaFade", "dir": "fixed"},
    "the-rebel":             {"items": ["⚡","🔥","🎸","⚡","🔥","🎸","⚡","🔥","🎸"], "anim": "rebelCrash", "dir": "top"},
    "the-trendsetter":       {"items": ["✨","🚀","💿","⚡","✨","🪩","🚀","✨","💿"], "anim": "trendRise", "dir": "bottom"},
}

POSITIONS = [
    ("8%","6%"),("15%","82%"),("28%","18%"),("44%","72%"),("60%","35%"),
    ("72%","88%"),("38%","55%"),("82%","20%"),("50%","92%")
]

# ============================================================
# TOPIC 1 — PERSON 1: DATA LOADING
# ============================================================
def load_artist_data(filepath):
    df = pd.read_excel(filepath)
    artist_data = {}
    # Handle both column name formats
    artist_col = "Artist" if "Artist" in df.columns else df.columns[1]
    genre_col = "Genre" if "Genre" in df.columns else df.columns[2]
    country_col = "Country" if "Country" in df.columns else df.columns[3]
    for _, row in df.iterrows():
        artist = str(row[artist_col]).strip().lower()
        artist_data[artist] = {
            "name":    str(row[artist_col]).strip(),
            "genre":   str(row[genre_col]).strip(),
            "country": str(row[country_col]).strip(),
        }
    return artist_data

# ============================================================
# TOPIC 2 — FLOW CONTROL: PERSON 2 SEARCH LOGIC
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
    else:
        return "Artist not found. Please try again."

# ============================================================
# TOPIC 3 — FUNCTIONS: PERSON 3 CORE LOGIC
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
    """Function 3: Build a personality profile from a list of artist names."""
    profile = {"energy": 0, "extroversion": 0, "emotionality": 0}
    found_count = 0
    for name in artist_names:
        result = search_artist(name, data)
        if isinstance(result, dict):
            genre = result.get("genre", "")
            found_count += 1
            if genre in GENRE_PROFILES:
                for key in profile:
                    profile[key] += GENRE_PROFILES[genre][key]
            else:
                profile["energy"] += 1
                profile["extroversion"] += 1
                profile["emotionality"] += 1
    return profile, found_count

def genre_to_persona_id(genre):
    """Function 4: Map a genre string to a persona ID."""
    for key, pid in GENRE_TO_PERSONA.items():
        if key.lower() in genre.lower():
            return pid
    return "the-daydreamer"

def merge_and_decide(artist_scores, quiz_scores):
    """Function 5: Combine artist scores (40%) and quiz scores (60%)."""
    all_ids = set(list(artist_scores.keys()) + list(quiz_scores.keys()))
    final = {}
    for pid in all_ids:
        a = artist_scores.get(pid, 0)
        q = quiz_scores.get(pid, 0)
        final[pid] = (a * 0.4) + (q * 0.6)
    if final:
        return max(final, key=final.get)
    else:
        return "the-daydreamer"

def format_result(persona_id):
    """Function 6: Return a formatted result string."""
    p = PERSONA_DETAILS.get(persona_id, PERSONA_DETAILS["the-daydreamer"])
    return f"{p['emoji']} {p['name']}: {p['description']}"

# ============================================================
# TOPIC 4 — CLASSES: PERSON 4 MusicPersona CLASS
# ============================================================
class MusicPersona:
    """Represents a user's music personality result."""
    def __init__(self, persona_id, artist_names_found):
        p = PERSONA_DETAILS.get(persona_id, PERSONA_DETAILS["the-daydreamer"])
        self.persona_id     = persona_id
        self.name           = p["name"]
        self.emoji          = p["emoji"]
        self.description    = p["description"]
        self.anthem         = p["anthem"]
        self.traits         = p["traits"]
        self.color          = p["color"]
        self.artists        = p["artists"]
        self.dna            = p["dna"]
        self.recs           = p.get("recs", [])
        self.artist_sources = artist_names_found

    def get_traits_string(self):
        """Method: returns traits joined as a readable string."""
        return " · ".join(self.traits)

    def get_share_text(self):
        """Method: returns a copyable text summary for sharing."""
        return "\n".join([
            "My music persona is " + self.name + " " + self.emoji,
            "",
            self.description,
            "",
            "My anthem: " + self.anthem,
            "",
            "My traits: " + self.get_traits_string(),
            "",
            "Find yours at yourlifeasaplaylist.streamlit.app",
        ])

    def __repr__(self):
        return f"MusicPersona(name={self.name!r})"


# ── Card generator ─────────────────────────────────────────────────────────────
def clean_text(text):
    """Replace unicode characters that PIL fonts may not render."""
    replacements = {
        "\u2014": "-", "\u2013": "-", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"', "\u2026": "...",
    }
    for char, rep in replacements.items():
        text = text.replace(char, rep)
    return text

def render_emoji_img(emoji_char, target_size=88):
    """Render a single emoji to an RGBA PIL Image using NotoColorEmoji."""
    font_path = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
    if not os.path.exists(font_path):
        return None
    attempts = []
    try:
        attempts.append({"size": 109, "layout_engine": ImageFont.Layout.RAQM})
    except Exception:
        pass
    attempts += [{"size": 109}, {"size": 72}, {"size": 64}]
    for kw in attempts:
        try:
            font = ImageFont.truetype(font_path, **kw)
            canvas_size = kw["size"] * 2
            tmp = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
            d = ImageDraw.Draw(tmp)
            d.text((kw["size"] // 4, kw["size"] // 4), emoji_char, font=font, embedded_color=True)
            bbox = tmp.getbbox()
            if bbox and (bbox[2] - bbox[0]) > 4 and (bbox[3] - bbox[1]) > 4:
                return tmp.crop(bbox).resize((target_size, target_size), Image.LANCZOS)
        except Exception:
            continue
    return None

def generate_persona_card(persona):
    """Generate a downloadable PNG result card."""
    def hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    def blend(color, bg, alpha):
        return tuple(int(bg[i] * (1-alpha) + color[i] * alpha) for i in range(3))
    def wrap_text(draw, text, font, max_width):
        words = text.split()
        lines, line = [], ""
        for w in words:
            test = (line + " " + w).strip()
            if draw.textlength(test, font=font) < max_width:
                line = test
            else:
                if line: lines.append(line)
                line = w
        if line: lines.append(line)
        return lines

    W, H = 900, 1120
    accent = hex_to_rgb(persona.color)
    bg_dark, bg_mid = (15, 12, 41), (48, 43, 99)

    img = Image.new("RGBA", (W, H), bg_dark)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        draw.line([(0, y), (W, y)], fill=(
            int(bg_dark[0]*(1-t)+bg_mid[0]*t),
            int(bg_dark[1]*(1-t)+bg_mid[1]*t),
            int(bg_dark[2]*(1-t)+bg_mid[2]*t), 255))

    pad = 56
    draw.rounded_rectangle([pad, pad, W-pad, H-pad], radius=32,
        fill=(*blend(accent, bg_dark, 0.14), 255), outline=(*accent, 110), width=2)
    draw.rounded_rectangle([pad, pad, W-pad, pad+7], radius=3, fill=(*accent, 255))

    def try_font(path, size):
        try: return ImageFont.truetype(path, size)
        except: return ImageFont.load_default()

    poppins     = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
    poppins_reg = "/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf"
    poppins_med = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
    lora        = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"

    f_label  = try_font(poppins, 15)
    f_name   = try_font(lora, 58)
    f_name_s = try_font(lora, 44)
    f_body   = try_font(poppins_reg, 24)
    f_traits = try_font(poppins_med, 22)
    f_small  = try_font(poppins_reg, 19)
    f_tiny   = try_font(poppins_reg, 16)

    cx = W // 2
    MUTED = (190, 190, 210, 255)
    DIMMED = (120, 120, 145, 255)

    card_name   = clean_text(persona.name)
    card_desc   = clean_text(persona.description)
    card_anthem = clean_text(persona.anthem)
    card_traits = [clean_text(t) for t in persona.traits]

    lbl = "YOUR LIFE AS A PLAYLIST"
    lw = draw.textlength(lbl, font=f_label)
    draw.text(((W-lw)//2, 100), lbl, fill=(*accent, 200), font=f_label)
    draw.line([(cx-70, 136), (cx+70, 136)], fill=(*accent, 70), width=1)

    emoji_img = render_emoji_img(persona.emoji, target_size=88)
    emoji_y = 158
    if emoji_img:
        img.paste(emoji_img, ((W - emoji_img.width) // 2, emoji_y), emoji_img)
        name_y = emoji_y + emoji_img.height + 18
    else:
        draw.text((cx-20, emoji_y+10), persona.emoji, fill=(*accent, 200), font=f_name_s)
        name_y = emoji_y + 96

    name_font = f_name
    nw = draw.textlength(card_name, font=name_font)
    if nw > W - 160:
        name_font = f_name_s
        nw = draw.textlength(card_name, font=name_font)
    draw.text(((W-nw)//2, name_y), card_name, fill=(*accent, 255), font=name_font)

    desc_y = name_y + 74
    for line in wrap_text(draw, card_desc, f_body, W-200)[:5]:
        lw2 = draw.textlength(line, font=f_body)
        draw.text(((W-lw2)//2, desc_y), line, fill=MUTED, font=f_body)
        desc_y += 36

    ay = desc_y + 24
    draw.rounded_rectangle([pad+44, ay, W-pad-44, ay+66], radius=14,
        fill=(*blend(accent, (0,0,0), 0.20), 255), outline=(*accent, 65), width=1)
    anthem_str = "Your anthem:  " + card_anthem
    aw = draw.textlength(anthem_str, font=f_small)
    draw.text(((W-aw)//2, ay+20), anthem_str, fill=(*accent, 230), font=f_small)

    ty = ay + 94
    traits_str = "  -  ".join(card_traits)
    tw = draw.textlength(traits_str, font=f_traits)
    draw.text(((W-tw)//2, ty), traits_str, fill=MUTED, font=f_traits)

    dna_y = ty + 68
    bar_x, bar_w = pad + 72, W - (pad + 72) * 2
    for i, (lbl2, val) in enumerate([("Energy", persona.dna["energy"]), ("Extroversion", persona.dna["extroversion"]), ("Emotionality", persona.dna["emotionality"])]):
        yb = dna_y + i * 56
        draw.text((bar_x, yb), lbl2, fill=DIMMED, font=f_tiny)
        pct = str(val) + "%"
        pw = draw.textlength(pct, font=f_tiny)
        draw.text((bar_x + bar_w - pw, yb), pct, fill=(*accent, 220), font=f_tiny)
        draw.rounded_rectangle([bar_x, yb+24, bar_x+bar_w, yb+40], radius=6, fill=(255,255,255,22))
        fw2 = max(12, int(bar_w * val / 100))
        draw.rounded_rectangle([bar_x, yb+24, bar_x+fw2, yb+40], radius=6, fill=(*accent, 255))

    note_y = dna_y + 3*56 + 10
    if persona.artist_sources:
        src = "Based on: " + ", ".join(persona.artist_sources)
        sw = draw.textlength(src, font=f_tiny)
        draw.text(((W-sw)//2, note_y), src, fill=DIMMED, font=f_tiny)

    fy = H - pad - 42
    draw.line([(cx-110, fy), (cx+110, fy)], fill=(255,255,255,28), width=1)
    footer = "yourlifeasaplaylist.streamlit.app"
    fw3 = draw.textlength(footer, font=f_tiny)
    draw.text(((W-fw3)//2, fy+13), footer, fill=DIMMED, font=f_tiny)

    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="PNG", dpi=(144,144))
    buf.seek(0)
    return buf.getvalue()


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
            pos = "top:-10%;left:" + str(10 + i*10) + "%;"
        elif anim["dir"] == "bottom":
            pos = "bottom:-80px;left:" + str(5 + i*10) + "%;"
        elif anim["dir"] == "left":
            top, _ = POSITIONS[i]
            pos = "top:" + top + ";left:-15%;"
        else:
            top, left = POSITIONS[i]
            pos = "top:" + top + ";left:" + left + ";"
        items_html += (
            '<div style="position:absolute;' + pos + 'font-size:1.8rem;opacity:0;'
            'animation:' + anim["anim"] + " " + str(duration) + "s ease-in-out " + str(delay) + 's infinite;">'
            + item + '</div>'
        )
    st.markdown(
        '<div id="' + uid + '_layer" style="position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;overflow:hidden;z-index:999;">'
        + items_html + '</div>',
        unsafe_allow_html=True
    )

def dna_bar(label, value, color):
    return (
        '<div style="margin-bottom:0.9rem;">'
        '<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
        '<span style="font-size:0.82rem;color:rgba(255,255,255,0.7);">' + label + '</span>'
        '<span style="font-size:0.82rem;color:' + color + ';font-weight:600;">' + str(value) + '%</span>'
        '</div>'
        '<div style="background:rgba(255,255,255,0.1);border-radius:50px;height:8px;overflow:hidden;">'
        '<div style="width:' + str(value) + '%;background:linear-gradient(90deg,' + color + '88,' + color + ');height:100%;border-radius:50px;"></div>'
        '</div></div>'
    )

def restart():
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
.dot.active{background:white;}.dot.done{background:rgba(255,255,255,0.55);}
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
.stProgress>div>div{background:rgba(255,255,255,0.1)!important;border-radius:10px!important;}
.stProgress>div>div>div{background:linear-gradient(90deg,#a78bfa,#f472b6)!important;border-radius:10px!important;}
@keyframes partyFall{0%{transform:translateY(0) rotate(0deg);opacity:0}10%{opacity:0.35}90%{opacity:0.2}100%{transform:translateY(110vh) rotate(360deg);opacity:0}}
@keyframes mainTwinkle{0%,100%{transform:scale(0.7);opacity:0.05}50%{transform:scale(1.3);opacity:0.3}}
@keyframes dreamDrift{0%{transform:translateX(0);opacity:0}8%{opacity:0.25}90%{opacity:0.15}100%{transform:translateX(125vw);opacity:0}}
@keyframes chillFloat{0%{transform:translateY(0);opacity:0}12%{opacity:0.5}85%{opacity:0.25}100%{transform:translateY(-115vh);opacity:0}}
@keyframes globalFloat{0%{transform:translateY(0) rotate(0deg);opacity:0}10%{opacity:0.35}100%{transform:translateY(-115vh) rotate(20deg);opacity:0}}
@keyframes romanticRise{0%{transform:translateY(0);opacity:0}15%{opacity:0.35}100%{transform:translateY(-115vh);opacity:0}}
@keyframes oldSoulSway{0%,100%{transform:rotate(-8deg) scale(0.85);opacity:0.05}50%{transform:rotate(8deg) scale(1.1);opacity:0.22}}
@keyframes hypeFall{0%{transform:translateY(0) rotate(0deg) scale(0.8);opacity:0}8%{opacity:0.4}90%{opacity:0.25}100%{transform:translateY(110vh) rotate(720deg) scale(1.2);opacity:0}}
@keyframes thinkSpin{0%,100%{transform:rotate(0deg) scale(0.8);opacity:0.04}50%{transform:rotate(360deg) scale(1.2);opacity:0.25}}
@keyframes nostalgiaFade{0%,100%{transform:scale(0.85) rotate(-5deg);opacity:0.04}50%{transform:scale(1.1) rotate(5deg);opacity:0.22}}
@keyframes rebelCrash{0%{transform:translateY(0) rotate(0deg);opacity:0}6%{opacity:0.38}88%{opacity:0.2}100%{transform:translateY(110vh) rotate(180deg);opacity:0}}
@keyframes trendRise{0%{transform:translateY(0) scale(0.7);opacity:0}10%{opacity:0.5}100%{transform:translateY(-115vh) scale(1.2);opacity:0}}
footer{visibility:hidden;}#MainMenu{visibility:hidden;}header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
defaults = {
    "step": "intro", "artist_scores": {}, "quiz_scores": {},
    "quiz_step": 0, "artist_names_found": [], "celebrated": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

@st.cache_data
def get_data():
    return load_data("database_artists.xlsx")

data = get_data()

# ── INTRO ──────────────────────────────────────────────────────────────────────
if st.session_state.step == "intro":
    st.markdown('<div class="hero-title">🎵 SoundPrint 🎵</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Your Music Taste Has a Signature.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="intro-stat"><div class="intro-stat-num">12</div><div class="intro-stat-label">possible personas</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="intro-stat"><div class="intro-stat-num">11</div><div class="intro-stat-label">quiz questions</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="intro-stat"><div class="intro-stat-num">1000+</div><div class="intro-stat-label">artists in our database</div></div>', unsafe_allow_html=True)

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
            Answer 11 questions about how you experience music.<br>
            We combine both to reveal your true music identity.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Let's find my sound →", use_container_width=True):
        st.session_state.step = "artists"
        st.rerun()

# ── STEP 1: ARTISTS ────────────────────────────────────────────────────────────
elif st.session_state.step == "artists":
    st.markdown('<div class="hero-title">🎵 Your Life<br>as a Playlist</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">Step 1 of 2 — Your top artists</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="question-card">
        <div class="question-text">Which artists define your soundtrack?</div>
        <div style="font-size:0.9rem;color:rgba(255,255,255,0.5);margin-top:0.5rem;">Enter up to 3. At least 1 is required.</div>
    </div>
    """, unsafe_allow_html=True)

    artist1 = st.text_input("Artist #1", placeholder="e.g. Amr Diab")
    artist2 = st.text_input("Artist #2 (optional)", placeholder="e.g. Kendrick Lamar")
    artist3 = st.text_input("Artist #3 (optional)", placeholder="e.g. Lorde")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Next — Take the quiz →", use_container_width=True):
        artists = [a for a in [artist1, artist2, artist3] if a.strip()]
        if not artists:
            st.warning("Please enter at least one artist.")
        else:
            artist_scores = {}
            found_names = []
            for name in artists:
                result = search_artist(name, data)
                if isinstance(result, dict):
                    pid = genre_to_persona_id(result.get("genre", ""))
                    artist_scores[pid] = artist_scores.get(pid, 0) + 3
                    found_names.append(name)
            if not found_names:
                st.error("None of those artists were found. Try checking the spelling.")
                st.stop()
            else:
                st.session_state.artist_scores = artist_scores
                st.session_state.artist_names_found = found_names
                st.session_state.step = "quiz"
                st.rerun()

# ── STEP 2: QUIZ ───────────────────────────────────────────────────────────────
elif st.session_state.step == "quiz":
    q_idx = st.session_state.quiz_step
    total = len(QUIZ_QUESTIONS)

    st.markdown('<div class="hero-title">🎵 Your Life<br>as a Playlist</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="step-badge">Step 2 of 2 — Question ' + str(q_idx+1) + ' of ' + str(total) + '</div>',
        unsafe_allow_html=True
    )

    dots = "".join([
        '<div class="dot ' + ("done" if i < q_idx else "active" if i == q_idx else "") + '"></div>'
        for i in range(total)
    ])
    st.markdown('<div class="progress-dots">' + dots + '</div>', unsafe_allow_html=True)
    st.progress(q_idx / total)

    q = QUIZ_QUESTIONS[q_idx]
    st.markdown('<div class="question-card"><div class="question-text">' + q["question"] + '</div></div>', unsafe_allow_html=True)

    for i, (option_text, p1, p2) in enumerate(q["options"]):
        if st.button(option_text, key="q" + str(q_idx) + "_opt" + str(i), use_container_width=True):
            st.session_state.quiz_scores[p1] = st.session_state.quiz_scores.get(p1, 0) + 2
            st.session_state.quiz_scores[p2] = st.session_state.quiz_scores.get(p2, 0) + 1
            if q_idx + 1 >= total:
                st.session_state.step = "loading"
            else:
                st.session_state.quiz_step += 1
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Start over"):
        restart()
        st.rerun()

# ── LOADING ────────────────────────────────────────────────────────────────────
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
        placeholder.markdown(
            '<div class="loading-screen">'
            '<div style="font-size:3.5rem;margin-bottom:1rem;">' + emoji + '</div>'
            '<div class="loading-msg">' + msg + '</div>'
            '<div class="loading-dots"><div class="loading-dot"></div><div class="loading-dot"></div><div class="loading-dot"></div></div>'
            '</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.9)
    placeholder.empty()
    st.session_state.step = "result"
    st.rerun()

# ── RESULT ─────────────────────────────────────────────────────────────────────
elif st.session_state.step == "result":

    persona_id = merge_and_decide(st.session_state.artist_scores, st.session_state.quiz_scores)
    persona = MusicPersona(persona_id=persona_id, artist_names_found=st.session_state.artist_names_found)

    if not st.session_state.celebrated:
        if persona.persona_id in ("the-life-of-the-party", "the-hype-beast"):
            st.balloons()
        elif persona.persona_id == "the-daydreamer":
            st.snow()
        st.session_state.celebrated = True

    render_persona_animation(persona.persona_id)

    traits_html = "".join(['<span class="trait-pill">' + t + '</span>' for t in persona.traits])
    artist_note = ""
    if persona.artist_sources:
        artist_note = '<p style="opacity:0.6;font-size:0.82rem;margin-top:1.2rem;">Based on: ' + ", ".join(persona.artist_sources) + ' — combined with your quiz answers.</p>'

    st.markdown('<div class="hero-title">🎵 Your Result</div>', unsafe_allow_html=True)

    # 0. Download card expander at top
    with st.expander("📸 Download your result card"):
        card_bytes = generate_persona_card(persona)
        card_img = Image.open(io.BytesIO(card_bytes))
        st.image(card_img, use_container_width=True)
        st.download_button(
            label="⬇️ Download PNG",
            data=card_bytes,
            file_name="my-music-persona-" + persona.persona_id + ".png",
            mime="image/png",
            use_container_width=True,
            key="dl_top",
        )

    # 1. Main result card
    st.markdown(
        '<div class="result-card" style="background:linear-gradient(135deg,' + persona.color + '22,' + persona.color + '44);border:2px solid ' + persona.color + '55;">'
        '<span class="result-emoji">' + persona.emoji + '</span>'
        '<div class="result-name" style="color:' + persona.color + ';">' + persona.name + '</div>'
        '<div class="result-desc" style="color:white;">' + persona.description + '</div>'
        '<div class="anthem-box" style="color:' + persona.color + ';">🎶 Your anthem: <strong>' + persona.anthem + '</strong></div>'
        '<div>' + traits_html + '</div>'
        + artist_note +
        '</div>',
        unsafe_allow_html=True
    )

    # 2. Music DNA
    st.markdown('<div class="section-title">🧬 Your Music DNA</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:1.5rem;">'
        + dna_bar("Energy", persona.dna["energy"], persona.color)
        + dna_bar("Extroversion", persona.dna["extroversion"], persona.color)
        + dna_bar("Emotionality", persona.dna["emotionality"], persona.color)
        + '</div>',
        unsafe_allow_html=True
    )

    # 3. Artists you would vibe with
    st.markdown('<div class="section-title">🎤 Artists you would vibe with</div>', unsafe_allow_html=True)
    artists_html = "".join(['<span class="artist-chip">♪ ' + a + '</span>' for a in persona.artists])
    st.markdown('<div style="text-align:center;">' + artists_html + '</div>', unsafe_allow_html=True)

    # 4. Song recommendations
    st.markdown('<div class="section-title">🎧 Songs you might not know yet</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.85rem;color:rgba(255,255,255,0.45);margin-bottom:1rem;">Three picks curated specifically for your persona.</p>', unsafe_allow_html=True)
    for rec in persona.recs:
        st.markdown(
            '<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-left:3px solid ' + persona.color + ';border-radius:12px;padding:1rem 1.25rem;margin-bottom:0.6rem;">'
            '<div style="font-weight:600;color:white;font-size:0.95rem;">' + rec["title"] + '</div>'
            '<div style="color:' + persona.color + ';font-size:0.85rem;margin:2px 0 6px 0;">' + rec["artist"] + '</div>'
            '<div style="color:rgba(255,255,255,0.5);font-size:0.82rem;font-style:italic;">' + rec["why"] + '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    # 5. Take it again
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Take it again", use_container_width=True):
        restart()
        st.rerun()
