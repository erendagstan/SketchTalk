from dotenv import load_dotenv
import os
import google.generativeai as genai
import PIL.Image
from openai import OpenAI
import requests
from io import BytesIO
from datetime import datetime

load_dotenv('.env')

my_key_openai = os.getenv("openai_apikey")

client = OpenAI(
    api_key=my_key_openai
)

# Ensure directory exists before saving files
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_image_with_dalle(prompt):
    ai_response = client.images.generate(
        model="dall-e-3",
        size="1024x1024",
        quality="hd",
        n=1,
        response_format="url",
        prompt=prompt
    )

    image_url = ai_response.data[0].url

    response = requests.get(image_url)
    image_bytes = BytesIO(response.content)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Specify the correct path for saving images
    img_directory = os.path.join('images')

    # Ensure that the folder structure exists
    ensure_directory_exists(img_directory)

    # Create the filename with a timestamp to make it unique
    filename = os.path.join(img_directory, f"generated_image_{timestamp}.png")

    # Save the image
    with open(filename, "wb") as file:
        file.write(image_bytes.getbuffer())

    return filename


my_key_google = os.getenv("gemini_apikey")

genai.configure(
    api_key=my_key_google
)


def gemini_vision_with_local_file(image_path, prompt):

    multimodality_prompt = f"""Bu gönderdiğim resmi, bazı ek yönergelerle birlikte yeniden oluşturmanı istiyorum. 
    Bunun için ilk olarak resmi son derece ayrıntılı biçimde betimle. Daha sonra sonucunda bana vereceğin metni, bir yapay zeka modelini kullanarak görsel oluşturmakta kullanacağım. 
    O yüzden yanıtına son halini verirken bunun resim üretmek için kullanılacak bir girdi yani prompt olduğunu dikkatele al. 
    İşte ek yönerge şöyle: {prompt}
    """

    client = genai.GenerativeModel(model_name="gemini-pro-vision")

    source_image = PIL.Image.open(image_path)

    ai_response_gemini = client.generate_content(
        {
            multimodality_prompt,
            source_image
        }
    )

    ai_response_gemini.resolve()
    return ai_response_gemini.text


def generate_image(image_path, prompt):

    image_based_prompt = gemini_vision_with_local_file(image_path=image_path, prompt=prompt)

    filename = generate_image_with_dalle(prompt=image_based_prompt)

    return filename



