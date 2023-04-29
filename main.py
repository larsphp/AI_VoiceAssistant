import os
import openai
import requests
import speech_recognition
from elevenlabslib import *
from elevenlabslib import ElevenLabsUser

# Get keys from keys.txt file
with open("keys.txt", "r") as key_file:
    lines = key_file.read().replace(" ", "").split("\n")
    OPENAI_KEY = lines[0].split("=")[1]
    ELEVENLABS_KEY = lines[1].split("=")[1]

# Get config from config.txt file. If config is faulty, use default values
with open("config.txt", "r") as config_file:
    try:
        lines = config_file.read().split("\n")
        VOICE = lines[0].split("=")[1]
        line1split = lines[1].split("=")
        SYSTEM_PROMPT = ("" if len(line1split) == 1 else line1split[1])
    except:
        VOICE = "Bella"
        SYSTEM_PROMPT = ""

# Set the OpenAI and ElevenLabs API keys
openai.api_key = OPENAI_KEY

# Configure Elevenlabs API
user = ElevenLabsUser(ELEVENLABS_KEY)
voice = user.get_voices_by_name("Bella")[0]

# Check the number of characters left in Elevenlabs API
request = requests.get('https://api.elevenlabs.io/v1/user',
                       headers={'xi-api-key': ELEVENLABS_KEY})
request = request.json()['subscription']
count = request['character_limit'] - request['character_count']
print(str(count) + " characters left.")

# Initialize the messages list with the system prompt
messages = ([{"role": "system", "content": SYSTEM_PROMPT}]
            if SYSTEM_PROMPT != "" else [])

# Open the log file
log = open("log.txt", "a")
log.write("\n\n\n\nNEW CONVERSATION:\n\n")
log.close()

# Initialize the speech recognition module
sr = speech_recognition.Recognizer()

# Start the conversation loop.
# Every iteration of the loop is one turn of the conversation.
while (True):

    # Set the microphone as the audio source
    with speech_recognition.Microphone() as source:
        print("Say something!")
        audio = sr.listen(source)

    print("Processing...")
    # Save the audio to an MP3 file
    with open("audio.mp3", "wb") as f:
        f.write(audio.get_wav_data())

    #Get the text from the audio
    audio_file = open("audio.mp3", "rb")
    result = openai.Audio.transcribe("whisper-1", audio_file)
    audio_file.close()
    prompt = result["text"]
    print(prompt)

    # Add the user's prompt to the messages list and log it
    messages.append({"role": "user", "content": prompt})
    #NOTE: currently always opening and closing the log file,
    #      because there is no way to exit the loop yet
    with open("log.txt", "a") as log:
        log.write("User:\n" + prompt + "\n\n")

    # Send the messages to the OpenAI API and get the response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Get the response from the API and add it to the messages list and log it
    response = response.choices[0].message.content
    messages.append({"role": "system", "content": response})
    with open("log.txt", "a") as log:
        log.write("User:\n" + response + "\n\n")
    print(response)

    # Generate and play the audio
    audio = voice.generate_and_play_audio(response,
                                          playInBackground=False,
                                          model_id="eleven_multilingual_v1")

    #delete the audio file
    os.remove("audio.mp3")