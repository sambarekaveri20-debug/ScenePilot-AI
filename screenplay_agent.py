import os
import json
from google import genai

# Gemini client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def analyze_screenplay(screenplay):
    prompt = f"""
You are ScenePilot AI's Screenplay Agent.

Analyze the screenplay below and extract production information
for every scene.

For each scene identify:
- scene_number
- location
- time_of_day
- characters
- props
- action
- special_requirements

Return ONLY valid JSON in this format:

{{
  "scenes": [
    {{
      "scene_number": 1,
      "location": "",
      "time_of_day": "",
      "characters": [],
      "props": [],
      "action": "",
      "special_requirements": []
    }}
  ]
}}

SCREENPLAY:
{screenplay}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown code fences if Gemini adds them
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


# Sample screenplay for demo
screenplay = """
SCENE 1 - HOUSE - MORNING

Rahul enters his house. His mother is sitting in the living room.
Rahul puts his school bag on the table.

SCENE 2 - COLLEGE - DAY

Rahul meets his friend Amit near the classroom.
They discuss the upcoming competition.

SCENE 3 - PLAYGROUND - EVENING

Rahul and Amit play football with other students.
A football and school bags are visible.
"""

result = analyze_screenplay(screenplay)

print("\n===== SCENEPILOT AI - SCREENPLAY ANALYSIS =====\n")
print(json.dumps(result, indent=2))

print("\n===== VALIDATION =====")

for scene in result["scenes"]:
    required = [
        "scene_number",
        "location",
        "time_of_day",
        "characters",
        "props",
        "action",
        "special_requirements"
    ]

    missing = [field for field in required if field not in scene]

    if missing:
        print(f"Scene {scene.get('scene_number', '?')}: Missing {missing}")
    else:
        print(f"Scene {scene['scene_number']}: VALID")