from flask import Flask, render_template, request
from pathlib import Path
import os
import google.generativeai as genai

app = Flask(__name__)

# Set Google API key
os.environ['GOOGLE_API_KEY'] = "paste you API key"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
# you should use dotenv instead

# Model Configuration
MODEL_CONFIG = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Safety Settings of Model
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

model = genai.GenerativeModel(model_name="gemini-pro-vision",
                               generation_config=MODEL_CONFIG,
                               safety_settings=safety_settings)

def image_format(image_path):
    img = Path(image_path)

    if not img.exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    image_parts = [
        {
            "mime_type": "image/png",
            "data": img.read_bytes()
        }
    ]
    return image_parts

def gemini_output(image_path, system_prompt, user_prompt):
    image_info = image_format(image_path)
    input_prompt = [system_prompt, image_info[0], user_prompt]
    response = model.generate_content(input_prompt)
    return response.text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Save the uploaded image to a location
            file_path = 'uploads/' + file.filename
            file.save(file_path)
            # Generate HTML content
            system_prompt = """
              Welcome to the OCR Challenge! Your mission, should you choose to accept it, is to harness your inner OCR expertise and decipher the cryptic characters scattered across a mysterious image—otherwise known as a receipt. Armed with your keen eye and HTML prowess, your task is to meticulously transcribe every symbol, number, and word from the image onto the digital canvas.

                But wait, there's a twist! Not only must you accurately translate the text, but you must also ensure that every character is aligned precisely as it appears on the original receipt. Yes, that means each decimal point, every dollar sign, and all those sneaky spaces must follow the same formatting and arrangement as the enigmatic image.

                Do you have what it takes to conquer the OCR Challenge and emerge victorious? Prepare your HTML tags, sharpen your focus, and dive into the tangled web of characters awaiting your expert scrutiny! """

            user_prompt = "Your mission, should you choose to accept it, is to craft an HTML code capable of faithfully replicating the enigmatic text lurking within a mysterious image . As you embark on this journey, remember: precision is paramount. Your task is not merely to transcribe the characters, but to ensure that every dot, comma, and space aligns perfectly, mirroring the cryptic arrangement of the original image"

            page = gemini_output(file_path, system_prompt, user_prompt)
            print(page)
            return page
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
