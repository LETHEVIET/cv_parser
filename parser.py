import argparse
import json
import os
import pathlib

from google.genai import types
import PIL.Image

from schema import DeveloperResume
from prompts import parsing_prompts
from logger import logger


def parse_pdf(pdf_path: str, genai_client) -> dict:
    filepath = pathlib.Path(pdf_path)

    logger.info(f"Parsing PDF file: {filepath}")

    response = genai_client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[
            types.Part.from_bytes(
                data=filepath.read_bytes(),
                mime_type="application/pdf",
            ),
            parsing_prompts,
        ],
        config={
            "response_mime_type": "application/json",
            'response_schema': DeveloperResume,
        },
    )

    json_data = json.loads(response.text)
    return json_data

def parse_image(image_path:str, genai_client) -> dict:

    image = PIL.Image.open(image_path)

    logger.info(f"Parsing image file: {image_path}")

    response = genai_client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[
            image,
            parsing_prompts,
        ],
        config={
            "response_mime_type": "application/json",
            'response_schema': DeveloperResume,
        },
    )

    json_data = json.loads(response.text)
    return json_data