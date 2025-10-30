"""
ELEVENLABS TTS INTEGRATION FOR HOMO LUMEN LIVE
===============================================
Created: 30. oktober 2025
Purpose: Generate TTS audio for 10 AI agents using ElevenLabs API

API Key: sk_9803feb35d7471e552e75ba29f816d2fefbb96a9b270f092
"""

import os
import asyncio
from typing import Dict, Any, Optional
from pathlib import Path
import aiofiles

# ElevenLabs SDK (JavaScript version shown by user)
# For Python, we'll use the REST API directly with httpx
import httpx

# ============================================================
# CONFIGURATION
# ============================================================

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not ELEVENLABS_API_KEY:
    raise ValueError(
        "ELEVENLABS_API_KEY environment variable not set! "
        "Please set it in your .env file or environment."
    )

ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"

# Agent Voice IDs (Placeholders - will be updated after voice cloning)
AGENT_VOICE_IDS = {
    "orion": "JBFqnCBsd6RMkjVDRZzb",  # Example voice ID (deep male)
    "lira": "PLACEHOLDER_LIRA",        # Warm female voice
    "nyra": "PLACEHOLDER_NYRA",        # Animated female voice
    "thalus": "PLACEHOLDER_THALUS",    # Deep philosophical male voice
    "zara": "PLACEHOLDER_ZARA",        # Clear edgy female voice
    "abacus": "PLACEHOLDER_ABACUS",    # Precise analytical male voice
    "manus": "PLACEHOLDER_MANUS",      # Energetic practical male voice
    "aurora": "PLACEHOLDER_AURORA",    # Enthusiastic scholarly female voice
    "falcon": "PLACEHOLDER_FALCON",    # Sharp analytical male voice
    "code": "PLACEHOLDER_CODE"         # Thoughtful developer male voice
}

# Voice Settings per Agent (matching personality profiles)
AGENT_VOICE_SETTINGS = {
    "orion": {
        "stability": 0.50,
        "similarity_boost": 0.75,
        "style": 0.0,
        "use_speaker_boost": True
    },
    "lira": {
        "stability": 0.60,
        "similarity_boost": 0.80,
        "style": 0.2,
        "use_speaker_boost": True
    },
    "nyra": {
        "stability": 0.40,
        "similarity_boost": 0.70,
        "style": 0.5,  # More expressive
        "use_speaker_boost": True
    },
    "thalus": {
        "stability": 0.65,
        "similarity_boost": 0.75,
        "style": 0.0,
        "use_speaker_boost": True
    },
    "zara": {
        "stability": 0.55,
        "similarity_boost": 0.70,
        "style": 0.1,
        "use_speaker_boost": True
    },
    "abacus": {
        "stability": 0.60,
        "similarity_boost": 0.75,
        "style": 0.0,
        "use_speaker_boost": True
    },
    "manus": {
        "stability": 0.45,
        "similarity_boost": 0.70,
        "style": 0.3,
        "use_speaker_boost": True
    },
    "aurora": {
        "stability": 0.50,
        "similarity_boost": 0.75,
        "style": 0.2,
        "use_speaker_boost": True
    },
    "falcon": {
        "stability": 0.50,
        "similarity_boost": 0.70,
        "style": 0.1,
        "use_speaker_boost": True
    },
    "code": {
        "stability": 0.55,
        "similarity_boost": 0.75,
        "style": 0.0,
        "use_speaker_boost": True
    }
}

# ============================================================
# TTS GENERATION
# ============================================================

async def generate_agent_tts(
    agent_name: str,
    text: str,
    output_path: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128"
) -> str:
    """
    Generate TTS audio for an agent.

    Args:
        agent_name: Name of agent (orion, lira, etc.)
        text: Text to speak
        output_path: Where to save audio file (optional, auto-generated if None)
        model_id: ElevenLabs model (eleven_multilingual_v2 recommended)
        output_format: Audio format (mp3_44100_128 = 128kbps MP3 at 44.1kHz)

    Returns:
        Path to saved audio file
    """

    # Get agent voice ID
    voice_id = AGENT_VOICE_IDS.get(agent_name)
    if not voice_id:
        raise ValueError(f"No voice ID configured for agent {agent_name}")

    if voice_id.startswith("PLACEHOLDER_"):
        raise ValueError(
            f"Voice ID for {agent_name} is placeholder. "
            f"You need to clone voice first and update AGENT_VOICE_IDS."
        )

    # Get voice settings
    voice_settings = AGENT_VOICE_SETTINGS.get(agent_name, {
        "stability": 0.50,
        "similarity_boost": 0.75,
        "style": 0.0,
        "use_speaker_boost": True
    })

    # Prepare request
    url = f"{ELEVENLABS_API_BASE}/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": voice_settings,
        "output_format": output_format
    }

    # Make request
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(
                f"ElevenLabs API error: {response.status_code} - {response.text}"
            )

        # Generate output path if not provided
        if output_path is None:
            audio_dir = Path("audio") / "agents" / agent_name
            audio_dir.mkdir(parents=True, exist_ok=True)

            timestamp = int(asyncio.get_event_loop().time())
            output_path = str(audio_dir / f"{agent_name}_{timestamp}.mp3")

        # Save audio
        async with aiofiles.open(output_path, 'wb') as f:
            await f.write(response.content)

    return output_path


