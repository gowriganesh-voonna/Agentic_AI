from google import genai
from google.genai import types

import requests   # It helps your Python program talk to the web.



# with open("lion_hunting.jpg", "rb") as image_file:
#     image_bytes = image_file.read()


client = genai.Client(api_key="AIzaSyC1i5T2p6WfcrgdUtp2t-k799dAoUO3R_o")

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents = [
#         types.Part.from_bytes(
#             data = image_bytes,
#             mime_type = "image/jpeg"
#         ),
#         'Caption this image in a concise manner.'
#     ]
# )

# print(response.text)



# Working code with image URL

image_path = "https://thumbs.dreamstime.com/z/king-wolf-portrait-gray-crown-beautiful-fabulous-ai-generated-296271457.jpg?ct=jpeg"

image_bytes = requests.get(image_path).content

image = types.Part.from_bytes(
    data=image_bytes,
    mime_type="image/jpeg"
)

response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents=[
        image,
        "Provide a concise caption for this image."
        
    ],
)

print(response.text)