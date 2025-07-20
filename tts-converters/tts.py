#!/usr/bin/env python3
"""
Robust Gemini Text-to-Speech Converter
Enhanced version with comprehensive error handling, logging, and debugging features
"""

import os
import sys
import time
import wave
import base64
import logging
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime

# Import required libraries with error handling
try:
    from google import genai
    from google.genai import types
    from google.genai.errors import ClientError, APIError
except ImportError as e:
    print("❌ Required libraries not found! Install them:")
    print("pip install google-genai")
    print(f"Import error: {e}")
    sys.exit(1)

# Enhanced logging configuration
def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup comprehensive logging with file and console output"""
    
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("Gemini_TTS_Converter")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # File handler
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"gemini_tts_{timestamp}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"📝 Log file created: {log_file}")
    return logger

class RobustGeminiTTSConverter:
    """Enhanced Gemini TTS converter with robust error handling"""
    
    def __init__(self, api_key: str, input_folder: str, voice_name: str = "Zephyr"):
        self.api_key = api_key.strip()
        self.input_folder = Path(input_folder)
        self.voice_name = voice_name
        self.logger = setup_logging()
        self.client = None
        
        # Conversion statistics
        self.conversion_stats = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'start_time': time.time(),
            'total_audio_size': 0
        }
        
        # Audio configuration
        self.audio_config = {
            'channels': 1,
            'sample_rate': 24000,
            'sample_width': 2,
            'format': 'PCM'
        }
        
        # Supported voice names
        self.supported_voices = [
            'Zephyr', 'Aoede', 'Charon', 'Fenrir', 'Puck'
        ]
        
        self.validate_setup()
    
    def validate_setup(self) -> None:
        """Validate initial setup and configuration"""
        self.logger.info("🚀 Gemini TTS Converter شروع ہو رہا ہے...")
        
        # Validate API key
        if not self.api_key:
            self.logger.error("❌ API key نہیں دی گئی!")
            raise ValueError("API key is required")
        
        if len(self.api_key) < 30:  # Basic API key format check
            self.logger.warning("⚠️ API key کا format suspicious لگ رہا ہے")
        
        # Validate input folder
        if not self.input_folder.exists():
            self.logger.error(f"❌ Input folder موجود نہیں: {self.input_folder}")
            raise FileNotFoundError(f"Input folder not found: {self.input_folder}")
        
        if not self.input_folder.is_dir():
            self.logger.error(f"❌ Input path فولڈر نہیں ہے: {self.input_folder}")
            raise NotADirectoryError(f"Input path is not a directory: {self.input_folder}")
        
        # Validate voice name
        if self.voice_name not in self.supported_voices:
            self.logger.warning(f"⚠️ Voice '{self.voice_name}' may not be supported")
            self.logger.info(f"Supported voices: {', '.join(self.supported_voices)}")
        
        # Initialize Gemini client
        self.initialize_client()
        
        self.logger.info(f"📁 Input folder: {self.input_folder.resolve()}")
        self.logger.info(f"🎤 Voice: {self.voice_name}")
        self.logger.info(f"🎵 Audio config: {self.audio_config}")
    
    def initialize_client(self) -> None:
        """Initialize Gemini client with error handling"""
        try:
            self.logger.info("🔗 Initializing Gemini client...")
            self.client = genai.Client(api_key=self.api_key)
            self.logger.info("✅ Gemini client initialized successfully")
            
            # Test API connection
            self.test_api_connection()
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Gemini client: {str(e)}")
            raise
    
    def test_api_connection(self) -> bool:
        """Test Gemini API connectivity with a small request"""
        try:
            self.logger.info("🔗 Testing API connectivity...")
            
            # Test with minimal content
            test_response = self.client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents="test",
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=self.voice_name,
                            )
                        )
                    ),
                )
            )
            
            if test_response and test_response.candidates:
                self.logger.info("✅ API connectivity test successful")
                return True
            else:
                self.logger.error("❌ API test returned empty response")
                return False
                
        except ClientError as e:
            self.logger.error(f"❌ API Client Error: {str(e)}")
            return False
        except APIError as e:
            self.logger.error(f"❌ API Error: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"❌ API connectivity test failed: {str(e)}")
            return False
    
    def read_text_file(self, file_path: Path) -> Optional[str]:
        """Safely read text file with multiple encoding attempts"""
        encodings = ['utf-8', 'utf-16', 'cp1252', 'iso-8859-1', 'ascii']
        
        for encoding in encodings:
            try:
                content = file_path.read_text(encoding=encoding)
                if content.strip():
                    self.logger.debug(f"✅ File read with {encoding}: {file_path.name}")
                    return content.strip()
                else:
                    self.logger.warning(f"⚠️ File is empty: {file_path.name}")
                    return None
                    
            except UnicodeDecodeError:
                self.logger.debug(f"❌ Failed to read with {encoding}: {file_path.name}")
                continue
            except Exception as e:
                self.logger.error(f"❌ Error reading file {file_path.name}: {str(e)}")
                return None
        
        self.logger.error(f"❌ Could not read file with any encoding: {file_path.name}")
        return None
    
    def validate_text_content(self, text: str, max_chars: int = 50000) -> Tuple[bool, str]:
        """Validate text content for Gemini TTS processing"""
        if not text or not text.strip():
            return False, "Text is empty"
        
        if len(text) > max_chars:
            return False, f"Text too long ({len(text)} chars > {max_chars} limit)"
        
        # Check for potentially problematic characters
        if any(ord(char) > 65535 for char in text[:100]):  # Check first 100 chars for unusual Unicode
            self.logger.warning("⚠️ Text contains unusual Unicode characters")
        
        return True, "Valid"
    
    def create_wave_file(self, filename: str, pcm_data: bytes, 
                        channels: int = 1, rate: int = 24000, sample_width: int = 2) -> bool:
        """Create WAV file from PCM data with error handling"""
        try:
            self.logger.debug(f"🎵 Creating WAV file: {filename}")
            
            # Ensure output directory exists
            output_path = Path(filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create temporary file first
            temp_path = output_path.with_suffix('.tmp')
            
            with wave.open(str(temp_path), "wb") as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(sample_width)
                wf.setframerate(rate)
                wf.writeframes(pcm_data)
            
            # Move temp file to final location
            temp_path.rename(output_path)
            
            # Verify file creation
            if output_path.exists() and output_path.stat().st_size > 1000:
                file_size = output_path.stat().st_size
                self.conversion_stats['total_audio_size'] += file_size
                self.logger.info(f"✅ WAV file created: {output_path.name} ({file_size:,} bytes)")
                return True
            else:
                self.logger.error(f"❌ WAV file creation failed or too small: {filename}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error creating WAV file {filename}: {str(e)}")
            return False
    
    def generate_audio_with_retry(self, text: str, max_retries: int = 3) -> Optional[bytes]:
        """Generate audio from text with retry mechanism"""
        
        for attempt in range(1, max_retries + 1):
            try:
                self.logger.debug(f"🎤 Generating audio (attempt {attempt}/{max_retries})")
                
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash-preview-tts",
                    contents=text,
                    config=types.GenerateContentConfig(
                        response_modalities=["AUDIO"],
                        speech_config=types.SpeechConfig(
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=self.voice_name,
                                )
                            )
                        ),
                    )
                )
                
                # Extract PCM data
                if (response and response.candidates and 
                    len(response.candidates) > 0 and 
                    response.candidates[0].content and
                    response.candidates[0].content.parts and
                    len(response.candidates[0].content.parts) > 0):
                    
                    pcm_data = response.candidates[0].content.parts[0].inline_data.data
                    
                    if pcm_data:
                        self.logger.debug(f"✅ Audio generated successfully ({len(pcm_data):,} bytes)")
                        return pcm_data
                    else:
                        self.logger.error("❌ No PCM data in response")
                        return None
                else:
                    self.logger.error("❌ Invalid response structure")
                    return None
                    
            except ClientError as e:
                self.logger.error(f"❌ Client Error (attempt {attempt}): {str(e)}")
                if "quota" in str(e).lower() or "limit" in str(e).lower():
                    self.logger.error("💰 API quota/limit exceeded")
                    return None  # Don't retry quota errors
                    
            except APIError as e:
                self.logger.error(f"❌ API Error (attempt {attempt}): {str(e)}")
                
            except Exception as e:
                self.logger.error(f"❌ Unexpected error (attempt {attempt}): {str(e)}")
            
            if attempt < max_retries:
                wait_time = attempt * 3  # Exponential backoff
                self.logger.info(f"⏳ Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        
        self.logger.error(f"❌ Failed to generate audio after {max_retries} attempts")
        return None
    
    def process_single_file(self, file_path: Path) -> bool:
        """Process a single text file to audio"""
        self.logger.info(f"📄 Processing: {file_path.name}")
        
        # Check if output already exists
        output_path = file_path.with_suffix('.wav')
        if output_path.exists():
            self.logger.info(f"⏭️ Output already exists, skipping: {output_path.name}")
            self.conversion_stats['skipped'] += 1
            return True
        
        # Read text content
        text_content = self.read_text_file(file_path)
        if not text_content:
            self.logger.error(f"❌ Could not read text from: {file_path.name}")
            self.conversion_stats['failed'] += 1
            return False
        
        # Validate content
        is_valid, validation_msg = self.validate_text_content(text_content)
        if not is_valid:
            self.logger.error(f"❌ Text validation failed for {file_path.name}: {validation_msg}")
            self.conversion_stats['failed'] += 1
            return False
        
        self.logger.info(f"📊 Text length: {len(text_content):,} characters")
        
        # Generate audio
        pcm_data = self.generate_audio_with_retry(text_content)
        if not pcm_data:
            self.logger.error(f"❌ Failed to generate audio for: {file_path.name}")
            self.conversion_stats['failed'] += 1
            return False
        
        # Create WAV file
        success = self.create_wave_file(
            str(output_path), 
            pcm_data,
            **self.audio_config
        )
        
        if success:
            self.conversion_stats['successful'] += 1
            return True
        else:
            self.conversion_stats['failed'] += 1
            return False
    
    def find_text_files(self, start_num: int = 1, end_num: int = 100, 
                       prefix: str = "lec_", extension: str = ".txt") -> List[Path]:
        """Find text files with specified pattern"""
        
        files_found = []
        
        # Method 1: Try numbered files
        for i in range(start_num, end_num + 1):
            file_path = self.input_folder / f"{prefix}{i}{extension}"
            if file_path.exists():
                files_found.append(file_path)
        
        if files_found:
            self.logger.info(f"📋 Found {len(files_found)} numbered files ({prefix})")
            return files_found
        
        # Method 2: Find all text files if no numbered files found
        all_text_files = list(self.input_folder.glob(f"*{extension}"))
        if all_text_files:
            self.logger.info(f"📋 Found {len(all_text_files)} text files in folder")
            return sorted(all_text_files)
        
        self.logger.warning("⚠️ No text files found!")
        return []
    
    def convert_batch(self, start_num: int = 19, end_num: int = 45, 
                     prefix: str = "lec_", extension: str = ".txt") -> None:
        """Convert batch of files with comprehensive error handling"""
        
        self.logger.info(f"🎯 Starting batch conversion: {prefix}{start_num} to {prefix}{end_num}")
        
        # Find files to process
        files_to_process = self.find_text_files(start_num, end_num, prefix, extension)
        
        if not files_to_process:
            self.logger.error("❌ No files found to process!")
            return
        
        self.conversion_stats['total'] = len(files_to_process)
        self.logger.info(f"📊 Total files to process: {self.conversion_stats['total']}")
        
        # Process each file
        for i, file_path in enumerate(files_to_process, 1):
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"📁 File {i}/{len(files_to_process)}: {file_path.name}")
            
            try:
                self.process_single_file(file_path)
                
                # Add delay between requests to avoid rate limiting
                if i < len(files_to_process):  # Don't wait after last file
                    self.logger.debug("⏳ Waiting to avoid rate limiting...")
                    time.sleep(2)  # 2 second delay between files
                    
            except KeyboardInterrupt:
                self.logger.info("\n⏹️ Process interrupted by user")
                break
            except Exception as e:
                self.logger.error(f"❌ Unexpected error processing {file_path.name}: {str(e)}")
                self.conversion_stats['failed'] += 1
        
        self.print_summary()
    
    def print_summary(self) -> None:
        """Print comprehensive conversion summary"""
        elapsed_time = time.time() - self.conversion_stats['start_time']
        
        self.logger.info(f"\n{'='*70}")
        self.logger.info("📊 GEMINI TTS CONVERSION SUMMARY")
        self.logger.info(f"{'='*70}")
        self.logger.info(f"⏰ Total time: {elapsed_time:.2f} seconds")
        self.logger.info(f"📁 Total files: {self.conversion_stats['total']}")
        self.logger.info(f"✅ Successful: {self.conversion_stats['successful']}")
        self.logger.info(f"❌ Failed: {self.conversion_stats['failed']}")
        self.logger.info(f"⏭️ Skipped: {self.conversion_stats['skipped']}")
        
        if self.conversion_stats['total_audio_size'] > 0:
            size_mb = self.conversion_stats['total_audio_size'] / (1024 * 1024)
            self.logger.info(f"💾 Total audio size: {size_mb:.2f} MB")
        
        if self.conversion_stats['total'] > 0:
            success_rate = (self.conversion_stats['successful'] / self.conversion_stats['total']) * 100
            self.logger.info(f"📈 Success rate: {success_rate:.1f}%")
        
        if elapsed_time > 0 and self.conversion_stats['successful'] > 0:
            avg_time = elapsed_time / self.conversion_stats['successful']
            self.logger.info(f"⚡ Average time per file: {avg_time:.2f} seconds")
        
        self.logger.info(f"🎤 Voice used: {self.voice_name}")
        self.logger.info(f"{'='*70}")

def main():
    """Main function with enhanced configuration"""
    
    # Configuration - یہاں اپنی settings change کریں
    CONFIG = {
        'api_key': os.environ.get('GEMINI_API_KEY', ''),  # set GEMINI_API_KEY in your environment
        'input_folder': 'tts_input',  # folder with the text files to convert
        'voice_name': 'Zephyr',  # Zephyr, Aoede, Charon, Fenrir, Puck
        'start_num': 19,
        'end_num': 45,
        'prefix': 'lec_',
        'extension': '.txt'
    }
    
    # Validate API key
    if not CONFIG['api_key'].strip():
        print("❌ Error: API key نہیں دی گئی!")
        print("CONFIG section میں اپنی Gemini API key add کریں")
        return 1
    
    try:
        print("🚀 Gemini TTS Converter Starting...")
        
        # Create converter instance
        converter = RobustGeminiTTSConverter(
            api_key=CONFIG['api_key'],
            input_folder=CONFIG['input_folder'],
            voice_name=CONFIG['voice_name']
        )
        
        # Start conversion
        converter.convert_batch(
            start_num=CONFIG['start_num'],
            end_num=CONFIG['end_num'],
            prefix=CONFIG['prefix'],
            extension=CONFIG['extension']
        )
        
        print("\n🎉 Conversion completed! Check the logs for details.")
        
    except KeyboardInterrupt:
        print("\n⏹️ Process cancelled by user")
    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        print("Check the log files for detailed error information")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())