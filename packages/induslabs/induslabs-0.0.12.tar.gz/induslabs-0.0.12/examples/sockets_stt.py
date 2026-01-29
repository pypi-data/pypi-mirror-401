"""
Speech-to-Text Examples - WebSocket Streaming with Model and Streaming Parameters
Enhanced with Time to First Byte (TTFB) Measurements
"""
import os
import asyncio
import warnings
import time
from induslabs import Client, STTSegment


# --- NEW ERROR HANDLING FUNCTION ---
def handle_expected_error(func, *args, **kwargs):
    """Helper to catch expected ValueErrors due to validation."""
    try:
        func(*args, **kwargs)
        print("  ❌ Test Failed: Expected ValueError was not raised.")
    except ValueError as e:
        print(f"  ✅ Caught expected error: {e}")
    except Exception as e:
        print(f"  ❌ Caught unexpected exception: {e}")
# --- END NEW ERROR HANDLING FUNCTION ---


class TTFBTracker:
    """Helper class to track Time to First Byte"""
    def __init__(self):
        self.start_time = None
        self.first_byte_time = None
        self.ttfb = None
    
    def start(self):
        """Mark the start of the request"""
        self.start_time = time.time()
        self.first_byte_time = None
        self.ttfb = None
    
    def record_first_byte(self):
        """Record when first byte/segment is received"""
        if self.first_byte_time is None and self.start_time is not None:
            self.first_byte_time = time.time()
            self.ttfb = self.first_byte_time - self.start_time
    
    def get_ttfb_ms(self):
        """Get TTFB in milliseconds"""
        return self.ttfb * 1000 if self.ttfb is not None else None


