import streamlit as st
from pathlib import Path
import os
import google.generativeai as genai

# Set Google API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyADvpyRnnyKupNoddbNv3D4QNqf2eaGRGo"
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
    return response.text

def main():
    st.title("Retail Product Inventory Management System")
    file = st.file_uploader("Upload Image")

    if file is not None:
        # Save the uploaded image to a location
        file_path = 'uploads/' + file.name
        with open(file_path, "wb") as f:
            f.write(file.read())
        
        # Generate HTML content
        system_prompt = """Business Problem:

As a shopkeeper, you face the challenge of accurately tracking the products in your inventory and monitoring their frequency at any given time. Manual methods of inventory management are time-consuming, prone to errors, and inefficient, especially as your business grows. Therefore, you need a comprehensive solution that utilizes advanced technology to streamline inventory tracking and ensure accuracy.

Solution Approach:

To address your business problem effectively, we propose the development of an automated inventory management system that leverages computer vision technology. Here's a detailed breakdown of how the system will work:

Image Recognition Module:

Develop a deep learning-based object detection model trained on a diverse dataset of product images.
Utilize state-of-the-art convolutional neural networks (CNNs) such as YOLO (You Only Look Once) or Faster R-CNN for accurate and efficient product recognition.
Train the model to recognize various products commonly found in your store, including brands, types, and variants.
Quantity Estimation Component:

Once a product is detected in an image, employ algorithms to estimate the quantity of that product present.
Implement techniques such as counting individual instances of the product or estimating quantity based on the spatial distribution of objects in the image.
Integrate additional sensors where applicable, such as weight sensors for items sold by weight, to enhance quantity estimation accuracy.
Data Logging and Management:

Establish a centralized database system to store and manage inventory data efficiently.
Log each identified product along with its corresponding quantity and timestamp of detection.
Ensure data integrity and security measures to protect sensitive inventory information.
Real-time Updates and Notifications:

Design the system to provide real-time updates on inventory changes.
Implement notifications to alert the shopkeeper of low stock levels, potential discrepancies, or any other relevant inventory-related events.
Enable remote access to inventory data, allowing the shopkeeper to monitor stock levels from anywhere at any time.
Accuracy Validation and Model Refinement:

Regularly validate the accuracy of the object detection and quantity estimation modules.
Conduct manual audits and comparisons with manual counts to identify discrepancies and refine the system accordingly.
Incorporate feedback mechanisms to continuously improve the performance of the deep learning models through retraining on updated datasets.
User Interface Development:

Create a user-friendly interface tailored to the needs of the shopkeeper.
Design intuitive dashboards and visualizations to present inventory data in a clear and comprehensible manner.
Provide functionalities for manual corrections, adjustments, and annotations to facilitate human oversight and intervention when necessary.
Scalability and Flexibility:

Design the system architecture to accommodate future growth and expansion of the business.
Ensure scalability to handle an increasing number of products, locations, and transactions.
Maintain flexibility to integrate with existing inventory management systems or third-party platforms as needed.
Benefits:

Enhanced Efficiency: Automation of inventory management processes saves time and resources, allowing the shopkeeper to focus on core business activities.

Increased Accuracy: Leveraging computer vision technology ensures precise identification and tracking of products, minimizing errors associated with manual methods.

Improved Decision-making: Access to real-time inventory data enables informed decision-making regarding stock replenishment, pricing strategies, and resource allocation.

Cost Savings: Reduction in labor costs and inventory discrepancies leads to cost savings and improved profitability.

Enhanced Customer Satisfaction: Maintaining optimal stock levels ensures product availability, thereby enhancing the overall shopping experience for customers.

By implementing this detailed automated inventory management system, you can optimize operations, mitigate risks, and drive business growth effectively."""

        user_prompt = "user will get the names of product with frequencey shown in the image"

        page = gemini_output(file_path, system_prompt, user_prompt)
        st.write(page)

if __name__ == "__main__":
    main()
