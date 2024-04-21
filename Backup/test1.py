import requests

# Define the URL for the OCR endpoint
ocr_url = "https://25a0-2405-201-e049-31-9c96-5a9e-2547-8afc.ngrok-free.app/v2/ocr"

def extract_text_from_image(image_path):
    # Open the image file in binary mode
    with open(image_path, "rb") as image_file:
        # Create a dictionary payload with the file data
        files = {'file': image_file}
        
        # Make a POST request to the OCR endpoint
        response = requests.post(ocr_url, files=files)
        
        print(response, response.json())
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the text from the response JSON
            text = response.json()
            return text
        else:
            print("Error:", response.status_code)
            return None

# Path to the image file
image_path = "/home/nagipragalathan/Test/mayan-edms-4.6.3/1702393529166.jpeg"

# Extract text from the image
extracted_text = extract_text_from_image(image_path)

# Print the extracted text
print("Extracted Text:")
print(extracted_text)