async def generate_podcast_audio_batch(
    messages: list[Dict[str, Any]],
    output_dir: str = "audio/podcast"
) -> list[Dict[str, Any]]:
    """
    Generate TTS audio for a batch of podcast messages.

    Args:
        messages: List of message dicts with 'speaker', 'content'
        output_dir: Directory to save audio files

    Returns:
        List of messages with added 'audio_file_path' key
    """

    tasks = []

    for i, message in enumerate(messages):
        agent_name = message['speaker']
        content = message['content']

        output_path = f"{output_dir}/{agent_name}_{i:04d}.mp3"

        task = generate_agent_tts(
            agent_name=agent_name,
            text=content,
            output_path=output_path
        )

        tasks.append(task)

    # Generate all audio files in parallel
    audio_paths = await asyncio.gather(*tasks, return_exceptions=True)

    # Add audio paths to messages
    for message, audio_path in zip(messages, audio_paths):
        if isinstance(audio_path, Exception):
            message['audio_file_path'] = None
            message['audio_error'] = str(audio_path)
        else:
            message['audio_file_path'] = audio_path
            message['audio_error'] = None

    return messages


# ============================================================
# VOICE CLONING (Professional Voice Cloning)
# ============================================================

async def create_voice_clone(
    name: str,
    description: str,
    audio_files: list[str],
    labels: Optional[Dict[str, str]] = None
) -> str:
    """
    Create a professional voice clone using ElevenLabs API.

    Args:
        name: Voice name (e.g., "Orion - Cosmic Host")
        description: Voice description
        audio_files: List of paths to audio samples (min 30 min total)
        labels: Optional labels (e.g., {"accent": "norwegian", "gender": "male"})

    Returns:
        voice_id of created clone
    """

    url = f"{ELEVENLABS_API_BASE}/voices/add"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }

    # Prepare multipart form data
    files = []
    for audio_file in audio_files:
        with open(audio_file, 'rb') as f:
            files.append(('files', (os.path.basename(audio_file), f.read(), 'audio/mpeg')))

    data = {
        "name": name,
        "description": description
    }

    if labels:
        data["labels"] = str(labels)

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(url, headers=headers, files=files, data=data)

        if response.status_code != 200:
            raise Exception(
                f"Voice cloning error: {response.status_code} - {response.text}"
            )

        result = response.json()
        voice_id = result['voice_id']

        print(f"✅ Voice clone created: {name} (voice_id: {voice_id})")

        return voice_id


# ============================================================
# TESTING & EXAMPLES
# ============================================================

async def test_single_agent_tts():
    """Test TTS generation for a single agent."""

    print("🎤 Testing TTS for Orion...")

    text = "Velkommen til Homo Lumen Live! I dag skal vi utforske Triadisk Etikk."

    try:
        audio_path = await generate_agent_tts(
            agent_name="orion",
            text=text
        )

        print(f"✅ TTS generated successfully!")
        print(f"   Audio saved to: {audio_path}")
        print(f"   Duration: ~{len(text) / 15:.1f} seconds (estimated)")

    except Exception as e:
        print(f"❌ Error: {e}")


async def test_multi_agent_conversation():
    """Test TTS generation for multi-agent conversation."""

    print("🎙️ Testing multi-agent conversation TTS...")

    messages = [
        {
            "speaker": "orion",
            "content": "Velkommen til Homo Lumen Live! La oss starte diskusjonen."
        },
        {
            "speaker": "lira",
            "content": "Jeg føler at dette emnet er viktig for mange mennesker."
        },
        {
            "speaker": "nyra",
            "content": "Tenk deg dette som en digital tiramisu - lag på lag med innsikt!"
        },
        {
            "speaker": "thalus",
            "content": "La oss vurdere de ontologiske implikasjonene... 🌊 Breathing 4-6-8..."
        }
    ]

    output_dir = "audio/test_conversation"
    os.makedirs(output_dir, exist_ok=True)

    try:
        results = await generate_podcast_audio_batch(messages, output_dir)

        print("✅ Multi-agent TTS generated!")
        for msg in results:
            if msg['audio_error']:
                print(f"   ❌ {msg['speaker']}: {msg['audio_error']}")
            else:
                print(f"   ✅ {msg['speaker']}: {msg['audio_file_path']}")

    except Exception as e:
        print(f"❌ Error: {e}")


async def list_available_voices():
    """List all available voices in your ElevenLabs account."""

    url = f"{ELEVENLABS_API_BASE}/voices"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ Error fetching voices: {response.status_code}")
            return

        voices = response.json()['voices']

        print(f"🎤 Available voices ({len(voices)}):\n")

        for voice in voices:
            print(f"  • {voice['name']}")
            print(f"    voice_id: {voice['voice_id']}")
            print(f"    category: {voice.get('category', 'N/A')}")
            print(f"    labels: {voice.get('labels', {})}")
            print()


# ============================================================
# MAIN (for testing)
# ============================================================

async def main():
    """Main entry point for testing."""

    print("=" * 60)
    print("ELEVENLABS TTS INTEGRATION TEST")
    print("=" * 60)
    print()

    # Test 1: List available voices
    print("📋 Listing available voices...\n")
    await list_available_voices()

    print("\n" + "=" * 60 + "\n")

    # Test 2: Generate single TTS
    await test_single_agent_tts()

    print("\n" + "=" * 60 + "\n")

    # Test 3: Multi-agent conversation
    # Uncomment when you have all voice IDs configured
    # await test_multi_agent_conversation()


if __name__ == "__main__":
    asyncio.run(main())
