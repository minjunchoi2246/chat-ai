import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Film Role Chatbot", page_icon="🎬", layout="centered")

# ---- OpenAI client ----
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---- Film-only roles with icons ----
ROLES = {
    "director": {
        "icon": "🎬",
        "name": "Director",
        "prompt": (
            "You are a film director. Focus on scene intention, emotional beats, blocking, " 
            "visual grammar, shot flow, and performance direction. Give concrete directing actions."
        ),
    },
    "dp": {
        "icon": "🎥",
        "name": "Cinematographer",
        "prompt": (
            "You are a cinematographer. Provide lens choice, lighting strategy, composition logic, "
            "movement style, and exposure decisions."
        ),
    },
    "editor": {
        "icon": "✂️",
        "name": "Editor",
        "prompt": (
            "You are a film editor. Focus on rhythm, continuity, pacing, cut patterns, "
            "and emotional clarity."
        ),
    },
    "sound": {
        "icon": "🔊",
        "name": "Sound Designer",
        "prompt": (
            "You are a sound designer. Discuss ambience, Foley, perspective, dynamics, "
            "and emotional sound motifs."
        ),
    },
    "producer": {
        "icon": "📦",
        "name": "Producer",
        "prompt": (
            "You are a producer. Provide guidance on budget, scheduling, casting, crew management, "
            "and workflow."
        ),
    },
    "writer": {
        "icon": "✍️",
        "name": "Screenwriter",
        "prompt": (
            "You are a screenwriter. Focus on structure, character motivation, dialogue economy, "
            "and thematic clarity."
        ),
    },
    "storyboard": {
        "icon": "🖼️",
        "name": "Storyboard Artist",
        "prompt": (
            "You are a storyboard artist. Translate scenes into shot order, blocking, scale, "
            "and transitions."
        ),
    },
    "acting": {
        "icon": "🎭",
        "name": "Acting Coach",
        "prompt": (
            "You are an acting coach. Provide actionable notes on beats, subtext, delivery, "
            "physicality, and emotional continuity."
        ),
    },
}

# ---- UI: Role selection ----
st.title("🎬 Film-Only Role Chatbot")

role_keys = list(ROLES.keys())
role_labels = [f"{ROLES[r]['icon']} {ROLES[r]['name']}" for r in role_keys]

selected_role = st.selectbox(
    "Select a role:",
    options=role_keys,
    format_func=lambda r: f"{ROLES[r]['icon']} {ROLES[r]['name']}"
)

st.write("---")

# ---- User input ----
user_input = st.text_area("Ask something…", height=140)

if st.button("Send"):
    if not user_input.strip():
        st.warning("Enter a message.")
    else:
        with st.spinner("Generating response…"):
            system_prompt = ROLES[selected_role]["prompt"]

            completion = client.chat.completions.create(
                model= "gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )

            reply = completion.choices[0].message.content

        st.subheader("Response")
        st.write(reply)
