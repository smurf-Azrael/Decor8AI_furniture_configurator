from fastapi import APIRouter, HTTPException,UploadFile, File, Form
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
from app.services.api_service import generate_designs_for_room, generate_inspirational_designs, replace_sky_behind_house, prime_walls_for_room, remove_objects_from_room, upscale_image
# Load environment variables
load_dotenv()
BASE_URL = os.getenv("DECOR8AI_BASE_URL", "https://api.decor8.ai")
API_KEY = os.getenv("DECOR8AI_API_KEY")

router = APIRouter()

def get_headers():
    """Returns the authorization headers required for Decor8AI API."""
    if not API_KEY:
        raise HTTPException(status_code=401, detail="API key is missing.")
    
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

@router.get("/speak_friend_and_enter")
async def test_authentication():
    """Tests authentication by calling the Decor8AI authentication endpoint."""
    headers = get_headers()
    response = requests.get(f"{BASE_URL}/speak_friend_and_enter", headers=headers)
    
    if response.status_code == 200:
        return {"message": "Authentication successful"}
    elif response.status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized - Invalid API key")
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

# Define request body schema for generating designs
class GenerateDesignsRequest(BaseModel):
    input_image_url: str
    room_type: str
    design_style: str
    num_images: int
    scale_factor: Optional[int] = 1
    color_scheme: Optional[str] = "COLOR_SCHEME_0"
    speciality_decor: Optional[str] = "SPECIALITY_DECOR_0"
    mask_info: Optional[str] = None
    keep_original_floor: Optional[bool] = False

@router.post("/generate_designs_for_room")
async def generate_designs_for_room_endpoint(request: GenerateDesignsRequest):
    """Endpoint to generate room designs using the Decor8AI API."""
    
    result = generate_designs_for_room(
        input_image_url=request.input_image_url,
        room_type=request.room_type,
        design_style=request.design_style,
        num_images=request.num_images,
        scale_factor=request.scale_factor,
        color_scheme=request.color_scheme,
        speciality_decor=request.speciality_decor,
        mask_info=request.mask_info,
        keep_original_floor=request.keep_original_floor
    )

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result
class GenerateInspirationalDesignsRequest(BaseModel):
    room_type: str
    design_style: str
    num_images: int
    color_scheme: Optional[str] = "COLOR_SCHEME_0"
    speciality_decor: Optional[str] = "SPECIALITY_DECOR_0"

@router.post("/generate_inspirational_designs")
async def generate_inspirational_designs_endpoint(request: GenerateInspirationalDesignsRequest):
    """Endpoint to generate inspirational room designs using the Decor8AI API."""
    
    result = generate_inspirational_designs(
        room_type=request.room_type,
        design_style=request.design_style,
        num_images=request.num_images,
        color_scheme=request.color_scheme,
        speciality_decor=request.speciality_decor
    )

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result

class PrimeWallsRequest(BaseModel):
    input_image_url: str

@router.post("/prime_walls_for_room")
async def prime_walls_for_room_endpoint(request: PrimeWallsRequest):
    """Endpoint to prime the walls of a room."""
    
    result = prime_walls_for_room(request.input_image_url)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result


# Define request body schema for replacing the sky
class ReplaceSkyRequest(BaseModel):
    input_image_url: str
    sky_type: str  # Allowed values: "day", "dusk", "night"

@router.post("/replace_sky_behind_house")
async def replace_sky_behind_house_endpoint(request: ReplaceSkyRequest):
    """Endpoint to replace the sky in an image of a house."""
    
    result = replace_sky_behind_house(request.input_image_url, request.sky_type)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result

class RemoveObjectsRequest(BaseModel):
    input_image_url: str

@router.post("/upscale_image")
async def upscale_image_endpoint(input_image: UploadFile = File(...), scale_factor: int = 2):
    """Endpoint to upscale an image."""
    
    image_content = await input_image.read()
    result = upscale_image(image_content, scale_factor)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result


@router.post("/remove_objects_from_room")
async def remove_objects_from_room_endpoint(request: RemoveObjectsRequest):
    """Endpoint to remove objects from a room image."""
    
    result = remove_objects_from_room(request.input_image_url)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result
