import llm
import os
import json
import re
import time
import requests
import openai
import logging
import tiktoken 
import random


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)        


# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()
# Load environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_base = os.getenv("OPENAI_API_BASE")
