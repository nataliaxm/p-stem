from google import genai
import pandas as pd
import json
import os
import sys
import numpy as np

# =========================
# 1. SETUP
# =========================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("\n[!] ERROR: GEMINI_API_KEY not found")
    sys.exit(1)

client = genai.Client(api_key=api_key)

LLM_MODEL = "models/gemini-2.5-flash"
EMBED_MODEL = "models/gemini-embedding-001"

CACHE_FILE = "rso_embeddings.pkl"


# =========================
# 2. UTILITIES
# =========================

def cosine(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) + 1e-8) / (np.linalg.norm(b) + 1e-8)


def build_user_text(interests, goal, vibe):
    return f"""
User Interests: {interests}
Primary Goal: {goal}
Preferred Vibe: {vibe}
"""


# =========================
# 3. BATCH EMBEDDING (FIXED)
# =========================

def batch_embed(texts, batch_size=100):
    embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        response = client.models.embed_content(
            model=EMBED_MODEL,
            contents=batch
        )

        embeddings.extend([e.values for e in response.embeddings])

    return embeddings


# =========================
# 4. MAIN APP
# =========================

def run_maroon_matcher():

    print("\n" + "=" * 55)
    print("   MAROON MATCHER: UCHICAGO RSO ENGINE (V5)")
    print("=" * 55)

    # -------------------------
    # USER INPUT
    # -------------------------
    print("\n--- TELL US ABOUT YOURSELF ---")

    interests = input("[?] Interests (full sentence): ")
    goal = input("[?] Goal (Professional / Social / Service): ")
    vibe = input("[?] Vibe (Chill / Competitive / Creative): ")

    user_text = build_user_text(interests, goal, vibe)

    # -------------------------
    # LOAD DATA
    # -------------------------
    print("\n[System] Loading RSO directory...")

    try:
        df = pd.read_csv("UChicago_RSO_Directory.csv")

        df["search_blob"] = (
            df["RSO Name"].fillna("") + " " +
            df["Category"].fillna("") + " " +
            df["Description"].fillna("")
        )

    except FileNotFoundError:
        print("CSV not found.")
        return

    # -------------------------
    # EMBEDDINGS (CACHE SAFE)
    # -------------------------
    print("[System] Processing embeddings...")

    if os.path.exists(CACHE_FILE):
        print("[System] Loading cached embeddings...")
        df = pd.read_pickle(CACHE_FILE)

    else:
        print("[System] Generating embeddings in batches...")

        df["embedding"] = batch_embed(df["search_blob"].tolist())

        df.to_pickle(CACHE_FILE)

    # -------------------------
    # USER EMBEDDING
    # -------------------------
    user_emb = client.models.embed_content(
        model=EMBED_MODEL,
        contents=user_text
    ).embeddings[0].values

    # -------------------------
    # SIMILARITY SCORING
    # -------------------------
    df["score"] = df["embedding"].apply(lambda x: cosine(x, user_emb))

    # -------------------------
    # PRE-FILTER TOP CANDIDATES
    # -------------------------
    filtered = df.sort_values("score", ascending=False).head(200)
    top = filtered.head(20)

    rso_data = top[[
        "RSO Name",
        "Category",
        "Description",
        "Blueprint URL"
    ]].to_dict(orient="records")

    # -------------------------
    # GEMINI RERANK
    # -------------------------
    print("[System] Running AI ranking...")

    prompt = f"""
You are a UChicago RSO recommendation engine.

User Profile:
{user_text}

Candidate RSOs:
{json.dumps(rso_data, indent=2)}

TASK:
- Rank top 10 RSOs
- Score each 0–100 based ONLY on semantic fit
- Focus on: interests, social fit, vibe
- Do NOT use popularity assumptions

Return STRICT JSON:

[
  {{
    "name": "...",
    "percentage": 0,
    "reason": "...",
    "url": "..."
  }}
]
"""

    try:
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=prompt
        )

        raw = response.text.strip()

        if "```" in raw:
            raw = raw.split("```")[1].replace("json", "").strip()

        matches = json.loads(raw)

    except Exception as e:
        print(f"\n[!] Gemini ranking failed: {e}")
        return

    # -------------------------
    # OUTPUT
    # -------------------------
    print("\n" + "⭐ YOUR TOP MATCHES ⭐".center(55, "="))

    for i, rso in enumerate(matches[:5], 1):
        print(f"\n{i}. {rso['name']} | {rso['percentage']}% Match")
        print(f"   {rso['reason']}")
        print(f"   {rso['url']}")

    print("\n" + " Honorable Mentions ".center(55, "-"))

    for rso in matches[5:10]:
        print(f" • {rso['name']} ({rso['percentage']}%)")

    print("\n" + "=" * 55)
    print("Success! Find your people.")


# =========================
# RUN
# =========================

if __name__ == "__main__":
    run_maroon_matcher()