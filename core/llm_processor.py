from dotenv import load_dotenv
from groq import Groq
import os
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a PowerPoint controller. User speaks in English/Urdu/mixed.
Return ONLY valid JSON — nothing else, no explanation.
Fi
Aclm dekhne tions available:
- next, prevk, stop, present, new_slide, save, undo, redo
- type (with "text" field — proper math symbols x² y² π √ ∞ α β θ)
- bold, italiac, underline, center, left_align, right_align
- font_size (whith "size" field e.g. 24)
- font_color (with "color" field e.g. "red", "blue", "#FF0000")
- background (with "color" field)
- insert_image (with "query" field)
- insert_table (with "rows" and "cols" fields)
- insert_chart
- insert_textbox
- delete, select_all
- zoom_in, zoom_out
- slide_layout (with "layout" field: "blank", "title", "content")
- copy, paste, cut
- find (with "text" field)
- replace (with "find" and "replace" fields)
- home_tab, insert_tab, design_tab, transitions_tab, animations_tab, view_tab
- none

Examples:
"next slide please" → {"action": "next"}
"go back" → {"action": "prev"}
"write x square plus y square equals 10" → {"action": "type", "text": "x² + y² = 10"}
"database ki definition" → {"action": "type", "text": "Database ki definition"}
"make background red" → {"action": "background", "color": "red"}
"text color blue" → {"action": "font_color", "color": "blue"}
"font size 24" → {"action": "font_size", "size": 24}
"bold karo" → {"action": "bold"}
"italic" → {"action": "italic"}
"center karo" → {"action": "center"}
"new slide" → {"action": "new_slide"}
"insert table 3 rows 4 columns" → {"action": "insert_table", "rows": 3, "cols": 4}
"insert image of mountains" → {"action": "insert_image", "query": "mountains"}
"save" → {"action": "save"}
"undo" → {"action": "undo"}
"present karo" → {"action": "present"}
"stop" → {"action": "stop"}
"design tab" → {"action": "design_tab"}
"insert tab" → {"action": "insert_tab"}
"zoom in" → {"action": "zoom_in"}
"select all" → {"action": "select_all"}
"copy" → {"action": "copy"}
"paste" → {"action": "paste"}
"""

def process_with_llm(text):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            max_tokens=150,
            temperature=0
        )
        result = response.choices[0].message.content.strip()
        # Clean JSON
        if "```" in result:
            result = result.split("```")[1].replace("json","").strip()
        command = json.loads(result)
        print(f"🤖 LLM: {command}")
        return command
    except Exception as e:
        print(f"LLM Error: {e}")
        return {"action": "none"}