def main():
    # client needs to be created without 'async with' to run synchronous examples
    client = Client()

    # Example 1: Basic transcription with indus-stt-v1 model + TTFB
    print("Example 1: Basic Transcription (Indus-STT-V1 Model) with TTFB")
    print("=" * 60)
    
    audio_file = "test_audio.wav"
    
    if os.path.exists(audio_file):
        ttfb_tracker = TTFBTracker()
        
        def on_segment_ttfb(segment: STTSegment):
            ttfb_tracker.record_first_byte()
        
        ttfb_tracker.start()
        result = client.stt.transcribe(
            file=audio_file,
            model="indus-stt-v1",
            streaming=False,
            noise_cancellation=True,
            on_segment=on_segment_ttfb
        )
        
        print(f"Transcription: {result.text}")
        print(f"\nDetailed Information:")
        print(f"  Request ID: {result.request_id}")
        print(f"  Model: indus-stt-v1")
        print(f"  Streaming: False")
        print(f"  Noise Cancellation: True")
        if ttfb_tracker.get_ttfb_ms():
            print(f"  ⏱️  Time to First Byte: {ttfb_tracker.get_ttfb_ms():.2f}ms")
        if result.metrics:
            print(f"  Audio Duration: {result.metrics.buffer_duration:.2f}s")
            print(f"  Processing Time: {result.metrics.transcription_time:.2f}s")
            print(f"  Total Time: {result.metrics.total_time:.2f}s")
            print(f"  Real-time Factor (RTF): {result.metrics.rtf:.3f}")
    else:
        print(f"Audio file '{audio_file}' not found.")
        print("Creating a sample audio file using TTS...")
        
        # Create sample audio
        tts_response = client.tts.speak(
            text="यह एक टेस्ट है। भाषण से पाठ रूपांतरण का परीक्षण।",
            voice="Indus-hi-Urvashi",
        )
        tts_response.save(audio_file)
        print(f"Created {audio_file}")
        
        # Now transcribe with TTFB tracking
        ttfb_tracker = TTFBTracker()
        
        def on_segment_ttfb(segment: STTSegment):
            ttfb_tracker.record_first_byte()
        
        ttfb_tracker.start()
        result = client.stt.transcribe(
            file=audio_file,
            model="indus-stt-v1",
            streaming=False,
            noise_cancellation=True,
            on_segment=on_segment_ttfb
        )
        
        print(f"\nTranscription: {result.text}")
        if ttfb_tracker.get_ttfb_ms():
            print(f"⏱️  Time to First Byte: {ttfb_tracker.get_ttfb_ms():.2f}ms")

    # Example 2: Transcription with indus-stt-hi-en model + TTFB
    print("\n\nExample 2: Transcription with Indus-STT-Hi-En Model + TTFB")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        ttfb_tracker = TTFBTracker()
        
        def on_segment_ttfb(segment: STTSegment):
            ttfb_tracker.record_first_byte()
        
        ttfb_tracker.start()
        result = client.stt.transcribe(
            file=audio_file,
            model="indus-stt-hi-en",
            streaming=False,
            noise_cancellation=True,
            language="hindi",
            on_segment=on_segment_ttfb
        )
        
        print(f"Transcription: {result.text}")
        print(f"Model: indus-stt-hi-en")
        print(f"Language: hindi")
        print(f"Noise Cancellation: True")
        if ttfb_tracker.get_ttfb_ms():
            print(f"⏱️  Time to First Byte: {ttfb_tracker.get_ttfb_ms():.2f}ms")
        if result.metrics:
            print(f"Processing time: {result.metrics.transcription_time:.2f}s")

    # Example 3: Streaming mode with indus-stt-v1 model (NOW EXPECTED TO FAIL)
    print("\n\nExample 3: Streaming Mode with Indus-STT-V1 Model (Testing Validation)")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        print("Attempting to transcribe with streaming=True and model='indus-stt-v1'...")
        
        def on_segment(segment: STTSegment):
            print(f"  📝 Segment: '{segment.text}'")
        
        handle_expected_error(
            client.stt.transcribe,
            file=audio_file,
            model="indus-stt-v1",
            streaming=True,
            on_segment=on_segment
        )

    # Example 4: Streaming mode with indus-stt-hi-en model (VALID) + TTFB
    print("\n\nExample 4: Streaming Mode with Indus-STT-Hi-En Model (VALID) + TTFB")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        print("Transcribing with indus-stt-hi-en model and streaming...\n")
        
        ttfb_tracker = TTFBTracker()
        
        def on_segment(segment: STTSegment):
            ttfb_tracker.record_first_byte()
            print(f"  📝 [{segment.start:.2f}s] {segment.text}")
        
        ttfb_tracker.start()
        result = client.stt.transcribe(
            file=audio_file,
            model="indus-stt-hi-en",
            streaming=True,
            language="hindi",
            on_segment=on_segment
        )
        
        print(f"\n✅ Complete: {result.text}")
        print(f"Model: indus-stt-hi-en, Streaming: True")
        if ttfb_tracker.get_ttfb_ms():
            print(f"⏱️  Time to First Byte: {ttfb_tracker.get_ttfb_ms():.2f}ms")
        if result.metrics:
            print(f"RTF: {result.metrics.rtf:.3f}")

    # Example 5: Comparing models with TTFB
    print("\n\nExample 5: Comparing Indus-STT-V1 vs Indus-STT-Hi-En Model with TTFB")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        print("Testing with indus-stt-v1 model (non-streaming)...")
        ttfb_tracker1 = TTFBTracker()
        
        def on_segment1(segment: STTSegment):
            ttfb_tracker1.record_first_byte()
        
        ttfb_tracker1.start()
        result_default = client.stt.transcribe(
            file=audio_file,
            model="indus-stt-v1",
            streaming=False,
            noise_cancellation=True,
            on_segment=on_segment1
        )
        
        print("Testing with indus-stt-hi-en model (streaming)...")
        ttfb_tracker2 = TTFBTracker()
        
        def on_segment2(segment: STTSegment):
            ttfb_tracker2.record_first_byte()
        
        ttfb_tracker2.start()
        result_hien = client.stt.transcribe(
            file=audio_file,
            model="indus-stt-hi-en",
            streaming=True,
            language="hindi",
            on_segment=on_segment2
        )
        
        print("\nComparison Results:")
        print(f"  Indus-STT-V1 Model: {result_default.text}")
        if ttfb_tracker1.get_ttfb_ms():
            print(f"    ⏱️  TTFB: {ttfb_tracker1.get_ttfb_ms():.2f}ms")
        if result_default.metrics:
            print(f"    RTF: {result_default.metrics.rtf:.3f}")
        
        print(f"\n  Indus-STT-Hi-En Model: {result_hien.text}")
        if ttfb_tracker2.get_ttfb_ms():
            print(f"    ⏱️  TTFB: {ttfb_tracker2.get_ttfb_ms():.2f}ms")
        if result_hien.metrics:
            print(f"    RTF: {result_hien.metrics.rtf:.3f}")

    # Example 6: All parameter combinations with TTFB
    print("\n\nExample 6: Testing All Parameter Combinations (Valid/Invalid) with TTFB")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        combinations = [
            ("indus-stt-v1", False, False, "Valid - Non-Streaming"),
            ("indus-stt-v1", False, True, "Valid - Non-Streaming + Noise Cancellation"),
            ("indus-stt-v1", True, False, "Invalid - Streaming=True requires indus-stt-hi-en"),
            ("indus-stt-v1", True, True, "Invalid - Streaming=True requires indus-stt-hi-en"),
            ("indus-stt-hi-en", False, False, "Valid - Non-Streaming"),
            ("indus-stt-hi-en", False, True, "Valid - Non-Streaming + Noise Cancellation"),
            ("indus-stt-hi-en", True, False, "Valid - Streaming"),
            ("indus-stt-hi-en", True, True, "Warning - Streaming + Noise Cancellation"),
        ]

        for model, streaming, noise_cancellation, status in combinations:
            print(
                f"\nTesting: model={model}, streaming={streaming}, noise_cancellation={noise_cancellation} ({status})"
            )

            if status.startswith("Invalid"):
                handle_expected_error(
                    client.stt.transcribe,
                    file=audio_file,
                    model=model,
                    streaming=streaming,
                    noise_cancellation=noise_cancellation,
                    language="hindi" if model == "indus-stt-hi-en" else None,
                )
            else:
                language = "hindi" if model == "indus-stt-hi-en" else None
                ttfb_tracker = TTFBTracker()
                
                def on_segment_ttfb(segment: STTSegment):
                    ttfb_tracker.record_first_byte()
                
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter("always")
                    ttfb_tracker.start()
                    result = client.stt.transcribe(
                        file=audio_file,
                        model=model,
                        streaming=streaming,
                        noise_cancellation=noise_cancellation,
                        language=language,
                        on_segment=on_segment_ttfb
                    )

                if caught:
                    for warn in caught:
                        print(f"  ⚠️ Warning: {warn.message}")

                print(f"  Result: {result.text[:50]}...")
                if ttfb_tracker.get_ttfb_ms():
                    print(f"  ⏱️  TTFB: {ttfb_tracker.get_ttfb_ms():.2f}ms")
                if result.metrics:
                    print(f"  RTF: {result.metrics.rtf:.3f}")

    # Example 7: Custom chunk size with streaming + TTFB
    print("\n\nExample 7: Custom Chunk Size with Streaming + TTFB")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        ttfb_tracker = TTFBTracker()
        
        def on_segment_ttfb(segment: STTSegment):
            ttfb_tracker.record_first_byte()
            print(f"  📝 {segment.text}")
        
        ttfb_tracker.start()
        result = client.stt.transcribe(
            file=audio_file,
            model="indus-stt-hi-en",
            streaming=True,
            chunk_size=4096,
            language="hindi",
            on_segment=on_segment_ttfb
        )
        
        print(f"\n✅ Complete: {result.text}")
        print(f"Segments received: {len(result.segments)}")
        if ttfb_tracker.get_ttfb_ms():
            print(f"⏱️  Time to First Byte: {ttfb_tracker.get_ttfb_ms():.2f}ms")


