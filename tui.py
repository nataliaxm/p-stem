from google import genai
import pandas as pd
import json
import os
import sys

# 1. SECURE KEY ACCESS
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("\n[!] ERROR: GEMINI_API_KEY not found in environment.")
    print("    Run: export GEMINI_API_KEY='AIzaSyB5VG9chjYcl7eSlrl0NIPOPz0sgYqRU60'")
    sys.exit(1)

# Initialize Client
client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-2.0-flash" 

def run_maroon_matcher():
    print("\n" + "="*45)
    print("       MAROON MATCHER: UCHICAGO RSO ENGINE")
    print("="*45)

    # 2. GATHER USER INPUT
    print("\n--- TELL US ABOUT YOURSELF ---")
    interests = input("[?] Interests/Hobbies (e.g., Coding, Jazz, Sports): ")
    goals = input("[?] Primary Goal (Professional / Social / Service): ")
    vibe = input("[?] Preferred Vibe (Chill / Competitive / Creative): ")

    user_profile = {
        "interests": interests,
        "goals": goals,
        "vibe": vibe
    }

    # 3. READ RSO DATA
    print("\n[System] Parsing UChicago RSO Directory...")
    try:
        df = pd.read_csv("UChicago_RSO_Directory.csv")
        rso_summary = df[['RSO Name', 'Category', 'Description', 'Blueprint URL']].to_string(index=False)
    except FileNotFoundError:
        print("Error: UChicago_RSO_Directory.csv not found in this directory!")
        return
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # 4. THE AI LOGIC
    print("[System] Analyzing community asymmetries...")
    
    prompt = f"""
    You are a UChicago Student Life Advisor. 
    User Profile: {json.dumps(user_profile)}
    
    RSO Directory:
    {rso_summary}

    TASK:
    1. Match the user to the top 10 RSOs from the directory.
    2. Rank them by "percentage" (0-100) based on their profile.
    3. Return strictly a JSON list of objects.
    
    JSON Format:
    [
      {{"name": "RSO Name", "percentage": 95, "reason": "1-sentence why", "url": "link"}},
      ...
    ]
    """

    try:
        # Call Gemini 2.0 API
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        
        raw_text = response.text.strip()
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
        matches = json.loads(raw_text)

        # 5. OUTPUT RESULTS
        print("\n" + "⭐ YOUR TOP 5 MATCHES ".center(45, "="))
        for i, rso in enumerate(matches[:5], 1):
            print(f"\n{i}. {rso['name']} | {rso['percentage']}% Match")
            print(f"   Context: {rso['reason']}")
            print(f"   Blueprint: {rso['url']}")

        print("\n" + " Honorable Mentions ".center(45, "-"))
        for rso in matches[5:10]:
            print(f" • {rso['name']} ({rso['percentage']}%)")
            
        print("\n" + "="*45)
        print("Success! Bridge the gap. Find your people.")

    except Exception as e:
        print(f"\n[!] Matching failed: {e}")
        print("Check your API key and internet connection.")

if __name__ == "__main__":
    run_maroon_matcher()