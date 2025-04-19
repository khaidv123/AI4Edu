from openai import OpenAI
from google import genai
from google.genai import types
from together import Together
import base64
import os
from dotenv import load_dotenv
import PIL.Image

load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")

class LLM:
    def __init__(self, provider: str, model: str, temperature: float = 1.0):

        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.client = self._initialize_client()

    def _initialize_client(self):
        if self.provider == "OpenAI":
            return OpenAI()
        elif self.provider == "Google":
            return genai.Client(api_key=gemini_api_key)
        elif self.provider == "TogetherAI":
            return Together()
        elif self.provider == "Nebius":
            return OpenAI(base_url="https://api.studio.nebius.com/v1/", 
                          api_key=os.environ.get("NEBIUS_API_KEY"))
        else:
            raise ValueError("No provider")

    def generate(self, prompt: str, image_path: str = None) -> str:
        if self.provider == "OpenAI":
            return self._openai_completion(prompt, image_path)
        elif self.provider == "Google":
            return self._google_completion(prompt, image_path)
        elif self.provider == "TogetherAI":
            return self._together_completion(prompt, image_path)
        else:
            raise ValueError("No provider")

    def stream(self, prompt: str, image_path: str = None):
        if self.provider == "OpenAI":
            yield from self._openai_stream(prompt, image_path)
        elif self.provider == "Google":
            yield from self._google_stream(prompt, image_path)
        elif self.provider == "TogetherAI":
            yield from self._together_stream(prompt, image_path)
        else:
            raise ValueError("No provider")


    # Open AI
    def _openai_completion(self, prompt: str, image_path: str) -> str:
        messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
        if image_path:
            base64_image = self.encode_image(image_path)
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            })
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )
        return completion.choices[0].message.content

    def _openai_stream(self, prompt: str, image_path: str):
        messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
        if image_path:
            base64_image = self.encode_image(image_path)
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            })
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            temperature=self.temperature
        )
        for chunk in stream:
            yield chunk.choices[0].delta.content or ""


    # Google : (gemma-3-27b-it chưa dùng được hình ảnh)
    def _google_completion(self, prompt: str, image_path: str) -> str:
        contents = [prompt]
        if image_path:
            pil_image = PIL.Image.open(image_path)
            contents.append(pil_image)
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=self.temperature
            )
        )
        return response.text

    def _google_stream(self, prompt: str, image_path: str):
        contents = [prompt]
        if image_path:
            pil_image = PIL.Image.open(image_path)
            contents.append(pil_image)
        response = self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=self.temperature
            )
        )
        for chunk in response:
            yield chunk.text


    # TogetherAI
    def _together_completion(self, prompt: str, image_path: str) -> str:
        messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
        if image_path:
            base64_image = self.encode_image(image_path)
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            })
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )
        return response.choices[0].message.content

    def _together_stream(self, prompt: str, image_path: str):
        messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
        if image_path:
            base64_image = self.encode_image(image_path)
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            })
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            temperature=self.temperature
        )
        for chunk in stream:
            yield chunk.choices[0].delta.content or ""

    def encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
        