async def async_examples():
    """Async examples with model and streaming parameters + TTFB"""
    
    print("\n\n" + "=" * 60)
    print("ASYNC EXAMPLES WITH MODEL & STREAMING PARAMETERS + TTFB")
    print("=" * 60)
    
    async with Client() as client:
        audio_file = "test_audio.wav"
        
        if not os.path.exists(audio_file):
            print(f"Audio file '{audio_file}' not found. Skipping async examples.")
            return
        
        # Example 8: Async with indus-stt-v1 model + TTFB
        print("\nExample 8: Async with Indus-STT-V1 Model + TTFB")
        print("-" * 60)
        
        ttfb_tracker = TTFBTracker()
        
        def on_segment_ttfb(segment: STTSegment):
            ttfb_tracker.record_first_byte()
        
        ttfb_tracker.start()
        result = await client.stt.transcribe_async(
            audio_file,
            model="indus-stt-v1",
            streaming=False,
            noise_cancellation=True,
            on_segment=on_segment_ttfb
        )
        
        print(f"Transcription: {result.text}")
        print(f"Model: indus-stt-v1, Streaming: False")
        if ttfb_tracker.get_ttfb_ms():
            print(f"⏱️  Time to First Byte: {ttfb_tracker.get_ttfb_ms():.2f}ms")
        if result.metrics:
            print(f"Processing time: {result.metrics.transcription_time:.2f}s")
        
        # Example 9: Async with hi-en model and streaming + TTFB
        print("\nExample 9: Async with Indus-STT-Hi-En Model and Streaming + TTFB")
        print("-" * 60)
        
        segments_received = []
        ttfb_tracker = TTFBTracker()
        
        def on_segment(segment: STTSegment):
            ttfb_tracker.record_first_byte()
            segments_received.append(segment)
            print(f"  📝 Segment: '{segment.text}'")
        
        ttfb_tracker.start()
        result = await client.stt.transcribe_async(
            audio_file,
            model="indus-stt-hi-en",
            streaming=True,
            language="hindi",
            on_segment=on_segment
        )
        
        print(f"\n✅ Complete: {result.text}")
        print(f"Model: indus-stt-hi-en, Streaming: True")
        if ttfb_tracker.get_ttfb_ms():
            print(f"⏱️  Time to First Byte: {ttfb_tracker.get_ttfb_ms():.2f}ms")
        print(f"Total segments: {len(segments_received)}")
        
        # Example 10: Parallel transcriptions with different models + TTFB
        print("\nExample 10: Parallel Async Transcriptions (Different Models) + TTFB")
        print("-" * 60)
        
        ttfb_trackers = [TTFBTracker(), TTFBTracker(), TTFBTracker()]
        
        def make_callback(tracker):
            def callback(segment: STTSegment):
                tracker.record_first_byte()
            return callback
        
        tasks = []
        
        # Valid: indus-stt-v1 (no stream)
        ttfb_trackers[0].start()
        tasks.append(
            client.stt.transcribe_async(
                audio_file,
                model="indus-stt-v1",
                streaming=False,
                noise_cancellation=True,
                on_segment=make_callback(ttfb_trackers[0])
            )
        )
        
        # Valid: indus-stt-hi-en (no stream)
        ttfb_trackers[1].start()
        tasks.append(
            client.stt.transcribe_async(
                audio_file,
                model="indus-stt-hi-en",
                streaming=False,
                noise_cancellation=True,
                language="hindi",
                on_segment=make_callback(ttfb_trackers[1])
            )
        )
        
        # Valid: indus-stt-hi-en (stream)
        ttfb_trackers[2].start()
        tasks.append(
            client.stt.transcribe_async(
                audio_file,
                model="indus-stt-hi-en",
                streaming=True,
                language="hindi",
                on_segment=make_callback(ttfb_trackers[2])
            )
        )
        
        results = await asyncio.gather(*tasks)
        
        models = ["indus-stt-v1 (no stream)", "indus-stt-hi-en (no stream)", "indus-stt-hi-en (stream)"]
        for i, (result, model_desc, tracker) in enumerate(zip(results, models, ttfb_trackers), 1):
            print(f"  Result {i} ({model_desc}): {result.text[:40]}...")
            if tracker.get_ttfb_ms():
                print(f"    ⏱️  TTFB: {tracker.get_ttfb_ms():.2f}ms")
            if result.metrics:
                print(f"    RTF: {result.metrics.rtf:.3f}")


