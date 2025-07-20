#!/usr/bin/env python3
"""
Robust Text-to-Speech Converter using gTTS
Enhanced version with comprehensive error handling, logging, and debugging features
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime

try:
    from gtts import gTTS
    from gtts.tts import gTTSError
except ImportError:
    print("❌ gTTS library nahi mila! Install karein:")
    print("pip install gtts")
    sys.exit(1)

# Logging configuration
def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Enhanced logging setup with file and console output"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("gTTS_Converter")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # File handler with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"conversion_{timestamp}.log"
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
    
    logger.info(f"Log file: {log_file}")
    return logger

class RobustgTTSConverter:
    """Enhanced Text-to-Speech converter with robust error handling"""
    
    def __init__(self, input_folder: str, language: str = 'hi', slow: bool = False):
        self.input_folder = Path(input_folder)
        self.language = language
        self.slow = slow
        self.logger = setup_logging()
        self.conversion_stats = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'start_time': time.time()
        }
        
        # Language validation and mapping
        self.language_map = {
            'urdu': 'ur',
            'hindi': 'hi',
            'english': 'en',
            'arabic': 'ar',
            'ur': 'ur',
            'hi': 'hi',
            'en': 'en',
            'ar': 'ar'
        }
        
        self.validate_setup()
    
    def validate_setup(self) -> None:
        """Validate initial setup and configuration"""
        self.logger.info("🚀 gTTS Converter شروع ہو رہا ہے...")
        
        # Validate input folder
        if not self.input_folder.exists():
            self.logger.error(f"❌ Input folder موجود نہیں: {self.input_folder}")
            raise FileNotFoundError(f"Input folder not found: {self.input_folder}")
        
        if not self.input_folder.is_dir():
            self.logger.error(f"❌ Input path فولڈر نہیں ہے: {self.input_folder}")
            raise NotADirectoryError(f"Input path is not a directory: {self.input_folder}")
        
        # Validate language
        if self.language.lower() in self.language_map:
            self.language = self.language_map[self.language.lower()]
            self.logger.info(f"✅ Language set to: {self.language}")
        else:
            self.logger.warning(f"⚠️ Unknown language '{self.language}', using as-is")
        
        # Test internet connectivity
        self.test_gtts_connection()
        
        self.logger.info(f"📁 Input folder: {self.input_folder.resolve()}")
        self.logger.info(f"🌐 Language: {self.language}")
        self.logger.info(f"⚡ Speed: {'Slow' if self.slow else 'Normal'}")
    
    def test_gtts_connection(self) -> bool:
        """Test gTTS service connectivity"""
        try:
            self.logger.info("🔗 Testing gTTS connectivity...")
            test_tts = gTTS(text="test", lang=self.language, slow=False)
            self.logger.info("✅ gTTS service accessible")
            return True
        except Exception as e:
            self.logger.error(f"❌ gTTS connectivity test failed: {str(e)}")
            self.logger.error("Internet connection یا gTTS service کے ساتھ مسئلہ ہو سکتا ہے")
            return False
    
    def read_text_file(self, file_path: Path) -> Optional[str]:
        """Safely read text file with multiple encoding attempts"""
        encodings = ['utf-8', 'utf-16', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                content = file_path.read_text(encoding=encoding)
                if content.strip():  # Check if content is not empty
                    self.logger.debug(f"✅ File read successfully with {encoding}: {file_path.name}")
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
    
    def validate_text_content(self, text: str, max_chars: int = 100000) -> Tuple[bool, str]:
        """Validate text content for gTTS processing"""
        if not text or not text.strip():
            return False, "Text is empty"
        
        if len(text) > max_chars:
            return False, f"Text too long ({len(text)} chars > {max_chars} limit)"
        
        # Check for potentially problematic characters
        if len(text.encode('utf-8')) > len(text) * 4:  # Rough check for unusual encoding
            self.logger.warning("⚠️ Text contains unusual characters, proceeding with caution")
        
        return True, "Valid"
    
    def create_audio_with_retry(self, text: str, output_path: Path, max_retries: int = 3) -> bool:
        """Create audio file with retry mechanism"""
        
        for attempt in range(1, max_retries + 1):
            try:
                self.logger.debug(f"🎵 Creating TTS object (attempt {attempt}/{max_retries})")
                
                # Create gTTS object
                tts = gTTS(
                    text=text,
                    lang=self.language,
                    slow=self.slow,
                    lang_check=True  # Enable language validation
                )
                
                self.logger.debug(f"💾 Saving audio to: {output_path.name}")
                
                # Save with temporary file to avoid corruption
                temp_path = output_path.with_suffix('.tmp')
                tts.save(str(temp_path))
                
                # Move temporary file to final location
                temp_path.rename(output_path)
                
                # Verify file was created and has reasonable size
                if output_path.exists() and output_path.stat().st_size > 1000:  # At least 1KB
                    self.logger.info(f"✅ Audio created successfully: {output_path.name} ({output_path.stat().st_size:,} bytes)")
                    return True
                else:
                    self.logger.error(f"❌ Audio file too small or not created: {output_path.name}")
                    return False
                    
            except gTTSError as e:
                self.logger.error(f"❌ gTTS specific error (attempt {attempt}): {str(e)}")
                if attempt < max_retries:
                    wait_time = attempt * 2  # Exponential backoff
                    self.logger.info(f"⏳ Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                
            except Exception as e:
                self.logger.error(f"❌ Unexpected error (attempt {attempt}): {str(e)}")
                if attempt < max_retries:
                    wait_time = attempt * 2
                    self.logger.info(f"⏳ Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
        
        self.logger.error(f"❌ Failed to create audio after {max_retries} attempts: {output_path.name}")
        return False
    
    def process_single_file(self, file_path: Path) -> bool:
        """Process a single text file to audio"""
        self.logger.info(f"📄 Processing: {file_path.name}")
        
        # Check if output already exists
        output_path = file_path.with_suffix('.mp3')
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
        
        # Create audio
        success = self.create_audio_with_retry(text_content, output_path)
        
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
            self.logger.info(f"\n{'='*50}")
            self.logger.info(f"📁 File {i}/{len(files_to_process)}: {file_path.name}")
            
            try:
                self.process_single_file(file_path)
            except KeyboardInterrupt:
                self.logger.info("\n⏹️ Process interrupted by user")
                break
            except Exception as e:
                self.logger.error(f"❌ Unexpected error processing {file_path.name}: {str(e)}")
                self.conversion_stats['failed'] += 1
            
            # Add small delay between files to avoid overwhelming the service
            time.sleep(1)
        
        self.print_summary()
    
    def print_summary(self) -> None:
        """Print conversion summary"""
        elapsed_time = time.time() - self.conversion_stats['start_time']
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info("📊 CONVERSION SUMMARY")
        self.logger.info(f"{'='*60}")
        self.logger.info(f"⏰ Total time: {elapsed_time:.2f} seconds")
        self.logger.info(f"📁 Total files: {self.conversion_stats['total']}")
        self.logger.info(f"✅ Successful: {self.conversion_stats['successful']}")
        self.logger.info(f"❌ Failed: {self.conversion_stats['failed']}")
        self.logger.info(f"⏭️ Skipped: {self.conversion_stats['skipped']}")
        
        if self.conversion_stats['total'] > 0:
            success_rate = (self.conversion_stats['successful'] / self.conversion_stats['total']) * 100
            self.logger.info(f"📈 Success rate: {success_rate:.1f}%")
        
        self.logger.info(f"{'='*60}")

def main():
    """Main function with command line argument handling"""
    
    # Configuration - آپ یہاں اپنی settings change کر سکتے ہیں
    CONFIG = {
        'input_folder': 'tts_input',
        'language': 'ur',  # 'ur' for Urdu, 'hi' for Hindi, 'en' for English
        'slow': False,     # True for slow speech, False for normal speed
        'start_num': 19,   # Starting file number
        'end_num': 45,     # Ending file number
        'prefix': 'lec_',  # File prefix
        'extension': '.txt' # File extension
    }
    
    try:
        # Create converter instance
        converter = RobustgTTSConverter(
            input_folder=CONFIG['input_folder'],
            language=CONFIG['language'],
            slow=CONFIG['slow']
        )
        
        # Start conversion
        converter.convert_batch(
            start_num=CONFIG['start_num'],
            end_num=CONFIG['end_num'],
            prefix=CONFIG['prefix'],
            extension=CONFIG['extension']
        )
        
    except KeyboardInterrupt:
        print("\n⏹️ Process cancelled by user")
    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())