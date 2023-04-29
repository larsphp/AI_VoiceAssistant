# AI_VoiceAssistant

This is a python program which can be used to communicate with OpenAI's gpt-3.5-turbo language model using speech input.
The GPT output will be converted to audio and spoken to you.

The python package used to get audio from you're microphone is speech_recognition.
OpenAI's whisper-1 API is used to turn your spoken text into written text. This works for over 100 languages,
more about that on: https://openai.com/research/whisper.
GPT3.5 answers you're question in form of written text, which is then passed into
ElevenLabs' API to become humanly spoken audio. This works in only a few languages,
more about that on: https://beta.elevenlabs.io.

In order to run this program properly an ElevenLabs API Key as well as an OpenAI API Key is needed.
ElevenLabs has a free plan which includes 10000 free characters per month to be processed. This can be enough depending
on the usage.
OpenAI's API has a free trial of $5 for 3 months, after that it costs money (very little though).

The set up is simple:

- Write you'r API Keys into the "keys.txt" file.
- Optionally make some configurations in the "config.txt" file. You can select the ElevenLabs langauge and set a system prompt.
- Start the "main.py" script.

Enjoy.
