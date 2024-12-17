# VoiceDraw: Voice-Based Drawing

VoiceDraw is an innovative web application that combines voice recognition, transcription, and AI-powered image generation to create a unique voice-driven drawing experience. Users can speak prompts, which are transcribed and used to generate images through advanced AI models such as OpenAI's DALL·E and Google Gemini.

## Features

- **Voice Recording**: Record your voice and generate text from it using OpenAI’s Whisper model.
- **AI-Powered Image Generation**: Use the transcribed text to generate images using OpenAI’s DALL·E and Google Gemini.
- **Interactive UI**: A simple, user-friendly interface with real-time feedback, including audio playback and generated images.
- **Latest Image Use**: Optionally, use previously generated images to refine or alter new images based on new prompts.

## Technologies Used

- **Frontend**: Streamlit (Python Web Framework)
- **Backend**: Python, OpenAI API (for voice transcription and image generation), Google Gemini API (for advanced image-based prompts)
- **Audio Recording**: PyAudio
- **Image Generation**: DALL·E, Google Gemini
- **Environment Management**: dotenv for managing API keys securely
- **Storage**: Local storage for audio and image files

## Installation

Follow these steps to set up the project locally:

### 1. Clone the repository:

```bash
git clone https://github.com/erendagstan/SketchTalk.git
cd SketchTalk
```
### 2. Clone the repository:

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables:
```bash
openai_apikey=your-openai-api-key
gemini_apikey=your-google-gemini-api-key
```
### 4. Set up environment variables:
```bash
streamlit run app.py
```
<h2>How It Works</h2>
<ul>
  <li><strong>Recording:</strong> Click the "Start" button to begin recording your voice. The system captures your speech and saves it as a .wav file.</li>
  <li><strong>Transcription:</strong> Once you stop recording, the audio is transcribed using OpenAI’s Whisper model, converting speech to text.</li>
  <li><strong>Image Generation:</strong> The transcribed text is used as a prompt to generate an image using either OpenAI’s DALL·E model or Google Gemini. The system will display the image to you, along with an option to download it.</li>
  <li><strong>Interaction:</strong> You can toggle whether to use the most recently generated image in the prompt for the next creation.</li>
</ul>

<h2>File Overview</h2>
<ul>
  <li><strong>app.py:</strong> The main Streamlit app for handling the user interface, audio recording, transcription, and image generation.</li>
  <li><strong>recorder.py:</strong> Handles audio recording functionality using PyAudio.</li>
  <li><strong>transcriptor.py:</strong> Transcribes audio into text using OpenAI’s Whisper model.</li>
  <li><strong>painter.py:</strong> Generates images using OpenAI's DALL·E and Google Gemini based on the transcribed text.</li>
  <li><strong>images/:</strong> Directory where generated images are saved.</li>
  <li><strong>voices/:</strong> Directory where recorded audio files are saved.</li>
</ul>

<img width="960" alt="horse_in_space" src="https://github.com/user-attachments/assets/5e5dbaed-de20-4a1c-989d-9c17a7a98264" />

