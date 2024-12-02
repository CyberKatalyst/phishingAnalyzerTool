# Import required libraries and custom modules
from langdetect import detect
from googletrans import Translator
import mailparser
from bs4 import BeautifulSoup


# Checks the language and translates when necessary
def detect_translate(text):
    if not text:
        return None
    translator = Translator()
    detected_language = detect(text)
    # If the language is not EN, translates it
    if detected_language != 'en':
        translated_text = translator.translate(text, dest='en')
        translated_output = f"The original text was on {detected_language.upper()} language.\nThe translated text is:\n{translated_text.text}"
        return translated_output
    # Return the original text if it's in EN
    else:
        return text


# Parses the HTML content
def to_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    extracted_text = soup.get_text(separator="\n")
    clean_text = "\n".join([line.strip() for line in extracted_text.splitlines() if line.strip()])
    return clean_text


def parse_email_and_process_translation(file_path):
    # Parse the email file
    try:
        email_info = mailparser.parse_from_file(file_path)
    except Exception as e:
        print(f"Error parsing email: {e}")
        return

    # Imports the subject and check if it is needed to translate it
    email_subject = email_info.subject
    if email_subject:
        translated_email_subject = detect_translate(email_subject)
    else:
        translated_email_subject = None

    # Parse the email body and handle translation
    email_body_text = email_info.body
    if email_body_text:
        clean_text = to_text(email_body_text)
        translated_text = detect_translate(clean_text)
    else:
        translated_text = None

    # Return translated subject and body (if available)
    return translated_email_subject, translated_text