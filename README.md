# Invoice OCR with Flask

This Flask application allows users to upload invoice photos and generates HTML content by extracting text from the uploaded image using Google's Generative AI.

## Setup

1. Install dependencies by running: ```pip install Flask google-generativeai```

2. Set up a Google API key. You can obtain one from the Google Cloud Console.

3. Set the environment variable `GOOGLE_API_KEY` with your Google API key.

4. Run the Flask application: ```python app.py```


## Usage

1. Access the application through a web browser at `http://localhost:5000/`.

2. Upload an invoice photo using the provided form.

3. Click the "Upload" button to submit the photo.

4. The application will generate HTML content based on the uploaded image and display it on the web page.

## Dependencies

- Flask: Web framework for building the application.
- google-generativeai: Python library for interacting with Google's Generative AI model.

## Project Structure

- `app.py`: Main Flask application file containing routes and logic.
- `index.html`: HTML template for the upload form.
- `uploads/`: Folder to store uploaded images.

## Credits

This project utilizes Google's Generative AI model for content generation.

## License

[MIT License](LICENSE)

## Author
[Your Name Here](https://github.com/your-github-username)