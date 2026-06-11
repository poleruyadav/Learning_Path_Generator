import uuid
import streamlit as st

from chain import run_chain


# ---------- Session State ----------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat_id" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {"title": "New Chat", "skill": "", "output": None}
    st.session_state.current_chat_id = chat_id


# ---------- Page Config ----------
st.set_page_config(
    page_title="Learning Path Generator",
    page_icon="🧠",
    layout="centered"
)


# ---------- Sidebar ----------
with st.sidebar:
    st.title("💬 Chats")

    if st.button("➕ New Chat", use_container_width=True):
        chat_id = str(uuid.uuid4())
        st.session_state.chats[chat_id] = {"title": "New Chat", "skill": "", "output": None}
        st.session_state.current_chat_id = chat_id
        st.rerun()

    chat_ids = list(st.session_state.chats.keys())
    chat_titles = {cid: st.session_state.chats[cid]["title"] for cid in chat_ids}

    selected_chat = st.radio(
        "Chat History",
        chat_ids,
        format_func=lambda x: chat_titles[x],
        index=chat_ids.index(st.session_state.current_chat_id)
    )
    st.session_state.current_chat_id = selected_chat

    if st.button("🗑️ Delete Chat", use_container_width=True):
        del st.session_state.chats[selected_chat]

        if st.session_state.chats:
            st.session_state.current_chat_id = next(iter(st.session_state.chats))
        else:
            chat_id = str(uuid.uuid4())
            st.session_state.chats[chat_id] = {"title": "New Chat", "skill": "", "output": None}
            st.session_state.current_chat_id = chat_id

        st.rerun()


# ---------- Main UI ----------
current_chat = st.session_state.chats[st.session_state.current_chat_id]

st.title("🧠 Learning Path Generator")
st.write("Enter a skill/domain and generate a structured AI learning roadmap.")

skill = st.text_input(
    "Skill / Domain",
    value=current_chat["skill"],
    placeholder="e.g., Gen AI, NLP, Data Science"
)


# ---------- Generate ----------
if st.button("Generate Learning Path"):
    if not skill.strip():
        st.warning("⚠️ Please enter a skill/domain.")
    else:
        with st.spinner("Generating learning roadmap..."):
            try:
                validated_output = run_chain(skill)

                current_chat["skill"] = skill
                current_chat["title"] = skill[:25]
                current_chat["output"] = validated_output

                st.success("✅ Learning Path Generated Successfully!")

            except Exception as e:
                st.error("❌ Failed to generate learning path.")
                raw = getattr(e, "raw_output", "N/A")
                st.text("Raw LLM Output:")
                st.code(raw)
                st.text(f"Error: {e}")


# ---------- Display Output ----------
if current_chat["output"]:
    output = current_chat["output"]

    st.subheader("📚 Learning Stages")
    for stage in output.learning_stages:
        st.markdown(f"- {stage}")

    st.subheader("🧩 Key Topics")
    for topic in output.key_topics:
        st.markdown(f"- {topic}")

    st.subheader("🎯 Learning Goal Summary")
    st.write(output.learning_goal_summary)

    with st.expander("🔍 View Raw JSON Output"):
        st.json(output.model_dump())