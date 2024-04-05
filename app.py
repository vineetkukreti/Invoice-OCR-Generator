from flask import Flask, render_template, request, url_for, send_from_directory
import os
from pathlib import Path
import google.generativeai as genai

# Set Google API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyAroxf06TrvDGFDiWAdr5m8AUuqoqMe_TY"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

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
    return image_info[0]['data'], response.text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        system_prompt = """ 
        
you will work as  As the diligent shopkeeper, it's your responsibility to meticulously manage our inventory. To ensure utmost accuracy, I kindly request clear, well-lit images of the products you wish to count. Pay special attention to the labels, as they hold the key to identifying each item correctly.

Rest assured, we'll employ cutting-edge deep learning algorithms to meticulously analyze these images like ocr , yolo ,image segmentation and object detection should be accuracte, it's very impoartant so, these are very imaportant rule to follow to make the model. This advanced technology enables me to discern between various products, regardless of their size or shape. Each item will be accurately counted, and you'll compile a comprehensive table detailing the count of similar products.

In our pursuit of excellence, precision is paramount. With our sophisticated inventory management system, you can trust that every product will be accounted for with the utmost care and attention to detail.

So, be ready, when we provide the images. Your satisfaction is our commitment, and accuracy is our hallmark 

"""
        user_prompt = "user will get the names of product with frequencey  and if not then add that in unknown  in html format  and make sure focues the labels of the prroduct and it's shape ,size ,apperance etc or categoring similar product "

        file = request.files['file']
        if file:
            # Save the uploaded image to a location
            file_path = 'uploads/' + file.filename
            file.save(file_path)

            # Generate HTML content
            image_data, page_content = gemini_output(file_path, system_prompt, user_prompt)
            image_url = url_for('uploaded_file', filename=file.filename)
            return render_template('result.html', image_url=image_url, page_content=page_content)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    app.run(debug=True)