def streaming_comparison():
    """Compare streaming vs non-streaming modes with TTFB"""
    
    print("\n\n" + "=" * 60)
    print("STREAMING VS NON-STREAMING COMPARISON + TTFB")
    print("=" * 60)
    
    client = Client()
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found.")
        return
    
    # Non-Streaming (Valid with indus-stt-v1)
    print("Testing Non-Streaming Mode (Model: indus-stt-v1)...")
    segment_count_nonstream = 0
    ttfb_tracker1 = TTFBTracker()
    
    def callback_nonstream(segment: STTSegment):
        nonlocal segment_count_nonstream
        ttfb_tracker1.record_first_byte()
        segment_count_nonstream += 1
    
    ttfb_tracker1.start()
    result_nonstream = client.stt.transcribe(
        audio_file,
        model="indus-stt-v1",
        streaming=False,
        noise_cancellation=True,
        on_segment=callback_nonstream
    )
    
    print(f"  Segments: {segment_count_nonstream}")
    if ttfb_tracker1.get_ttfb_ms():
        print(f"  ⏱️  TTFB: {ttfb_tracker1.get_ttfb_ms():.2f}ms")
    if result_nonstream.metrics:
        print(f"  RTF: {result_nonstream.metrics.rtf:.3f}")
    
    # Streaming (Valid with hi-en)
    print("\nTesting Streaming Mode (Model: indus-stt-hi-en)...")
    segment_count_stream = 0
    ttfb_tracker2 = TTFBTracker()
    
    def callback_stream(segment: STTSegment):
        nonlocal segment_count_stream
        ttfb_tracker2.record_first_byte()
        segment_count_stream += 1
        print(f"  📝 Segment {segment_count_stream}: {segment.text}")
    
    ttfb_tracker2.start()
    result_stream = client.stt.transcribe(
        audio_file,
        model="indus-stt-hi-en",
        streaming=True,
        language="hindi",
        on_segment=callback_stream
    )
    
    print(f"\n  Total segments: {segment_count_stream}")
    if ttfb_tracker2.get_ttfb_ms():
        print(f"  ⏱️  TTFB: {ttfb_tracker2.get_ttfb_ms():.2f}ms")
    if result_stream.metrics:
        print(f"  RTF: {result_stream.metrics.rtf:.3f}")
    
    print("\nComparison:")
    print(f"  Non-Streaming (indus-stt-v1):")
    print(f"    Segments: {segment_count_nonstream}")
    if ttfb_tracker1.get_ttfb_ms():
        print(f"    TTFB: {ttfb_tracker1.get_ttfb_ms():.2f}ms")
    
    print(f"  Streaming (indus-stt-hi-en):")
    print(f"    Segments: {segment_count_stream}")
    if ttfb_tracker2.get_ttfb_ms():
        print(f"    TTFB: {ttfb_tracker2.get_ttfb_ms():.2f}ms")
    
    print(f"\n  Non-streaming final text: {result_nonstream.text[:30]}...")
    print(f"  Streaming final text: {result_stream.text[:30]}...")


