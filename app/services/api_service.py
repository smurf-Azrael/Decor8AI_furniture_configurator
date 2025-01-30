import requests
import logging
from app.config import API_KEY, BASE_URL

logging.basicConfig(level=logging.INFO)

def get_headers():
    """Returns authorization headers for API requests."""
    if not API_KEY:
        raise Exception("DECOR8AI_API_KEY is not set.")
    return {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

def send_post_request(endpoint, data=None, files=None):
    """Handles POST requests with error handling and logging."""
    headers = get_headers()
    response = requests.post(BASE_URL + endpoint, headers=headers, json=data, files=files)
    
    if response.status_code != 200:
        logging.error(f"API Error: {response.status_code} - {response.text}")
        return None
    
    return response.json()

def generate_designs_for_room(input_image_url, room_type, design_style, num_images=1, scale_factor=1, 
                              color_scheme="COLOR_SCHEME_0", speciality_decor="SPECIALITY_DECOR_0", 
                              mask_info=None, keep_original_floor=False):
    """Calls the Decor8AI API to generate virtual interior designs."""
    
    payload = {
        "input_image_url": input_image_url,
        "room_type": room_type,
        "design_style": design_style,
        "num_images": num_images,
        "scale_factor": scale_factor,
        "color_scheme": color_scheme,
        "speciality_decor": speciality_decor,
        "mask_info": mask_info,
        "keep_original_floor": keep_original_floor
    }

    response = send_post_request("/generate_designs_for_room", data=payload)

    if response:
        return response
    else:
        return {"error": "Failed to generate designs"}
    
def generate_inspirational_designs(room_type, design_style, num_images=1, color_scheme="COLOR_SCHEME_0", speciality_decor="SPECIALITY_DECOR_0"):

    payload = {
        "room_type": room_type,
        "design_style": design_style,
        "num_images": num_images,
        "color_scheme": color_scheme,
        "speciality_decor": speciality_decor
    }

    response = send_post_request("/generate_inspirational_designs", data=payload)

    if response:
        return response
    else:
        return {"error": "Failed to generate inspirational designs"}

def prime_walls_for_room(input_image_url):
    """Calls the Decor8AI API to prime the walls of a room."""
    
    payload = {"input_image_url": input_image_url}

    response = send_post_request("/prime_walls_for_room", data=payload)

    if response:
        return response
    else:
        return {"error": "Failed to prime walls for the room"}

def replace_sky_behind_house(input_image_url, sky_type):
    """Calls the Decor8AI API to replace the sky in an image of a house."""
    
    payload = {
        "input_image_url": input_image_url,
        "sky_type": sky_type
    }

    response = send_post_request("/replace_sky_behind_house", data=payload)

    if response:
        return response
    else:
        return {"error": "Failed to replace sky in the image"}

def upscale_image(input_image: bytes, scale_factor: int):
    """Calls the Decor8AI API to upscale an image."""

    files = {
        "input_image": ("image.jpg", input_image, "image/jpeg")
    }

    data = {"scale_factor": scale_factor}

    response = send_post_request("/upscale_image", data=data, files=files)

    if response:
        return response
    else:
        return {"error": "Failed to upscale image"}


def remove_objects_from_room(input_image_url: str):
    """Calls the Decor8AI API to remove objects from a room image."""

    payload = {"input_image_url": input_image_url}

    response = send_post_request("/remove_objects_from_room", data=payload)

    if response:
        return response
    else:
        return {"error": "Failed to remove objects from room"}



