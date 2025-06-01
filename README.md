# receipt-to-json
Convert a receipt into a JSON object using Google Cloud Vision API. 

STEPS TO RUN PROJECT:

1) Clone the repository
    git clone https://github.com/your-username/receipt-to-json.git
    cd receipt-to-json

2) Create and Activate Virtual Environment
    python3 -m venv venv
    source venv/bin/activate   On macOS/Linux
     OR
    venv\Scripts\activate   On Windows

3) Install dependencies
    pip install -r requirements.txt

4) Enable Google Cloud Vision API
    create a service account and download .json key
    save the key as receipt_ocr_key.json

5) Create a .env file with the following line:
    GOOGLE_CREDENTIALS=receipt_ocr_key.json

6) Add image of receipt into the project root. 

7) Run the program
    python main.py