def model_comparison():
    """Compare indus-stt-v1 vs indus-stt-hi-en models with TTFB"""
    
    print("\n\n" + "=" * 60)
    print("MODEL COMPARISON: INDUS-STT-V1 vs INDUS-STT-HI-EN + TTFB")
    print("=" * 60)
    
    client = Client()
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found.")
        return
    
    print("Testing Indus-STT-V1 Model (Non-Streaming)...")
    ttfb_tracker1 = TTFBTracker()
    
    def callback1(segment: STTSegment):
        ttfb_tracker1.record_first_byte()
    
    start = time.time()
    ttfb_tracker1.start()
    result_default = client.stt.transcribe(
        audio_file,
        model="indus-stt-v1",
        streaming=False,
        noise_cancellation=True,
        on_segment=callback1
    )
    time_default = time.time() - start
    
    print(f"  Text: {result_default.text}")
    print(f"  Wall time: {time_default:.3f}s")
    if ttfb_tracker1.get_ttfb_ms():
        print(f"  ⏱️  TTFB: {ttfb_tracker1.get_ttfb_ms():.2f}ms")
    if result_default.metrics:
        print(f"  RTF: {result_default.metrics.rtf:.3f}")
    
    print("\nTesting Indus-STT-Hi-En Model (Non-Streaming)...")
    ttfb_tracker2 = TTFBTracker()
    
    def callback2(segment: STTSegment):
        ttfb_tracker2.record_first_byte()
    
    start = time.time()
    ttfb_tracker2.start()
    result_hien = client.stt.transcribe(
        audio_file,
        model="indus-stt-hi-en",
        streaming=False,
        noise_cancellation=True,
        language="hindi",
        on_segment=callback2
    )
    time_hien = time.time() - start
    
    print(f"  Text: {result_hien.text}")
    print(f"  Wall time: {time_hien:.3f}s")
    if ttfb_tracker2.get_ttfb_ms():
        print(f"  ⏱️  TTFB: {ttfb_tracker2.get_ttfb_ms():.2f}ms")
    if result_hien.metrics:
        print(f"  RTF: {result_hien.metrics.rtf:.3f}")
    
    print("\nSummary (Non-Streaming):")
    print(f"  Indus-STT-V1 model:")
    print(f"    Wall time: {time_default:.3f}s")
    if ttfb_tracker1.get_ttfb_ms():
        print(f"    TTFB: {ttfb_tracker1.get_ttfb_ms():.2f}ms")
    if result_default.metrics:
        print(f"    RTF: {result_default.metrics.rtf:.3f}")
    
    print(f"  Indus-STT-Hi-En model:")
    print(f"    Wall time: {time_hien:.3f}s")
    if ttfb_tracker2.get_ttfb_ms():
        print(f"    TTFB: {ttfb_tracker2.get_ttfb_ms():.2f}ms")
    if result_hien.metrics:
        print(f"    RTF: {result_hien.metrics.rtf:.3f}")


