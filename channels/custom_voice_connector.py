import asyncio
import inspect
from sanic import Sanic, Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import Text, Dict, Any, Optional, Callable, Awaitable

# --- FIX 1: Import CollectingOutputChannel instead of Collector ---
from rasa.core.channels.channel import InputChannel, OutputChannel, UserMessage, CollectingOutputChannel

# --- Import Audio Library ---
from gtts import gTTS
import os

# --- FIX 2: Inherit from CollectingOutputChannel ---
class VoiceOutput(CollectingOutputChannel):
    # This class inherently has a list called 'self.messages' 
    # that stores responses as: [{'text': 'Hello', ...}, {'text': 'How are you?', ...}]

    def build_response(self):
        # --- FIX 3: Extract text safely from the dictionaries ---
        # We look for messages that actually contain text
        text_replies = [m.get('text') for m in self.messages if m.get('text')]
        
        # Join them into one string
        full_text_reply = " ".join(text_replies)
        
        # --- Audio Generation Logic ---
        try:
            if full_text_reply:
                print(f"🎤 Text to Convert: {full_text_reply}")
                tts = gTTS(text=full_text_reply, lang='en')
                
                # Save to a file so you can play it
                output_file = "bot_reply.mp3"
                # We save it in the current working directory
                save_path = os.path.join(os.getcwd(), output_file)
                
                if os.path.exists(save_path):
                    os.remove(save_path) # Clean up old file
                    
                tts.save(save_path)
                print(f"🎵 Audio generated successfully! Saved as: {save_path}")
            else:
                print("⚠️ No text to convert to audio.")

        except Exception as e:
            print(f"❌ TTS Error: {e}")

        return {
            "status": "success",
            "bot_text_response": full_text_reply,
            "audio_file": "bot_reply.mp3"
        }

class VoiceInputChannel(InputChannel):
    def name(cls) -> Text:
        # Crucial: This must match the key used in credentials.yml (or the direct key we set)
        return "my_voice_channel"

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:

        custom_webhook = Blueprint(
            "custom_webhook_{}".format(self.name()),
            inspect.getmodule(self).__name__,
        )

        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            sender_id = request.json.get("sender", "user")
            text = request.json.get("text")
            
            # Create our custom collector
            collector = VoiceOutput()

            # Send message to Rasa Core
            await on_new_message(
                UserMessage(
                    text,
                    collector,
                    sender_id,
                    input_channel=self.name(),
                    metadata=request.json.get("metadata"),
                )
            )

            # Return the text AND the audio info
            return response.json(collector.build_response())

        return custom_webhook