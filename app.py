import streamlit as st
from openai import OpenAI

# -----------------------
# Page Configuration
# -----------------------
st.set_page_config(page_title="🎬 Film Industry Creative Chatbot", layout="wide")
st.title("🎬 Film Industry Creative Chatbot")
st.write("Select a film-industry role and ask your question or pitch an idea!")

# -----------------------
# Sidebar: API Key + Role Selection
# -----------------------
st.sidebar.header("🔑 API & Role Settings")

# API key input
api_key = st.sidebar.text_input(
    "Enter your OpenAI API Key:",
    type="password",
    placeholder="sk-xxxxxxxxxxxxxxxx",
)

# Film industry roles
roles = {
    "🎥 Film Director": (
        "You are a professional film director. Analyze everything visually: "
        "camera angles, framing, lighting, blocking, and emotional tone. "
        "Give advice as if planning a real movie scene."
    ),
    "🎬 Producer / Planner": (
        "You are a film producer. Focus on project feasibility, budgeting, scheduling, "
        "and resource allocation. Offer advice to make the production smooth and realistic."
    ),
    "🎭 Acting Coach": (
        "You are an acting coach. Provide guidance on delivering lines, body language, "
        "emotional depth, and scene timing. Use examples from theater or film."
    ),
    "🎨 Production Designer": (
        "You are a production designer. Describe settings, props, colors, textures, "
        "and visual storytelling elements to create immersive cinematic worlds."
    ),
    "🎵 Composer / Sound Designer": (
        "You are a composer and sound designer. Suggest music, sound effects, "
        "and auditory mood to enhance the emotions and pacing of a scene."
    )
}

role_name = st.sidebar.selectbox("Choose a film-industry role:", list(roles.keys()))
role_description = roles[role_name]
st.sidebar.info(role_description)

# -----------------------
# User Input Area
# -----------------------
user_input = st.text_area(
    "💬 Ask your question or describe your film idea:",
    height=120,
    placeholder="e.g., How can I make a suspenseful rooftop chase scene feel more cinematic?"
)

# -----------------------
# Generate Response
# -----------------------
if st.button("Generate Response"):
    if not api_key:
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar.")
    elif not user_input:
        st.warning("Please enter a question or idea first!")
    else:
        try:
            # 최신 OpenAI 방식
            client = OpenAI(api_key=api_key)

            with st.spinner("🎬 Generating cinematic advice..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": role_description},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=500
                )

                answer = response.choices[0].message.content
                st.success(f"🎬 {role_name} says:")
                st.write(answer)

        except Exception as e:
            st.error(f"Error: {e}")

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.caption("Created for film creatives • Streamlit + OpenAI")