def error_handling_example():
    """Example showing error handling with new parameters"""
    
    print("\n\n" + "=" * 60)
    print("ERROR HANDLING WITH NEW PARAMETERS")
    print("=" * 60)
    
    client = Client()
    
    # Test for the new validation rule: streaming=True and model=indus-stt-v1
    print("\nTest 1: Streaming=True with model='indus-stt-v1'")
    handle_expected_error(
        client.stt.transcribe,
        "test_audio.wav",
        model="indus-stt-v1",
        streaming=True
    )

    # Example with invalid model (retained for completeness)
    print("\nTest 2: Invalid model parameter")
    handle_expected_error(
        client.stt.transcribe,
        "test_audio.wav",
        model="invalid-model",
        streaming=False
    )
    
    # Example with non-existent file
    print("\nTest 3: Non-existent file")
    try:
        result = client.stt.transcribe(
            "nonexistent.wav",
            model="indus-stt-v1",
            streaming=False
        )
        if result.has_error:
            print(f"  ℹ️  Transcription Error: {result.error}")
        else:
            print("  ❌ Test Failed: Expected error for non-existent file.")
    except Exception as e:
        print(f"  ✅ Error (expected from client/websocket): {e}")


def live_transcription_simulation():
    """Simulate live transcription with streaming enabled + TTFB"""
    
    print("\n\n" + "=" * 60)
    print("LIVE TRANSCRIPTION SIMULATION (Streaming Mode) + TTFB")
    print("=" * 60)
    
    client = Client()
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found.")
        return
    
    accumulated_text = []
    ttfb_tracker = TTFBTracker()
    
    def live_callback(segment: STTSegment):
        ttfb_tracker.record_first_byte()
        accumulated_text.append(segment.text)
        print(f"\r  Live: {' '.join(accumulated_text)}", end="", flush=True)
    
    print("Simulating live transcription with streaming=True (using indus-stt-hi-en model)...\n")
    
    ttfb_tracker.start()
    result = client.stt.transcribe(
        audio_file,
        model="indus-stt-hi-en",
        streaming=True,
        language="hindi",
        on_segment=live_callback
    )
    
    print()  # New line
    print(f"\n✅ Final: {result.text}")
    print(f"Model: indus-stt-hi-en, Streaming: True")
    if ttfb_tracker.get_ttfb_ms():
        print(f"⏱️  Time to First Byte: {ttfb_tracker.get_ttfb_ms():.2f}ms")


def performance_metrics_with_params():
    """Example focusing on performance metrics with different parameters + TTFB"""
    
    print("\n\n" + "=" * 60)
    print("PERFORMANCE METRICS WITH DIFFERENT PARAMETERS + TTFB")
    print("=" * 60)
    
    client = Client()
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found.")
        return
    
    configs = [
        ("indus-stt-v1", False, None, True),
        ("indus-stt-hi-en", False, "hindi", True),
        ("indus-stt-hi-en", True, "hindi", False),
        ("indus-stt-hi-en", True, "hindi", True),
    ]
    
    print(f"\n{'Model':<12} {'Streaming':<10} {'NoiseCancel':<13} {'Wall Time':<12} {'TTFB':<10} {'RTF':<8} {'Result'}")
    print("-" * 90)
    
    for model, streaming, language, noise_cancellation in configs:
        ttfb_tracker = TTFBTracker()
        
        def callback(segment: STTSegment):
            ttfb_tracker.record_first_byte()
        
        start_time = time.time()
        ttfb_tracker.start()
        
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = client.stt.transcribe(
                audio_file,
                model=model,
                streaming=streaming,
                noise_cancellation=noise_cancellation,
                language=language,
                on_segment=callback
            )
        
        wall_time = time.time() - start_time
        
        if caught:
            for warn in caught:
                print(f"  ⚠️ Warning ({model}): {warn.message}")
        
        rtf_str = f"{result.metrics.rtf:.3f}" if result.metrics else "N/A"
        ttfb_str = f"{ttfb_tracker.get_ttfb_ms():.0f}ms" if ttfb_tracker.get_ttfb_ms() else "N/A"
        text_preview = result.text[:25] + "..." if len(result.text) > 25 else result.text
        
        print(
            f"{model:<12} {str(streaming):<10} {str(noise_cancellation):<13} "
            f"{wall_time:<12.3f} {ttfb_str:<10} {rtf_str:<8} {text_preview}"
        )
    
    print("\nInterpretation:")
    print("  - TTFB: Time to First Byte (lower is better, especially for streaming)")
    print("  - RTF < 1.0: Faster than real-time")
    print("  - RTF > 1.0: Slower than real-time")
    print("  - Streaming mode is typically for real-time applications.")


