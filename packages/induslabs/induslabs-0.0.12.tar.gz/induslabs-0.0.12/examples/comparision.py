from induslabs import Client
import json

# Initialize the client
client = Client(api_key="4RzC13dC8ZUasNUwn1yJGi7bI1bwT1_U-t8oCfnSbBc")

# Test text
test_text = "Hello, this is a test of the voice in PCM format with streaming enabled."

def test_voice(voice_name):
    print(f"\n{'='*60}")
    print(f"Testing Voice: {voice_name}")
    print(f"{'='*60}")
    
    try:
        # Generate speech
        response = client.tts.speak(
            text=test_text,
            voice=voice_name,
            output_format="pcm",
            stream=True,
            sample_rate=8000
        )
        
        # Collect response data
        chunks = []
        total_bytes = 0
        
        with open(f"output_{voice_name}.pcm", "wb") as f:
            for i, chunk in enumerate(response.iter_bytes(chunk_size=4096)):
                f.write(chunk)
                chunks.append(len(chunk))
                total_bytes += len(chunk)
                print(f"Chunk {i+1}: {len(chunk)} bytes")
        
        # Print detailed response information
        print(f"\n--- Response Details ---")
        print(f"Voice: {voice_name}")
        print(f"Format: {response.format}")
        print(f"Sample Rate: {response.sample_rate}Hz")
        print(f"Channels: {response.channels}")
        print(f"Request ID: {response.request_id}")
        print(f"Total Chunks: {len(chunks)}")
        print(f"Total Bytes: {total_bytes}")
        print(f"Chunk Sizes: {chunks}")
        
        # Try to access any additional attributes
        print(f"\n--- All Response Attributes ---")
        for attr in dir(response):
            if not attr.startswith('_'):
                try:
                    value = getattr(response, attr)
                    if not callable(value):
                        print(f"{attr}: {value}")
                except Exception as e:
                    print(f"{attr}: [Error accessing: {e}]")
        
        print(f"\n✓ SUCCESS: {voice_name} completed")
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {voice_name} failed")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        print(f"Full Error: {repr(e)}")
        
        # Try to get more error details
        if hasattr(e, '__dict__'):
            print(f"Error Attributes: {e.__dict__}")
        
        return False

# Test both voices
maya_success = test_voice("Indus-en-maya")
ember_success = test_voice("Indus-en-Ember")

# Summary
print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
print(f"Indus-en-maya: {'✓ SUCCESS' if maya_success else '✗ FAILED'}")
print(f"Indus-en-Ember: {'✓ SUCCESS' if ember_success else '✗ FAILED'}")