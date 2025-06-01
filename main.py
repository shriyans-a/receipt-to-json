
# import necessary tools
from google.cloud import vision
from google.oauth2 import service_account
import json
import re

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
        "vendor": lines[0] if lines else "", # assume vendor to be the first line
        "items": [],
        "subtotal": "",
        "tax": "",
        "total": ""
    }

    promo_keywords = ["win", "gift card", "sweepstakes", "prize", "contest"] # list of promo words found on receipts. 
    skip_keywords = ["subtotal", "total", "tax", "visa", "card", "tender", "store", "sold", "returned", "auth"] # list of other words to be skipped.
    last_line = "" # empty string for use later.

    for line in lines: # Loop through every line in the receipt
        clean_line = line.strip() # remove leading and following whitespace
        lower_line = clean_line.lower()


        if any(keyword in lower_line for keyword in promo_keywords): # skip promotional content in the receipt.
            continue

        if "subtotal" in lower_line: # check for the word "subtotal" in the line. 
            next_line_l = lines.index(line) + 1 # get the index of the next line after finding our current one.
            if next_line_l < len(lines): 
                next_line = lines[next_line_l].strip() # gets the next line by using the index found in the previous bit. 
                if "$" in next_line: 
                    result["subtotal"] = next_line # append the amount to the end. 
            continue

        if "tax" in lower_line: # repeated same logic as in finding the subtotal. 
            next_line_l = lines.index(line) + 1
            if next_line_l < len(lines):
                next_line = lines[next_line_l].strip()
                if "$" in next_line:
                    result["tax"] = next_line
            continue

        if "total" in lower_line: # repeated same logic as in finding the subtotal. 
            next_line_l = lines.index(line) + 1
            if next_line_l < len(lines):
                next_line = lines[next_line_l].strip()
                if "$" in next_line:
                    result["total"] = next_line
            continue


        if any(keyword in lower_line for keyword in skip_keywords): # skip irrelevant details on receipt. 
            continue
        

        price_match = re.match(r"^\$[\d\.]+[A-Z]?$", clean_line) # searches for a dollar sign, one or more digits/decimal points, and one potential uppercase letter (accounting for the 'R' shown at the end of the prices on the receipt)

        if price_match and last_line and not re.match(r"^\$[\d\.]+[A-Z]?$", last_line): # checks that the current line and the last line aren't both prices, rather the current one is a price and the last line is a statement. 
            result["items"].append({
                "name": last_line,
                "price": re.sub(r"[A-Z]$", "", clean_line) # get rid the of 'R' at the end of the prices. Initially kept so that program does not skip over that line. 
            })


        last_line = clean_line # store the last line in the clean line for when it loops to the next iteration. Allows for comparison of next line with the current iteration.

    return result # return the final dictionary. 

# Print JSON output
parsed = parse_receipt(document) # feed the full text into our 'parse_receipt' function.
print("\n--- Parsed JSON ---\n") 
print(json.dumps(parsed, indent=2)) # converts python dictionary into json object. 

with open("receipt_filtered.json", "w") as fileout: # save as JSON file. 
    json.dump(parsed, fileout, indent = 2)