def comprehensive_test():
    """Comprehensive test of all scenarios with TTFB"""
    
    print("\n\n" + "=" * 60)
    print("COMPREHENSIVE TEST: ALL SCENARIOS + TTFB")
    print("=" * 60)
    
    client = Client()
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found.")
        print("Please create test_audio.wav first.")
        return
    
    scenarios = [
        ("Indus-STT-V1 / Non-Streaming", "indus-stt-v1", False, None, True, True),
        ("Indus-STT-V1 / Streaming", "indus-stt-v1", True, None, False, False),  # Invalid
        ("Indus-STT-Hi-En / Non-Streaming", "indus-stt-hi-en", False, "hindi", True, True),
        ("Indus-STT-Hi-En / Streaming", "indus-stt-hi-en", True, "hindi", True, False),
        (
            "Indus-STT-Hi-En / Streaming + Noise Cancellation",
            "indus-stt-hi-en",
            True,
            "hindi",
            True,
            True,
        ),
    ]
    
    results = {}
    
    for name, model, streaming, language, is_valid, noise_cancellation in scenarios:
        print(f"\n--- Testing: {name} ---")
        
        if not is_valid:
            handle_expected_error(
                client.stt.transcribe,
                audio_file,
                model=model,
                streaming=streaming,
                noise_cancellation=noise_cancellation,
                language=language
            )
            continue
        
        segment_count = 0
        ttfb_tracker = TTFBTracker()
        
        def count_segments(s):
            nonlocal segment_count
            ttfb_tracker.record_first_byte()
            segment_count += 1
        
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            ttfb_tracker.start()
            result = client.stt.transcribe(
                audio_file,
                model=model,
                streaming=streaming,
                noise_cancellation=noise_cancellation,
                language=language,
                on_segment=count_segments
            )
        
        if caught:
            for warn in caught:
                print(f"  ⚠️ Warning: {warn.message}")
        
        results[name] = {
            'text': result.text,
            'segments': segment_count,
            'rtf': result.metrics.rtf if result.metrics else None,
            'ttfb_ms': ttfb_tracker.get_ttfb_ms(),
            'noise_cancellation': noise_cancellation,
        }
        
        print(f"  ✅ Segments: {segment_count}")
        if ttfb_tracker.get_ttfb_ms():
            print(f"  ✅ TTFB: {ttfb_tracker.get_ttfb_ms():.2f}ms")
        print(f"  ✅ Text: {result.text[:50]}...")
        if result.metrics:
            print(f"  ✅ RTF: {result.metrics.rtf:.3f}")
    
    print("\n" + "=" * 60)
    print("SUMMARY OF VALID SCENARIOS")
    print("=" * 60)
    
    for name, data in results.items():
        if data['rtf'] is not None:  # Only show valid scenarios that completed
            print(f"\n{name}:")
            print(f"  Segments: {data['segments']}")
            if data['ttfb_ms']:
                print(f"  TTFB: {data['ttfb_ms']:.2f}ms")
            print(f"  RTF: {data['rtf']:.3f}")
            print(f"  Noise cancellation: {data['noise_cancellation']}")
            print(f"  Text length: {len(data['text'])} chars")


if __name__ == "__main__":
    # Run synchronous examples
    main()
    
    # Run async examples
    asyncio.run(async_examples())
    
    # Additional comparison examples
    streaming_comparison()
    model_comparison()
    error_handling_example()
    live_transcription_simulation()
    performance_metrics_with_params()
    comprehensive_test()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)