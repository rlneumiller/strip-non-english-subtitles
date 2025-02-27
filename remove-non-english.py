from langdetect import detect, LangDetectException
import re

input_file_path = '/home/arrel/gits/strip-non-english-subtitles/elysium-copy.srt'
output_file_path = '/home/arrel/gits/strip-non-english-subtitles/elysium-copy-result.srt'

def is_english(text):
    # Clean the text of any punctuation and whitespace for better assessment
    clean_text = text.strip()
    
    # Handle very short texts (1-2 words)
    if len(clean_text) <= 20:  # Adjust this threshold as needed
        # Check if text contains primarily Latin characters
        latin_char_pattern = re.compile(r'^[a-zA-Z0-9\s\'\"\.\,\!\?\-\:]+$')
        if latin_char_pattern.match(clean_text):
            print("-------------------- BEGIN ENGLISH -------------------")
            print(text)
            print("--------------------  END ENGLISH  -------------------")
            return True
    
    # For longer texts, use language detection
    try:
        if detect(text) == 'en':
            print("-------------------- BEGIN ENGLISH -------------------")
            print(text)
            print("--------------------  END ENGLISH  -------------------")
            return True
        else:
            print("-------------------- BEGIN NOT ENGLISH ---------------")
            print(text)
            print("--------------------  END NOT ENGLISH  ---------------")
            return False
    except LangDetectException:
        # For errors, check if text contains primarily Latin characters
        latin_char_pattern = re.compile(r'^[a-zA-Z0-9\s\'\"\.\,\!\?\-\:]+$')
        if latin_char_pattern.match(clean_text):
            print("-------------------- BEGIN ENGLISH -------------------")
            print(text)
            print("--------------------  END ENGLISH  -------------------")
            return True
        else:
            print("-------------------- BEGIN NOT ENGLISH ---------------")
            print(text)
            print("--------------------  END NOT ENGLISH  ---------------")
            return False

def clean_srt_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split the content into subtitle entries
    subtitle_entries = content.split('\n\n')
    cleaned_entries = []
    new_counter = 1
    
    for entry in subtitle_entries:
        # Skip empty entries
        if not entry.strip():
            continue
        
        # Split the entry into lines
        lines = entry.strip().split('\n')
        
        # Skip entries with less than 3 lines (need at least number, timestamp, and text)
        if len(lines) < 3:
            continue
        
        # Extract subtitle text (everything from line 3 onwards)
        subtitle_text = '\n'.join(lines[2:])
        
        # Check if the subtitle text is in English
        if is_english(subtitle_text):
            # If the subtitle is in English, keep it
            new_entry = str(new_counter) + '\n' + '\n'.join(lines[1:])
            cleaned_entries.append(new_entry)
            new_counter += 1
    
    # Join the cleaned entries
    cleaned_content = '\n\n'.join(cleaned_entries)
    
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

if __name__ == "__main__":
    clean_srt_file(input_file_path, output_file_path)
    print(f"Non-English subtitles removed and saved to {output_file_path}")