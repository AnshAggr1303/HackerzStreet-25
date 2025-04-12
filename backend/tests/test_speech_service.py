import asyncio
import argparse
import os
from speech_service import SpeechService  # adjust the import if needed

async def main():
    # Set up command-line arguments.
    parser = argparse.ArgumentParser(description="Test SpeechService with an input MP3 file.")
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the input MP3 file for speech-to-text conversion."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="tts_output.mp3",
        help="(Optional) Path where the TTS output MP3 file will be saved."
    )
    args = parser.parse_args()

    # Ensure the input file exists.
    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}")
        return

    # Read the input MP3 file as bytes.
    with open(args.input, "rb") as f:
        audio_content = f.read()

    # Create an instance of the SpeechService.
    service = SpeechService()

    # Test the speech_to_text function.
    try:
        print("Converting speech to text...")
        transcription = await service.speech_to_text(audio_content)
        print("Transcription Result:")
        print(transcription)
    except Exception as e:
        print(f"Error during speech-to-text: {e}")
        return

    # Test the text_to_speech function.
    try:
        # Use the transcription if available, otherwise use a default message.
        tts_text = transcription if transcription.strip() else "Hello, this is a test."
        print("Generating text-to-speech audio...")
        tts_audio = await service.text_to_speech(tts_text, "en")

        # Save the TTS output to a file.
        with open(args.output, "wb") as out_file:
            out_file.write(tts_audio)
        print(f"TTS audio saved to {args.output}")
    except Exception as e:
        print(f"Error during text-to-speech: {e}")

if __name__ == "__main__":
    asyncio.run(main())