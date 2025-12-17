import os
import sys
import yaml
import rasa.__main__

# --- 1. SETUP ENVIRONMENT ---
project_root = os.getcwd()
sys.path.insert(0, project_root)
print(f"📍 Project Root: {project_root}")

# --- 2. FORCE-FIX CREDENTIALS.YML (THE DIRECT KEY METHOD) ---
# We use the class path as the KEY. This forces Rasa to load it directly.
correct_credentials = {
    "rasa": {
        "url": "http://localhost:5002/api"
    },
    # NOTICE: The key itself is now the import path!
    "channels.custom_voice_connector.VoiceInputChannel": {
        # We can leave this empty or add parameters if needed later
    }
}

print("🔧 Force-correcting credentials.yml...")
with open("credentials.yml", "w") as f:
    yaml.dump(correct_credentials, f, default_flow_style=False)

# --- 3. PRIME THE PYTHON LOADER ---
print("🔌 Pre-loading voice channel...")
try:
    import channels.custom_voice_connector
    print(f"   ✅ Successfully loaded module: {channels.custom_voice_connector.__name__}")
except ImportError as e:
    print(f"   ❌ CRITICAL ERROR: Could not import module. Reason: {e}")
    sys.exit(1)

# --- 4. LAUNCH RASA ---
print("🚀 Starting Rasa Core...")

# Set arguments
sys.argv = [
    "rasa", 
    "run", 
    "--enable-api", 
    "--credentials", "credentials.yml",
    "--cors", "*"
]

# Launch!
rasa.__main__.main()