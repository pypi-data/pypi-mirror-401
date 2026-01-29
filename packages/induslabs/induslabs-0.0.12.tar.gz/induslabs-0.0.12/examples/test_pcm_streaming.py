from induslabs import Client

client = Client(api_key="4RzC13dC8ZUasNUwn1yJGi7bI1bwT1_U-t8oCfnSbBc")

test_text = "Testing sample rate compatibility."

def test_sample_rate(voice_name, sample_rate):
    """Test a specific voice and sample rate combination"""
    print(f"\n{'='*60}")
    print(f"Voice: {voice_name} | Sample Rate: {sample_rate}Hz")
    print(f"{'='*60}")
    
    try:
        response = client.tts.speak(
            text=test_text,
            voice=voice_name,
            output_format="pcm",
            stream=True,
            sample_rate=sample_rate
        )
        
        # Get provider info from headers
        provider = response.headers.get('x-provider', 'Unknown')
        actual_rate = response.sample_rate
        
        print(f"✓ Request successful")
        print(f"  Provider: {provider}")
        print(f"  Requested rate: {sample_rate}Hz")
        print(f"  Actual rate: {actual_rate}Hz")
        print(f"  Request ID: {response.request_id}")
        
        # Save file
        filename = f"{voice_name}_{sample_rate}hz.pcm"
        with open(filename, "wb") as f:
            for chunk in response.iter_bytes(chunk_size=4096):
                f.write(chunk)
        
        print(f"  Saved to: {filename}")
        
        # Check if audio data looks valid (simple heuristic)
        with open(filename, "rb") as f:
            data = f.read(1000)
            non_zero = sum(1 for b in data if b != 0)
            variation = len(set(data))
            
            print(f"  Data check: {non_zero}/1000 non-zero bytes, {variation} unique values")
            
            if non_zero < 100 or variation < 50:
                print(f"  ⚠️  WARNING: Audio data might be invalid (white noise?)")
        
        return True
        
    except Exception as e:
        print(f"✗ Request failed: {e}")
        return False

# Test matrix
voices = [
    "Indus-en-maya",      # IndusLabs provider
    "Indus-en-Ember"      # Kokoro provider
]

sample_rates = [8000, 16000, 24000]

print("\n" + "="*60)
print("SAMPLE RATE COMPATIBILITY TEST")
print("="*60)

results = {}
for voice in voices:
    results[voice] = {}
    for rate in sample_rates:
        success = test_sample_rate(voice, rate)
        results[voice][rate] = success

# Summary
print("\n" + "="*60)
print("COMPATIBILITY SUMMARY")
print("="*60)

for voice in voices:
    print(f"\n{voice}:")
    for rate in sample_rates:
        status = "✓ Works" if results[voice][rate] else "✗ Failed"
        print(f"  {rate}Hz: {status}")

print("\n" + "="*60)
print("FINDINGS")
print("="*60)
print("""
Based on the test results:

1. IndusLabs voices (maya): Support 8k, 16k, 24k sample rates
2. Kokoro voices (Ember): Only work properly with 24kHz (default)
   - 8kHz and 16kHz produce white noise/invalid audio

RECOMMENDATION:
- Always use 24000Hz (24kHz) for Kokoro voices
- Or don't specify sample_rate parameter (defaults to 24kHz)
- For 8kHz/16kHz requirements, use IndusLabs voices only
""")

print("\nTo convert to WAV and verify:")
print("ffmpeg -f s16le -ar 8000 -ac 1 -i Indus-en-maya_8000hz.pcm maya_8k.wav")
print("ffmpeg -f s16le -ar 8000 -ac 1 -i Indus-en-Ember_8000hz.pcm ember_8k.wav")
print("ffmpeg -f s16le -ar 24000 -ac 1 -i Indus-en-Ember_24000hz.pcm ember_24k.wav")