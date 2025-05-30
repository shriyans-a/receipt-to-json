
from google.cloud import vision
from google.oauth2 import service_account
import json

credentials = service_account.Credentials.from_service_account_file("receipt_ocr_key.json")
client = vision.ImageAnnotatorClient(credentials=credentials)


image_path = "receipt.jpg"  # save the file to a variable called image_path
with open(image_path, "rb") as image_file: # open the image file in 'read binary' mode 
    content = image_file.read() # read the raw binary content to feed to google vision API.

image = vision.Image(content=content) # creates a Google Vision Image object and passes it the binary data.
response = client.text_detection(image=image) # sends the image to vision API to run text detection. 

document = response.full_text_annotation.text # Get full text stored in the response variable after text detection has been carried out.


# Basic print
print("\n--- Raw Extracted Text ---\n")
print(document)

# Simple JSON parser (starter)
def parse_receipt(text): # define the function that takes an argument, text. 
    lines = text.split('\n') # split text into individual lines

    # initialize result dictionary #
    result = {
        "vendor": lines[0] if lines else "",
        "items": [],
        "total": ""
    }

    for line in lines: # Loop through every line in the receipt
        if "total" in line.lower(): # check if the word 'total' is in the line
            result["total"] = line # if the word 'total' is present, add the value to the dictionary next to the "total" row. 
        elif "$" in line: # check if the dollar sign symbol ($) is in the line. 
            result["items"].append(line) # if '$' is present, add that line to items in the dictionary. 
    return result # return the final dictionary. 

# Print JSON output
parsed = parse_receipt(document) # feed the full text into our 'parse_receipt' function.
print("\n--- Parsed JSON ---\n") 
print(json.dumps(parsed, indent=2)) # converts python dictionary into json object. 