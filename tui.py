import google.generativeai as genai
import pandas as pd
import json
import os
import sys

# 1. SECURE KEY ACCESS
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in environment.")
    print("Run: export GEMINI_API_KEY='your_key_here'")
    sys.exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def match_rsos():
    print("\n" + "="*40)
    print("       MAROON MATCHER: RSO ENGINE")
    print("="*40)

    # 2. GATHER INPUTS
    interest = input("\n[?] What are your interests/hobbies? ")
    goals = input("[?] What is your goal? (Professional/Social/Service): ")
    vibe = input("[?] Preferred vibe? (Chill/Competitive/Creative): ")

    user_profile = {
        "interests": interest,
        "goals": goals,
        "vibe": vibe
    }

    # 3. READ DATA
    try:
        df = pd.read_csv("UChicago_RSO_Directory.csv")
        rso_summary = df[['Name', 'Description', 'Category', 'Link']].to_string(index=False)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # 4. AI LOGIC
    print("\n[System] Calculating leverage and matching...")
    
    prompt = f"""
    You are a UChicago Student Success AI. 
    User Profile: {json.dumps(user_profile)}
    
    RSO Directory:
    {rso_summary}

    Identify 10 matches. Rank them by Match_Percentage.
    Return ONLY a JSON list of objects.
    Format: [{{"name": "", "percentage": 0, "reason": "", "link": ""}}]
    """

    try:
        response = model.generate_content(prompt)
        # Handle potential markdown formatting in AI response
        raw_json = response.text.replace('```json', '').replace('
```', '').strip()
        matches = json.loads(raw_json)

        # 5. DISPLAY
        print("\n" + "⭐ TOP 5 RECOMMENDATIONS ".center(40, "="))
        for i, rso in enumerate(matches[:5], 1):
            print(f"\n{i}. {rso['name']} ({rso['percentage']}%)")
            print(f"   Why: {rso['reason']}")
            print(f"   Link: {rso['link']}")

        print("\n" + " Honorable Mentions ".center(40, "-"))
        for rso in matches[5:]:
            print(f" • {rso['name']} ({rso['percentage']}%)")
            
    except Exception as e:
        print(f"Matching failed: {e}")

if __name__ == "__main__":
    match_rsos()