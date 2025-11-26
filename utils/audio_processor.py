"""
Audio Processing Utilities
Handles audio file conversion and preprocessing for Google Speech Recognition
"""

import io
import os
import wave
import tempfile
from typing import Optional, Tuple

# Try to import pydub for format conversion (requires FFmpeg)
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False


class AudioProcessor:
    """Handles audio file processing and conversion."""
    
    # WAV is always supported, others need FFmpeg
    SUPPORTED_FORMATS = ['wav', 'mp3', 'm4a', 'ogg', 'flac', 'webm']
    WAV_ONLY_FORMATS = ['wav']
    TARGET_SAMPLE_RATE = 16000
    TARGET_CHANNELS = 1
    
    @staticmethod
    def convert_to_wav(audio_data: bytes, source_format: str = 'm4a') -> Tuple[bytes, str]:
        """
        Convert audio data to WAV format suitable for Google Speech Recognition.
        
        Args:
            audio_data: Raw audio bytes
            source_format: Original audio format
            
        Returns:
            Tuple of (wav_bytes, temp_file_path)
        """
        # If already WAV, just write to temp file
        if source_format.lower() == 'wav':
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                return audio_data, temp_file.name
        
        # For other formats, try pydub (requires FFmpeg)
        if not PYDUB_AVAILABLE:
            raise Exception(
                f"Cannot convert {source_format} to WAV. "
                "Please upload WAV format directly, or ensure FFmpeg is installed on the server."
            )
        
        try:
            # Create temp file for input
            with tempfile.NamedTemporaryFile(suffix=f'.{source_format}', delete=False) as temp_input:
                temp_input.write(audio_data)
                temp_input_path = temp_input.name
            
            # Load audio with pydub
            audio = AudioSegment.from_file(temp_input_path, format=source_format)
            
            # Convert to mono and set sample rate for better recognition
            audio = audio.set_channels(AudioProcessor.TARGET_CHANNELS)
            audio = audio.set_frame_rate(AudioProcessor.TARGET_SAMPLE_RATE)
            
            # Export to WAV
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_output:
                audio.export(temp_output.name, format='wav')
                temp_output_path = temp_output.name
            
            # Read WAV bytes
            with open(temp_output_path, 'rb') as f:
                wav_bytes = f.read()
            
            # Cleanup input temp file
            os.unlink(temp_input_path)
            
            return wav_bytes, temp_output_path
            
        except Exception as e:
            # Cleanup on error
            if 'temp_input_path' in locals():
                try:
                    os.unlink(temp_input_path)
                except:
                    pass
            raise Exception(f"Audio conversion failed: {str(e)}")
    
    @staticmethod
    def get_audio_duration(audio_data: bytes, format: str = 'wav') -> float:
        """
        Get duration of audio in seconds.
        
        Args:
            audio_data: Audio bytes
            format: Audio format
            
        Returns:
            Duration in seconds
        """
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_data), format=format)
            return len(audio) / 1000.0  # Convert ms to seconds
        except:
            return 0.0
    
    @staticmethod
    def normalize_audio(audio_data: bytes, format: str = 'wav') -> bytes:
        """
        Normalize audio levels for better recognition.
        
        Args:
            audio_data: Audio bytes
            format: Audio format
            
        Returns:
            Normalized audio bytes
        """
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_data), format=format)
            
            # Normalize to -20 dBFS
            change_in_dBFS = -20.0 - audio.dBFS
            normalized = audio.apply_gain(change_in_dBFS)
            
            # Export back to bytes
            buffer = io.BytesIO()
            normalized.export(buffer, format=format)
            return buffer.getvalue()
            
        except Exception as e:
            # Return original if normalization fails
            return audio_data
    
    @staticmethod
    def cleanup_temp_file(file_path: str) -> None:
        """Remove temporary file if it exists."""
        try:
            if file_path and os.path.exists(file_path):
                os.unlink(file_path)
        except:
            pass
