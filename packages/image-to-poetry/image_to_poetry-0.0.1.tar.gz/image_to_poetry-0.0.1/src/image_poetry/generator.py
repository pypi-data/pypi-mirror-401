import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

def generate_poem(image_path: str) -> str:
    """
    Generates a poem based on the provided image using Google's Gemini model.

    Args:
        image_path (str): Path to the input image.

    Returns:
        str: The generated poem.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it to your Google Gen AI API key.")

    genai.configure(api_key=api_key)

    # Use Gemini Flash Latest (Standard Free Tier)
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
    except Exception:
         # Fallback
         model = genai.GenerativeModel('gemini-flash-latest')

    try:
        if not os.path.exists(image_path):
             raise FileNotFoundError(f"Image not found at {image_path}")

        img = Image.open(image_path)
        
        prompt = "Write a short, rhyming poem about this image."
        
        response = model.generate_content([prompt, img])
        return response.text

    except Exception as e:
        error_msg = f"Error generating poem: {str(e)}"
        if "404" in str(e) or "not found" in str(e).lower():
             error_msg += "\n\nAvailable models:"
             for m in genai.list_models():
                 if 'generateContent' in m.supported_generation_methods:
                     error_msg += f"\n - {m.name}"
        return error_msg
