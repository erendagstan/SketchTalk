import streamlit as st
import threading
import recorder
import transcriptor
import painter

if "record_active" not in st.session_state:
    st.session_state.record_active = threading.Event()
    st.session_state.recording_status = "Ready to Start!"
    st.session_state.recording_completed = False
    st.session_state.latest_image = ""
    st.session_state.messages = []  # List to store prompt messages
    st.session_state.frames = []  # List to store pieces of audio data

# Functions for recording control
def start_recording():
    st.session_state.record_active.set()
    st.session_state.frames = []
    st.session_state.recording_status = "🔴 Recording Your Voice..."
    st.session_state.recording_completed = False
    threading.Thread(target=recorder.record, args=(st.session_state.record_active, st.session_state.frames)).start()

def stop_recording():
    st.session_state.record_active.clear()
    st.session_state.recording_status = "🟩 Recording Completed!"
    st.session_state.recording_completed = True

# Streamlit UI Setup
st.set_page_config(page_title="Voice Draw", layout="wide", page_icon="icons/app_icon.png")
st.image(image="icons/top_banner.png", use_column_width=True)
st.header("VoiceDraw: Voice-Based Drawing")

st.divider()

col_audio, col_image = st.columns([1, 4])

with col_audio:
    st.subheader("Voice Recording")
    st.divider()
    status_message = st.info(st.session_state.recording_status)
    st.divider()

    subcol_left, subcol_right = st.columns([1, 2])

    with subcol_left:
        recorder_starter = st.button(label="Start", on_click=start_recording, disabled=st.session_state.record_active.is_set())
        recorder_stopper = st.button(label="Stop", on_click=stop_recording, disabled=not st.session_state.record_active.is_set())

    with subcol_right:
        recorded_audio = st.empty()  # Placeholder
        if st.session_state.recording_completed:
            recorded_audio = st.audio(data="voices/voice_prompt.wav")

    st.divider()
    latest_image_use = st.checkbox(label="Use Latest Image")

with col_image:
    st.subheader("Visual Outputs")
    st.divider()

    # Display messages and generated images
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message(name=message["role"], avatar="icons/ai_avatar.png"):
                st.warning("Here is the Image I Created for You:")
                st.image(image=message["content"], width=300)
        elif message["role"] == "user":
            with st.chat_message(name=message["role"], avatar="icons/user_avatar.png"):
                st.success(message["content"])

    # Once recording stops, process voice and generate an image
    if recorder_stopper:
        with st.chat_message(name="user", avatar="icons/user_avatar.png"):
            with st.spinner("Transcribing Your Voice..."):
                voice_prompt = transcriptor.transcribe_with_whisper(audio_file_name="voices/voice_prompt.wav")
            st.success(voice_prompt)

        st.session_state.messages.append({"role": "user", "content": voice_prompt})

        with st.chat_message(name="assistant", avatar="icons/ai_avatar.png"):
            st.warning("Here is the Image I Created for You:")
            with st.spinner("Generating Your Image..."):
                # Conditionally use the latest image or generate a new one
                if latest_image_use:
                    image_file_name = painter.generate_image(image_path=st.session_state.latest_image, prompt=voice_prompt)
                else:
                    image_file_name = painter.generate_image_with_dalle(prompt=voice_prompt)

            st.image(image=image_file_name, width=300)

            # Allow users to download the generated image
            with open(image_file_name, "rb") as file:
                st.download_button(
                    label="Download Image",
                    data=file,
                    file_name=image_file_name,
                    mime="image/png"
                )

        st.session_state.messages.append({"role": "assistant", "content": image_file_name})
        st.session_state.latest_image = f"{image_file_name}"
