"""
This module provides the SDK interface for Pupil functions.

Pupil is a component of the Telekinesis project. Use this module to access and interact with Pupil-related features programmatically.
"""

import requests
import os
import uuid
from cgi import parse_header
from requests_toolbelt.multipart import decoder
from loguru import logger
import numpy as np
from datatypes import datatypes, serializer
from utils import profiler

_PUPIL_API_BASE_URL = "https://api.telekinesis.ai/pupil/v1/"
_ENABLE_SDK_PROFILING = False

# Output format validation: maps input numpy dtype to allowed output format
IMAGE_TYPE_FORMAT_TABLE = {
    np.uint8: ["8bit", "16bitS", "32bit", "64bit"],  
    np.uint16: ["16bitU", "32bit", "64bit"],
    np.int16: ["16bitS", "32bit", "64bit"],
    np.float32: ["32bit"],
    np.float64: ["64bit"],
}

def _load_api_key() -> str:
    """
    Load the Telekinesis API key from the environment variable.

    Returns:
        The API key
    """

    api_key = os.getenv("TELEKINESIS_API_KEY")
    if not api_key:
        raise RuntimeError("Telekinesis API key not found.\n\n"
            "Set the TELEKINESIS_API_KEY environment variable.")
    
    return api_key


def _send_request(endpoint: str, input_data: dict) -> dict:
    """
    Send Telekinesis datatypes via multipart/mixed,
    each part = one Arrow IPC stream.
    """

    profiler_instance = profiler.Profiler(
        endpoint=endpoint,
        method="POST",
        enabled=_ENABLE_SDK_PROFILING,
    )

    profiler_instance.start()

    API_KEY = _load_api_key()

    def write_multipart_request(parts: dict[str, bytes]) -> tuple[bytes, str]:
        boundary = uuid.uuid4().hex
        body = bytearray()

        for name, payload in parts.items():
            body.extend(
                f"--{boundary}\r\n"
                f"Content-Type: application/vnd.apache.arrow.stream\r\n"
                f"Content-Disposition: inline; name=\"{name}\"\r\n\r\n"
                .encode()
            )
            body.extend(payload)
            body.extend(b"\r\n")

        body.extend(f"--{boundary}--\r\n".encode())
        return bytes(body), boundary

    # ---------- BUILD REQUEST ----------
    profiler_instance.mark("build_start")

    fields = {}
    total_request_bytes = 0

    for name, value in input_data.items():
        arrow_bytes = serializer.serialize_to_pyarrow_ipc(value)
        total_request_bytes += len(arrow_bytes)
        fields[name] = arrow_bytes

    body, boundary = write_multipart_request(fields)

    profiler_instance.mark("build_end")

    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": f"multipart/mixed; boundary={boundary}",
        "Content-Length": str(len(body)),
    }

    # ---------- HTTP ----------
    try:
        profiler_instance.mark("http_start")

        response = requests.post(
            f"{_PUPIL_API_BASE_URL}{endpoint}",
            data=body,
            headers=headers,
            timeout=130,
            stream=True,
        )

        response_content = response.content  # force full download

        profiler_instance.mark("http_end")

    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise

    # ---------- error handling ----------

    if not response.ok:
        content_type = response.headers.get("Content-Type", "")
        error = response.json() if "application/json" in content_type else response.text
        raise RuntimeError(f"Request failed [{response.status_code}]: {error}")

    # ---------- PARSE RESPONSE ----------

    profiler_instance.mark("parse_start")

    content_type = response.headers.get("Content-Type", "")
    if "multipart/" not in content_type:
        raise RuntimeError("Expected multipart response from server")

    decoded_data = decoder.MultipartDecoder.from_response(response)

    output_data = {}
    total_response_bytes = 0

    for part in decoded_data.parts:
        total_response_bytes += len(part.content)

        cd = part.headers.get(b"Content-Disposition", b"").decode()
        _, params = parse_header(cd)
        name = params.get("name")
        if not name:
            raise RuntimeError("Missing name in multipart response part")

        output_data[name] = serializer.deserialize_from_pyarrow_ipc(part.content)

    profiler_instance.mark("parse_end")

    # ---------- finalize profiling ----------
    
    profiler_instance.add_sizes(
        request_bytes=total_request_bytes,
        response_bytes=total_response_bytes,
    )
    profiler_instance.end()

    return output_data



# ===================== Contrast =====================

def enhance_image_using_clahe(
    image: datatypes.Image,
    clip_limit: datatypes.Float | float | int  = 2.0,
    tile_grid_size: datatypes.Int | int = 8,
    color_space: datatypes.String | str = "gray",
) -> datatypes.Image:
    """
    Applies Contrast Limited Adaptive Histogram Equalization.

    CLAHE enhances local contrast adaptively, preventing over-amplification of noise
    in uniform regions.

    Args:
        image: The input image to process. Should be a Image object(H, W) or
            (H, W, C).
        clip_limit: The contrast limiting threshold. Increasing allows more contrast
            enhancement but may amplify noise. Typical range: 1.0-8.0. Use 1.0-2.0
            for subtle enhancement, 2.0-4.0 for moderate, 4.0-8.0 for strong.
            Default: 2.0.
        tile_grid_size: The size of the grid for adaptive processing. Increasing
            processes larger regions but may lose local detail. Typical range: 2-16.
            Use 2-4 for fine detail, 4-8 for balanced, 8-16 for coarse. Default: 8.
        color_space: The color space to process. Options: "gray", "rgb", "lab".
            Set using `datatypes.String("space")`. Default: "gray".

    Returns:
        A Image object containing the CLAHE-enhanced image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(clip_limit, (datatypes.Float, float, int)):
        raise TypeError(
            f"clip_limit must be a Float, float, or int, class received: {type(clip_limit).__name__}"
        )
    if not isinstance(tile_grid_size, (datatypes.Int, int)):
        raise TypeError(
            f"tile_grid_size must be an Int or int, class received: {type(tile_grid_size).__name__}"
        )
    if not isinstance(color_space, (datatypes.String, str)):
        raise TypeError(
            f"color_space must be a String or str, class received: {type(color_space).__name__}"
        )
    
    if isinstance(clip_limit, (float, int)):
        clip_limit = datatypes.Float(clip_limit)
    if isinstance(tile_grid_size, int):
        tile_grid_size = datatypes.Int(tile_grid_size)
    if isinstance(color_space, str):
        color_space = datatypes.String(color_space)

    # Prepare input point clouds
    input_data = {"image": image, "clip_limit": clip_limit, "tile_grid_size": tile_grid_size, "color_space": color_space}
    
    # Call the API
    end_point = "enhance_image_using_clahe"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]

# ===================== Morphology =====================

def filter_image_using_morphological_erode(
    image: datatypes.Image,
    kernel_size: datatypes.Int | int = 5,
    kernel_shape: datatypes.String | str = "ellipse",
    iterations: datatypes.Int | int = 1,
    border_type: datatypes.String | str = "default",
) -> datatypes.Image:
    """
    Applies erosion to shrink bright regions and remove small noise.

    Erosion removes pixels from object boundaries, useful for removing small bright
    spots and shrinking objects.

    Args:
        image: The input image to process. Should be a grayscale Image object(H, W).
        kernel_size: The size of the structuring element. Increasing removes larger
            features but may shrink objects more. Typical range: 3-15. Default: 5.
        kernel_shape: The shape of the structuring element. Options: "ellipse",
            "rectangle", "cross". Set using `datatypes.String("shape")`.
            Default: "ellipse".
        iterations: The number of times erosion is applied. Increasing applies more
            erosion. Typical range: 1-10. Default: 1.
        border_type: The border handling mode. Options: "default", "constant",
            "replicate", "reflect", "wrap". Set using `datatypes.String("mode")`.
            Default: "default".

    Returns:
        A Image object containing the eroded image.
    """

    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(kernel_size, (datatypes.Int, int)):
        raise TypeError(
            f"kernel_size must be an Int or int, class received: {type(kernel_size).__name__}"
        )
    if not isinstance(kernel_shape, (datatypes.String, str)):
        raise TypeError(
            f"kernel_shape must be a String or str, class received: {type(kernel_shape).__name__}"
        )
    if not isinstance(iterations, (datatypes.Int, int)):
        raise TypeError(
            f"iterations must be an Int or int, class received: {type(iterations).__name__}"
        )
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(
            f"border_type must be a String or str, class received: {type(border_type).__name__}"
        )
    
    if isinstance(kernel_size, int):
        kernel_size = datatypes.Int(kernel_size)
    if isinstance(kernel_shape, str):
        kernel_shape = datatypes.String(kernel_shape)
    if isinstance(iterations, int):
        iterations = datatypes.Int(iterations)
    if isinstance(border_type, str):
        border_type = datatypes.String(border_type)

    # Prepare input data
    input_data = {
        "image": image,
        "kernel_size": kernel_size,
        "kernel_shape": kernel_shape,
        "iterations": iterations,
        "border_type": border_type,
    }

    # Call the API
    end_point = "filter_image_using_morphological_erode"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]



def filter_image_using_morphological_dilate(
    image: datatypes.Image,
    kernel_size: datatypes.Int | int = 5,
    kernel_shape: datatypes.String | str = "ellipse",
    iterations: datatypes.Int | int = 1,
    border_type: datatypes.String | str = "default",
) -> datatypes.Image:
    """
    Applies dilation to expand bright regions and fill holes.

    Dilation adds pixels to object boundaries, useful for filling gaps and expanding
    objects.

    Args:
        image: The input image to process. Should be a grayscale Image object(H, W).
        kernel_size: The size of the structuring element. Increasing expands objects
            more. Typical range: 3-15. Default: 5.
        kernel_shape: The shape of the structuring element. Options: "ellipse",
            "rectangle", "cross". Set using `datatypes.String("shape")`.
            Default: "ellipse".
        iterations: The number of times dilation is applied. Increasing applies more
            dilation. Typical range: 1-10. Default: 1.
        border_type: The border handling mode. Options: "default", "constant",
            "replicate", "reflect", "wrap". Set using `datatypes.String("mode")`.
            Default: "default".

    Returns:
        A Image object containing the dilated image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(kernel_size, (datatypes.Int, int)):
        raise TypeError(
            f"kernel_size must be an Int or int, class received: {type(kernel_size).__name__}"
        )
    if not isinstance(kernel_shape, (datatypes.String, str)):
        raise TypeError(
            f"kernel_shape must be a String or str, class received: {type(kernel_shape).__name__}"
        )
    if not isinstance(iterations, (datatypes.Int, int)):
        raise TypeError(
            f"iterations must be an Int or int, class received: {type(iterations).__name__}"
        )
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(
            f"border_type must be a String or str, class received: {type(border_type).__name__}"
        )
    
    if isinstance(kernel_size, int):
        kernel_size = datatypes.Int(kernel_size)
    if isinstance(kernel_shape, str):
        kernel_shape = datatypes.String(kernel_shape)
    if isinstance(iterations, int):
        iterations = datatypes.Int(iterations)
    if isinstance(border_type, str):
        border_type = datatypes.String(border_type)

    # Prepare input data
    input_data = {
        "image": image,
        "kernel_size": kernel_size,
        "kernel_shape": kernel_shape,
        "iterations": iterations,
        "border_type": border_type,
    }

    # Call the API
    end_point = "filter_image_using_morphological_dilate"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]

def filter_image_using_morphological_close(
    image: datatypes.Image,
    kernel_size: datatypes.Int | int = 5,
    kernel_shape: datatypes.String | str = "ellipse",
    iterations: datatypes.Int | int = 1,
    border_type: datatypes.String | str = "default",
) -> datatypes.Image:
    """
    Applies morphological closing (dilation followed by erosion).

    Closing fills small holes and gaps, useful for connecting nearby components
    while preserving overall shape.

    Args:
        image: The input image to process. Should be a grayscale Image object(H, W).
        kernel_size: The size of the structuring element. Increasing fills larger
            holes. Typical range: 3-15. Default: 5.
        kernel_shape: The shape of the structuring element. Options: "ellipse",
            "rectangle", "cross". Set using `datatypes.String("shape")`.
            Default: "ellipse".
        iterations: The number of times closing is applied. Typical range: 1-10.
            Default: 1.
        border_type: The border handling mode. Options: "default", "constant",
            "replicate", "reflect", "wrap". Set using `datatypes.String("mode")`.
            Default: "default".

    Returns:
        A Image object containing the closed image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(f"image must be a Image object, class received: {type(image).__name__}")
    if not isinstance(kernel_size, (datatypes.Int, int)):
        raise TypeError(f"kernel_size must be an Int or int, class received: {type(kernel_size).__name__}")
    if not isinstance(kernel_shape, (datatypes.String, str)):
        raise TypeError(f"kernel_shape must be a String or str, class received: {type(kernel_shape).__name__}")
    if not isinstance(iterations, (datatypes.Int, int)):
        raise TypeError(f"iterations must be an Int or int, class received: {type(iterations).__name__}")
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(f"border_type must be a String or str, class received: {type(border_type).__name__}")
    
    if isinstance(kernel_size, int):
        kernel_size = datatypes.Int(kernel_size)
    if isinstance(kernel_shape, str):
        kernel_shape = datatypes.String(kernel_shape)
    if isinstance(iterations, int):
        iterations = datatypes.Int(iterations)
    if isinstance(border_type, str):
        border_type = datatypes.String(border_type)

    input_data = {
        "image": image,
        "kernel_size": kernel_size,
        "kernel_shape": kernel_shape,
        "iterations": iterations,
        "border_type": border_type,
        "morphology_type": datatypes.String("closing"),
    }

    end_point = "filter_image_using_morphological"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]


def filter_image_using_morphological_open(
    image: datatypes.Image,
    kernel_size: datatypes.Int | int = 5,
    kernel_shape: datatypes.String | str = "ellipse",
    iterations: datatypes.Int | int = 1,
    border_type: datatypes.String | str = "default",
) -> datatypes.Image:
    """
    Applies morphological opening (erosion followed by dilation).

    Opening removes small objects and noise while preserving the overall shape.

    Args:
        image: The input image to process. Should be a grayscale Image object(H, W).
        kernel_size: The size of the structuring element. Increasing fills larger
            holes. Typical range: 3-15. Default: 5.
        kernel_shape: The shape of the structuring element. Options: "ellipse",
            "rectangle", "cross". Set using `datatypes.String("shape")`.
            Default: "ellipse".
        iterations: The number of times opening is applied. Typical range: 1-10.
            Default: 1.
        border_type: The border handling mode. Options: "default", "constant",
            "replicate", "reflect", "wrap". Set using `datatypes.String("mode")`.
            Default: "default".

    Returns:
        A Image object containing the opened image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(f"image must be a Image object, class received: {type(image).__name__}")
    if not isinstance(kernel_size, (datatypes.Int, int)):
        raise TypeError(f"kernel_size must be an Int or int, class received: {type(kernel_size).__name__}")
    if not isinstance(kernel_shape, (datatypes.String, str)):
        raise TypeError(f"kernel_shape must be a String or str, class received: {type(kernel_shape).__name__}")
    if not isinstance(iterations, (datatypes.Int, int)):
        raise TypeError(f"iterations must be an Int or int, class received: {type(iterations).__name__}")
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(f"border_type must be a String or str, class received: {type(border_type).__name__}")

    
    if isinstance(kernel_size, int):
        kernel_size = datatypes.Int(kernel_size)
    if isinstance(kernel_shape, str):
        kernel_shape = datatypes.String(kernel_shape)
    if isinstance(iterations, int):
        iterations = datatypes.Int(iterations)
    if isinstance(border_type, str):
        border_type = datatypes.String(border_type)

    input_data = {
        "image": image,
        "kernel_size": kernel_size,
        "kernel_shape": kernel_shape,
        "iterations": iterations,
        "border_type": border_type,
        "morphology_type": datatypes.String("open"),
    }

    end_point = "filter_image_using_morphological"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]

def filter_image_using_morphological_gradient(
    image: datatypes.Image,
    kernel_size: datatypes.Int | int = 5,
    kernel_shape: datatypes.String | str = "ellipse",
    iterations: datatypes.Int | int = 1,
    border_type: datatypes.String | str = "default",
) -> datatypes.Image:
    """
    Applies morphological gradient (dilation followed by erosion).

    Morphological gradient highlights boundaries by computing the difference between
    dilation and erosion.

    Args:
        image: The input image to process. Should be a grayscale Image object(H, W).
        kernel_size: The size of the structuring element. Increasing fills larger
            holes. Typical range: 3-15. Default: 5.
        kernel_shape: The shape of the structuring element. Options: "ellipse",
            "rectangle", "cross". Set using `datatypes.String("shape")`.
            Default: "ellipse".
        iterations: The number of times gradient is applied. Typical range: 1-10.
            Default: 1.
        border_type: The border handling mode. Options: "default", "constant",
            "replicate", "reflect", "wrap". Set using `datatypes.String("mode")`.
            Default: "default".

    Returns:
        A Image object containing the gradient image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(f"image must be a Image object, class received: {type(image).__name__}")
    if not isinstance(kernel_size, (datatypes.Int, int)):
        raise TypeError(f"kernel_size must be an Int or int, class received: {type(kernel_size).__name__}")
    if not isinstance(kernel_shape, (datatypes.String, str)):
        raise TypeError(f"kernel_shape must be a String or str, class received: {type(kernel_shape).__name__}")
    if not isinstance(iterations, (datatypes.Int, int)):
        raise TypeError(f"iterations must be an Int or int, class received: {type(iterations).__name__}")
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(f"border_type must be a String or str, class received: {type(border_type).__name__}")
    
    if isinstance(kernel_size, int):
        kernel_size = datatypes.Int(kernel_size)
    if isinstance(kernel_shape, str):
        kernel_shape = datatypes.String(kernel_shape)
    if isinstance(iterations, int):
        iterations = datatypes.Int(iterations)
    if isinstance(border_type, str):
        border_type = datatypes.String(border_type)

    input_data = {
        "image": image,
        "kernel_size": kernel_size,
        "kernel_shape": kernel_shape,
        "iterations": iterations,
        "border_type": border_type,
        "morphology_type": datatypes.String("gradient"),
    }

    end_point = "filter_image_using_morphological"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]

def filter_image_using_morphological_tophat(
    image: datatypes.Image,
    kernel_size: datatypes.Int | int = 5,
    kernel_shape: datatypes.String | str = "ellipse",
    iterations: datatypes.Int | int = 1,
    border_type: datatypes.String | str = "default",
) -> datatypes.Image:
    """
    Applies morphological tophat (dilation followed by erosion).

    Morphological tophat highlights bright features by computing the difference between
    dilation and erosion.

    Args:
        image: The input image to process. Should be a grayscale Image object(H, W).
        kernel_size: The size of the structuring element. Increasing fills larger
            holes. Typical range: 3-15. Default: 5.
        kernel_shape: The shape of the structuring element. Options: "ellipse",
            "rectangle", "cross". Set using `datatypes.String("shape")`.
            Default: "ellipse".
        iterations: The number of times tophat is applied. Typical range: 1-10.
            Default: 1.
        border_type: The border handling mode. Options: "default", "constant",
            "replicate", "reflect", "wrap". Set using `datatypes.String("mode")`.
            Default: "default".

    Returns:
        A Image object containing the tophat image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(f"image must be a Image object, class received: {type(image).__name__}")
    if not isinstance(kernel_size, (datatypes.Int, int)):
        raise TypeError(f"kernel_size must be an Int or int, class received: {type(kernel_size).__name__}")
    if not isinstance(kernel_shape, (datatypes.String, str)):
        raise TypeError(f"kernel_shape must be a String or str, class received: {type(kernel_shape).__name__}")
    if not isinstance(iterations, (datatypes.Int, int)):
        raise TypeError(f"iterations must be an Int or int, class received: {type(iterations).__name__}")
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(f"border_type must be a String or str, class received: {type(border_type).__name__}")

    if isinstance(kernel_size, int):
        kernel_size = datatypes.Int(kernel_size)
    if isinstance(kernel_shape, str):
        kernel_shape = datatypes.String(kernel_shape)
    if isinstance(iterations, int):
        iterations = datatypes.Int(iterations)
    if isinstance(border_type, str):
        border_type = datatypes.String(border_type)

    input_data = {
        "image": image,
        "kernel_size": kernel_size,
        "kernel_shape": kernel_shape,
        "iterations": iterations,
        "border_type": border_type,
        "morphology_type": datatypes.String("tophat"),
    }

    end_point = "filter_image_using_morphological"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]



def filter_image_using_morphological_blackhat(
    image: datatypes.Image,
    kernel_size: datatypes.Int | int = 5,
    kernel_shape: datatypes.String | str = "ellipse",
    iterations: datatypes.Int | int = 1,
    border_type: datatypes.String | str = "default",
) -> datatypes.Image:
    """
    Applies morphological blackhat (dilation followed by erosion).

    Morphological blackhat highlights dark features by computing the difference between
    dilation and erosion.

    Args:
        image: The input image to process. Should be a grayscale Image object(H, W).
        kernel_size: The size of the structuring element. Increasing fills larger
            holes. Typical range: 3-15. Default: 5.
        kernel_shape: The shape of the structuring element. Options: "ellipse",
            "rectangle", "cross". Set using `datatypes.String("shape")`.
            Default: "ellipse".
        iterations: The number of times blackhat is applied. Typical range: 1-10.
            Default: 1.
        border_type: The border handling mode. Options: "default", "constant",
            "replicate", "reflect", "wrap". Set using `datatypes.String("mode")`.
            Default: "default".

    Returns:
        A Image object containing the blackhat image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(f"image must be a Image object, class received: {type(image).__name__}")
    if not isinstance(kernel_size, (datatypes.Int, int)):
        raise TypeError(f"kernel_size must be an Int or int, class received: {type(kernel_size).__name__}")
    if not isinstance(kernel_shape, (datatypes.String, str)):
        raise TypeError(f"kernel_shape must be a String or str, class received: {type(kernel_shape).__name__}")
    if not isinstance(iterations, (datatypes.Int, int)):
        raise TypeError(f"iterations must be an Int or int, class received: {type(iterations).__name__}")
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(f"border_type must be a String or str, class received: {type(border_type).__name__}")
    
    if isinstance(kernel_size, int):
        kernel_size = datatypes.Int(kernel_size)
    if isinstance(kernel_shape, str):
        kernel_shape = datatypes.String(kernel_shape)
    if isinstance(iterations, int):
        iterations = datatypes.Int(iterations)
    if isinstance(border_type, str):
        border_type = datatypes.String(border_type)

    input_data = {
        "image": image,
        "kernel_size": kernel_size,
        "kernel_shape": kernel_shape,
        "iterations": iterations,
        "border_type": border_type,
        "morphology_type": datatypes.String("blackhat"),
    }

    end_point = "filter_image_using_morphological"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]


# ===================== Pyramid =====================

# Transform Functions
def transform_image_using_pyramid_downsampling(
    image: datatypes.Image,
    scale_factor: datatypes.Float | float | int = 0.5,
) -> datatypes.Image:
    """
    Downsamples an image using Gaussian pyramid.

    Pyramid down reduces image resolution, useful for multi-scale analysis and
    efficient processing.

    Args:
        image: The input image to downsample. Should be a Image object(H, W) or
            (H, W, C).
        scale_factor: The scale factor for downsampling. Must be between 0 and 1.
            Decreasing creates smaller output. Typical range: 0.1-0.9. Use 0.5 for
            half size, 0.25 for quarter size. Default: 0.5.

    Returns:
        A Image object containing the downsampled image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(scale_factor, (datatypes.Float, float, int)):
        raise TypeError(
            f"scale_factor must be a Float, float, or int, class received: {type(scale_factor).__name__}"
        )
    
    if isinstance(scale_factor, (float, int)):
        scale_factor = datatypes.Float(scale_factor)

    # Prepare input data
    input_data = {"image": image, "scale_factor": scale_factor}

    # Call the API
    end_point = "transform_image_using_pyramid_downsampling"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]


def transform_image_using_pyramid_upsampling(
    image: datatypes.Image,
    scale_factor: datatypes.Float | float | int = 2.0,
) -> datatypes.Image:
    """
    Upsamples an image using Gaussian pyramid.

    Pyramid up increases image resolution, useful for image enlargement and
    multi-scale reconstruction.

    Args:
        image: The input image to upsample. Should be a Image object(H, W) or
            (H, W, C).
        scale_factor: The scale factor for upsampling. Must be greater than 1.
            Increasing creates larger output. Typical range: 1.1-4.0. Use 2.0 for
            double size, 4.0 for quadruple size. Default: 2.0.

    Returns:
        A Image object containing the upsampled image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(scale_factor, (datatypes.Float, float, int)):
        raise TypeError(
            f"scale_factor must be a Float, float, or int, class received: {type(scale_factor).__name__}"
        )
    
    if isinstance(scale_factor, (float, int)):
        scale_factor = datatypes.Float(scale_factor)


    # Prepare input data
    input_data = {"image": image, "scale_factor": scale_factor}

    # Call the API
    end_point = "transform_image_using_pyramid_upsampling"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]

# ===================== Ridge / Vesselness =====================

def filter_image_using_frangi(
    image: datatypes.Image,
    scale_start: datatypes.Int | int = 1,
    scale_end: datatypes.Int | int = 10,
    scale_step: datatypes.Int | int = 2,
    alpha: datatypes.Float | float | int = 0.5,
    beta: datatypes.Float | float | int = 0.5,
    detect_black_ridges: datatypes.Bool | bool = True,
    border_type: datatypes.String | str = "reflect",
    constant_value: datatypes.Float | float | int = 0.0,
) -> datatypes.Image:
    """
    Applies Frangi vesselness filter to enhance tubular structures.

    Frangi filter is designed to detect vessel-like structures in medical images,
    fingerprints, and other images with elongated features.

    Args:
        image: The input image to filter. Should be a grayscale Image object(H, W)
            normalized to 0-1 range.
        scale_start: The minimum scale (sigma) for structure detection.
            Typical range: 1-5. Default: 1.
        scale_end: The maximum scale (sigma) for structure detection.
            Typical range: 5-20. Default: 10.
        scale_step: The step size between scales. Smaller steps provide
            finer scale resolution but are slower. Typical range: 1-5. Default: 2.
        alpha: The weight for the blobness measure. Increasing emphasizes blob-like
            structures. Typical range: 0.1-2.0. Default: 0.5.
        beta: The weight for the second-order structureness. Increasing emphasizes
            tubular structures. Typical range: 0.1-2.0. Default: 0.5.
        detect_black_ridges: Whether to detect dark ridges (vessels) instead of bright.
            Set using `datatypes.Bool(True)` or `datatypes.Bool(False)`.
            Default: True.
        border_type: The padding mode for ridge detection. Options: "reflect",
            "constant", "edge", "symmetric", "wrap". Set using `datatypes.String("mode")`.
            Default: "reflect".
        constant_value: The value used for constant padding mode. Typical range: 0.0-1.0.
            Default: 0.0.

    Returns:
        A Image object containing the vesselness-filtered image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(scale_start, (datatypes.Int, int)):
        raise TypeError(
            f"scale_start must be an Int or int, class received: {type(scale_start).__name__}"
        )
    if not isinstance(scale_end, (datatypes.Int, int)):
        raise TypeError(
            f"scale_end must be an Int or int, class received: {type(scale_end).__name__}"
        )
    if not isinstance(scale_step, (datatypes.Int, int)):
        raise TypeError(
            f"scale_step must be an Int or int, class received: {type(scale_step).__name__}"
        )
    if not isinstance(alpha, (datatypes.Float, float, int)):
        raise TypeError(
            f"alpha must be a Float, float, or int, class received: {type(alpha).__name__}"
        )
    if not isinstance(beta, (datatypes.Float, float, int)):
        raise TypeError(
            f"beta must be a Float, float, or int, class received: {type(beta).__name__}"
        )
    if not isinstance(detect_black_ridges, (datatypes.Bool, bool)):
        raise TypeError(
            f"detect_black_ridges must be a Bool or bool, class received: {type(detect_black_ridges).__name__}"
        )
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(
            f"border_type must be a String or str, class received: {type(border_type).__name__}"
        )
    if not isinstance(constant_value, (datatypes.Float, float, int)):
        raise TypeError(
            f"constant_value must be a Float, float, or int, class received: {type(constant_value).__name__}"
        )
    
    if isinstance(scale_start, int):
        scale_start = datatypes.Int(scale_start)
    if isinstance(scale_end, int):
        scale_end = datatypes.Int(scale_end)
    if isinstance(scale_step, int):
        scale_step = datatypes.Int(scale_step)
    if isinstance(alpha, (float, int)):
        alpha = datatypes.Float(alpha)
    if isinstance(beta, (float, int)):
        beta = datatypes.Float(beta)
    if isinstance(detect_black_ridges, bool):
        detect_black_ridges = datatypes.Bool(detect_black_ridges)
    if isinstance(border_type, str):
        border_type= datatypes.String(border_type)
    if isinstance(constant_value, (float, int)):
        constant_value = datatypes.Float(constant_value)
    
    # Prepare input data
    input_data = {
        "image": image,
        "scale_start": scale_start,
        "scale_end": scale_end,
        "scale_step": scale_step,
        "alpha": alpha,
        "beta": beta,
        "detect_black_ridges": detect_black_ridges,
        "border_type": border_type,
        "constant_value": constant_value,
    }

    # Call the API
    end_point = "filter_image_using_frangi"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]


def filter_image_using_hessian(
    image: datatypes.Image,
    scale_start: datatypes.Int | int = 1,
    scale_end: datatypes.Int | int = 10,
    scale_step: datatypes.Int | int = 2,
    detect_black_ridges: datatypes.Bool | bool = True,
    border_type: datatypes.String | str = "reflect",
    constant_value: datatypes.Float | float | int = 0.0,
) -> datatypes.Image:
    """
    Applies Hessian-based vesselness filter for tubular structure detection.

    Hessian filter uses eigenvalue analysis to detect vessel-like structures, similar
    to Frangi but with different vesselness measure.

    Args:
        image: The input image to filter. Should be a grayscale Image object(H, W)
            normalized to 0-1 range.
        scale_start: The starting scale (sigma) for multi-scale detection.
            Typical range: 1-5. Default: 1.
        scale_end: The ending scale (sigma) for multi-scale detection.
            Typical range: 5-20. Default: 10.
        scale_step: The step size between scales. Typical range: 1-5. Default: 2.
        detect_black_ridges: Whether to detect dark ridges instead of bright.
            Set using `datatypes.Bool(True)` or `datatypes.Bool(False)`.
            Default: True.
        border_type: The padding mode. Options: "reflect", "constant", "edge", "symmetric",
            "wrap". Set using `datatypes.String("mode")`. Default: "reflect".
        constant_value: The value used for constant padding mode. Typical range:
            0.0-1.0. Default: 0.0.

    Returns:
        A Image object containing the vesselness-filtered image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(scale_start, (datatypes.Int, int)):
        raise TypeError(
            f"scale_start must be an Int or int, class received: {type(scale_start).__name__}"
        )
    if not isinstance(scale_end, (datatypes.Int, int)):
        raise TypeError(
            f"scale_end must be an Int or int, class received: {type(scale_end).__name__}"
        )
    if not isinstance(scale_step, (datatypes.Int, int)):
        raise TypeError(
            f"scale_step must be an Int or int, class received: {type(scale_step).__name__}"
        )
    if not isinstance(detect_black_ridges, (datatypes.Bool, bool)):
        raise TypeError(
            f"detect_black_ridges must be a Bool or bool, class received: {type(detect_black_ridges).__name__}"
        )
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(
            f"border_type must be a String or str, class received: {type(border_type).__name__}"
        )
    if not isinstance(constant_value, (datatypes.Float, float, int)):
        raise TypeError(
            f"constant_value must be a Float, float, or int, class received: {type(constant_value).__name__}"
        )
    
    if isinstance(scale_start, int):
        scale_start = datatypes.Int(scale_start)
    if isinstance(scale_end, int):
        scale_end = datatypes.Int(scale_end)
    if isinstance(scale_step, int):
        scale_step = datatypes.Int(scale_step)
    if isinstance(detect_black_ridges, bool):
        detect_black_ridges = datatypes.Bool(detect_black_ridges)
    if isinstance(border_type, str):
        border_type= datatypes.String(border_type)
    if isinstance(constant_value, (float, int)):
        constant_value = datatypes.Float(constant_value)

    # Prepare input data
    input_data = {
        "image": image,
        "scale_start": scale_start,
        "scale_end": scale_end,
        "scale_step": scale_step,
        "detect_black_ridges": detect_black_ridges,
        "border_type": border_type,
        "constant_value": constant_value,
    }

    # Call the API
    end_point = "filter_image_using_hessian"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]


def filter_image_using_sato(
    image: datatypes.Image,
    scale_start: datatypes.Int | int = 1,
    scale_end: datatypes.Int | int = 10,
    scale_step: datatypes.Int | int = 2,
    detect_black_ridges: datatypes.Bool | bool = True,
    border_type: datatypes.String | str = "reflect",
    constant_value: datatypes.Float | float | int = 0.0,
) -> datatypes.Image:
    """
    Applies Sato filter for multi-scale ridge detection.

    Sato filter is designed to detect ridges and valleys at multiple scales, useful
    for detecting fine structures like vessels or fibers.

    Args:
        image: The input image to filter. Should be a grayscale Image object(H, W)
            normalized to 0-1 range.
        scale_start: The minimum scale (sigma) for structure detection.
            Typical range: 1-5. Default: 1.
        scale_end: The maximum scale (sigma) for structure detection.
            Typical range: 5-20. Default: 10.
        scale_step: The step size between scales. Typical range: 1-5.
            Default: 2.
        detect_black_ridges: Whether to detect dark ridges instead of bright.
            Set using `datatypes.Bool(True)` or `datatypes.Bool(False)`.
            Default: True.
        border_type: The padding mode. Options:'constant', 'reflect', 'wrap, 'nearest', 'mirror'.
            Set using `datatypes.String("mode")`.
            Default: "reflect".
        constant_value: The value used for constant padding mode. Typical range:
            0.0-1.0. Default: 0.0.

    Returns:
        A Image object containing the ridge-filtered image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(scale_start, (datatypes.Int, int)):
        raise TypeError(
            f"scale_start must be an Int or int, class received: {type(scale_start).__name__}"
        )
    if not isinstance(scale_end, (datatypes.Int, int)):
        raise TypeError(
            f"scale_end must be an Int or int, class received: {type(scale_end).__name__}"
        )
    if not isinstance(scale_step, (datatypes.Int, int)):
        raise TypeError(
            f"scale_step must be an Int or int, class received: {type(scale_step).__name__}"
        )
    if not isinstance(detect_black_ridges, (datatypes.Bool, bool)):
        raise TypeError(
            f"detect_black_ridges must be a Bool or bool, class received: {type(detect_black_ridges).__name__}"
        )
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(
            f"border_type must be a String or str, class received: {type(border_type).__name__}"
        )
    if not isinstance(constant_value, (datatypes.Float, float, int)):
        raise TypeError(
            f"constant_value must be a Float, float, or int, class received: {type(constant_value).__name__}"
        )
    
    if isinstance(scale_start, int):
        scale_start = datatypes.Int(scale_start)
    if isinstance(scale_end, int):
        scale_end = datatypes.Int(scale_end)
    if isinstance(scale_step, int):
        scale_step = datatypes.Int(scale_step)
    if isinstance(detect_black_ridges, bool):
        detect_black_ridges = datatypes.Bool(detect_black_ridges)
    if isinstance(border_type, str):
        border_type= datatypes.String(border_type)
    if isinstance(constant_value, (float, int)):
        constant_value = datatypes.Float(constant_value)

    # Prepare input data
    input_data = {
        "image": image,
        "scale_start": scale_start,
        "scale_end": scale_end,
        "scale_step": scale_step,
        "detect_black_ridges": detect_black_ridges,
        "border_type": border_type,
        "constant_value": constant_value,
    }

    # Call the API
    end_point = "filter_image_using_sato"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]


def filter_image_using_meijering(
    image: datatypes.Image,
    scale_start: datatypes.Int | int = 1,
    scale_end: datatypes.Int | int = 10,
    scale_step: datatypes.Int | int = 2,
    detect_black_ridges: datatypes.Bool | bool = True,
    border_type: datatypes.String | str = "reflect",
    constant_value: datatypes.Float | float | int = 0.0,
) -> datatypes.Image:
    """
    Applies Meijering filter for neurite detection.

    Meijering filter is optimized for detecting neurites and similar branching
    structures in biomedical images.

    Args:
        image: The input image to filter. Should be a grayscale Image object(H, W)
            normalized to 0-1 range.
        scale_start: The minimum scale (sigma) for structure detection.
            Typical range: 1-5. Default: 1.
        scale_end: The maximum scale (sigma) for structure detection.
            Typical range: 5-20. Default: 10.
        scale_step: The step size between scales. Typical range: 1-5.
            Default: 2.
        detect_black_ridges: Whether to detect dark ridges instead of bright.
            Set using `datatypes.Bool(True)` or `datatypes.Bool(False)`.
            Default: True.
        border_type: The padding mode. Options: "reflect", "constant", "edge",
            "symmetric", "wrap". Set using `datatypes.String("mode")`.
            Default: "reflect".
        constant_value: The value used for constant padding mode. Typical range:
            0.0-1.0. Default: 0.0.

    Returns:
        A Image object containing the neurite-filtered image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(scale_start, (datatypes.Int, int)):
        raise TypeError(
            f"scale_start must be an Int or int, class received: {type(scale_start).__name__}"
        )
    if not isinstance(scale_end, (datatypes.Int, int)):
        raise TypeError(
            f"scale_end must be an Int or int, class received: {type(scale_end).__name__}"
        )
    if not isinstance(scale_step, (datatypes.Int, int)):
        raise TypeError(
            f"scale_step must be an Int or int, class received: {type(scale_step).__name__}"
        )
    if not isinstance(detect_black_ridges, (datatypes.Bool, bool)):
        raise TypeError(
            f"detect_black_ridges must be a Bool or bool, class received: {type(detect_black_ridges).__name__}"
        )
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(
            f"border_type must be a String or str, class received: {type(border_type).__name__}"
        )
    if not isinstance(constant_value, (datatypes.Float, float, int)):
        raise TypeError(
            f"constant_value must be a Float, float, or int, class received: {type(constant_value).__name__}"
        )
    
    if isinstance(scale_start, int):
        scale_start = datatypes.Int(scale_start)
    if isinstance(scale_end, int):
        scale_end = datatypes.Int(scale_end)
    if isinstance(scale_step, int):
        scale_step = datatypes.Int(scale_step)
    if isinstance(detect_black_ridges, bool):
        detect_black_ridges = datatypes.Bool(detect_black_ridges)
    if isinstance(border_type, str):
        border_type= datatypes.String(border_type)
    if isinstance(constant_value, (float, int)):
        constant_value = datatypes.Float(constant_value)

    # Prepare input data
    input_data = {
        "image": image,
        "scale_start": scale_start,
        "scale_end": scale_end,
        "scale_step": scale_step,
        "detect_black_ridges": detect_black_ridges,
        "border_type": border_type,
        "constant_value": constant_value,
    }

    # Call the API
    end_point = "filter_image_using_meijering"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]

# ===================== Sharpening / Gradients =====================

def filter_image_using_laplacian(
    image: datatypes.Image,
    kernel_size: datatypes.Int | int = 3,
    scale: datatypes.Float | float | int = 1.0,
    delta: datatypes.Float | float | int = 0.0,
    output_format: datatypes.String | str = "64bit",
    border_type: datatypes.String | str = "default",
) -> datatypes.Image:
    """
    Applies Laplacian filter for edge detection using second derivatives.

    Laplacian operator detects edges by finding regions where the second derivative is
    zero or changes sign.

    Args:
        image: The input image to filter. Should be a grayscale Image object(H, W).
        kernel_size: The size of the Laplacian kernel. Must be 1, 3, 5, or 7. Larger
            kernels detect larger edges. Typical values: 1, 3, 5, 7. Default: 3.
        scale: The scale factor for the computed Laplacian values. Increasing amplifies
            edge responses. Typical range: 0.1-10.0. Use 0.1-1.0 for subtle edges,
            1.0-5.0 for normal, 5.0-10.0 for strong. Default: 1.0.
        delta: The offset added to the output. Useful for visualization.
            Typical range: -128.0 to 128.0. Default: 0.0.
        output_format: The output bit depth. Options: "8bit", "16bitS", "16bitU", "32bit", "64bit".
            Must be compatible with input image dtype. "16bitS" is signed 16-bit, "16bitU" is unsigned 16-bit.
            Set using `datatypes.String("format")`. Default: "64bit".
        border_type: The border handling mode. Options: "default", "constant", "replicate",
            "reflect", "wrap". Set using `datatypes.String("mode_name")`.
            Default: "default".

    Returns:
        A Image object containing the edge-detected image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(kernel_size, (datatypes.Int, int)):
        raise TypeError(
            f"kernel_size must be an Int or int, class received: {type(kernel_size).__name__}"
        )
    if not isinstance(scale, (datatypes.Float, float, int)):
        raise TypeError(
            f"scale must be a Float, float, or int, class received: {type(scale).__name__}"
        )
    if not isinstance(delta, (datatypes.Float, float, int)):
        raise TypeError(
            f"delta must be a Float, float, or int, class received: {type(delta).__name__}"
        )
    if not isinstance(output_format, (datatypes.String, str)):
        raise TypeError(
            f"output_format must be a String or str, class received: {type(output_format).__name__}"
        )
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(
            f"border_type must be a String or str, class received: {type(border_type).__name__}"
        )
    
    # Get output_format as string for validation
    output_format_str = output_format.value if isinstance(output_format, datatypes.String) else output_format

    # Validate output_format against input image dtype
    image_np = image.to_numpy()
    input_dtype = image_np.dtype.type
    
    if input_dtype not in IMAGE_TYPE_FORMAT_TABLE:
        raise ValueError(
            f"Unsupported input image dtype: {input_dtype}. Supported dtypes: {list(IMAGE_TYPE_FORMAT_TABLE.keys())}"
        )
    
    allowed_formats = IMAGE_TYPE_FORMAT_TABLE[input_dtype]
    if output_format_str not in allowed_formats:
        raise ValueError(
            f"output_format '{output_format_str}' is not valid for input dtype {input_dtype}. "
            f"Allowed formats: {allowed_formats}"
        )
    
    if isinstance(kernel_size, int):
        kernel_size = datatypes.Int(kernel_size)
    if isinstance(scale, (float, int)):
        scale = datatypes.Float(scale)
    if isinstance(delta, (float, int)):
        delta = datatypes.Float(delta)
    if isinstance(output_format, str):
        output_format = datatypes.String(output_format)
    if isinstance(border_type, str):
        border_type = datatypes.String(border_type)
    
    # Prepare input data
    input_data = {
        "image": image,
        "kernel_size": kernel_size,
        "scale": scale,
        "delta": delta,
        "output_format": output_format,  # API still uses desired_depth
        "border_type": border_type,
    }

    # Call the API
    end_point = "filter_image_using_laplacian"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]


def filter_image_using_sobel(
    image: datatypes.Image,
    dx: datatypes.Int | int = 1,
    dy: datatypes.Int | int = 1,
    kernel_size: datatypes.Int | int = 3,
    scale: datatypes.Float | float | int = 1.0,
    delta: datatypes.Float | float | int = 0.0,
    output_format: datatypes.String | str = "64bit",
    border_type: datatypes.String | str = "default",
) -> datatypes.Image:
    """
    Applies Sobel filter for directional edge detection.

    Sobel operator computes gradients in X and Y directions, useful for detecting edges
    and their orientation.

    Args:
        image: The input image to filter. Should be a grayscale Image object(H, W).
        dx: The order of the derivative in X direction. 0 means no
            derivative, 1 means first derivative (edge detection), 2 means second
            derivative. Typical values: 0, 1, 2. Default: 1.
        dy: The order of the derivative in Y direction. Typical values:
            0, 1, 2. Default: 1.
        kernel_size: The size of the Sobel kernel. Must be 1, 3, 5, 7, or 9. Larger
            kernels detect larger edges. Typical values: 1, 3, 5, 7, 9. Default: 3.
        scale: The scale factor for the computed derivative values. Increasing amplifies
            edge responses. Typical range: 0.1-10.0. Default: 1.0.
        delta: The offset added to the output. Typical range: -128.0 to 128.0.
            Default: 0.0.
        output_format: The output bit depth. Options: "8bit", "16bitS", "16bitU", "32bit", "64bit".
            Must be compatible with input image dtype. "16bitS" is signed 16-bit, "16bitU" is unsigned 16-bit.
            Set using `datatypes.String("format")`. Default: "64bit".
        border_type: The border handling mode. Options: "default", "constant", "replicate",
            "reflect", "wrap". Set using `datatypes.String("mode_name")`.
            Default: "default".

    Returns:
        A Image object containing the edge-detected image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(dx, (datatypes.Int, int)):
        raise TypeError(
            f"dx must be an Int or int, class received: {type(dx).__name__}"
        )
    if not isinstance(dy, (datatypes.Int, int)):
        raise TypeError(
            f"dy must be an Int or int, class received: {type(dy).__name__}"
        )
    if not isinstance(kernel_size, (datatypes.Int, int)):
        raise TypeError(
            f"kernel_size must be an Int or int, class received: {type(kernel_size).__name__}"
        )
    if not isinstance(scale, (datatypes.Float, float, int)):
        raise TypeError(
            f"scale must be a Float, float, or int, class received: {type(scale).__name__}"
        )
    if not isinstance(delta, (datatypes.Float, float, int)):
        raise TypeError(
            f"delta must be a Float, float, or int, class received: {type(delta).__name__}"
        )
    if not isinstance(output_format, (datatypes.String, str)):
        raise TypeError(
            f"output_format must be a String or str, class received: {type(output_format).__name__}"
        )
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(
            f"border_type must be a String or str, class received: {type(border_type).__name__}"
        )
    
    # Get output_format as string for validation
    output_format_str = output_format.value if isinstance(output_format, datatypes.String) else output_format
    
    # Validate output_format against input image dtype
    image_np = image.to_numpy()
    input_dtype = image_np.dtype.type
    
    if input_dtype not in IMAGE_TYPE_FORMAT_TABLE:
        raise ValueError(
            f"Unsupported input image dtype: {input_dtype}. Supported dtypes: {list(IMAGE_TYPE_FORMAT_TABLE.keys())}"
        )
    
    allowed_formats = IMAGE_TYPE_FORMAT_TABLE[input_dtype]
    if output_format_str not in allowed_formats:
        raise ValueError(
            f"output_format '{output_format_str}' is not valid for input dtype {input_dtype}. "
            f"Allowed formats: {allowed_formats}"
        )
    
    if isinstance(dx, int):
        dx = datatypes.Int(dx)
    if isinstance(dy, int):
        dy = datatypes.Int(dy)
    if isinstance(kernel_size, int):
        kernel_size = datatypes.Int(kernel_size)
    if isinstance(scale, (float, int)):
        scale = datatypes.Float(scale)
    if isinstance(delta, (float, int)):
        delta = datatypes.Float(delta)
    if isinstance(output_format, str):
        output_format = datatypes.String(output_format)
    if isinstance(border_type, str):
        border_type = datatypes.String(border_type)

    # Prepare input data
    input_data = {
        "image": image,
        "dx": dx,
        "dy": dy,
        "kernel_size": kernel_size,
        "scale": scale,
        "delta": delta,
        "output_format": output_format,  # API still uses desired_depth
        "border_type": border_type,
    }

    # Call the API
    end_point = "filter_image_using_sobel"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]

def filter_image_using_gabor(
    image: datatypes.Image,
    kernel_size: datatypes.Int | int = datatypes.Int(21),
    standard_deviation: datatypes.Float | float | int = datatypes.Float(5.0),
    orientation: datatypes.Float | float | int = datatypes.Float(0.0),
    wavelength: datatypes.Float | float | int = datatypes.Float(10.0),
    aspect_ratio: datatypes.Float | float | int = datatypes.Float(0.5),
    phase_offset: datatypes.Float | float | int = datatypes.Float(0.0),
) -> datatypes.Image:
    """
    Applies Gabor filter for texture analysis and feature detection.

    Gabor filters are useful for detecting oriented features and textures at specific
    scales and orientations.

    Args:
        image: The input image to filter. Should be a grayscale Image object(H, W).
        kernel_size: The size of the Gabor kernel. Must be odd. Increasing captures
            larger features. Typical range: 5-51. Use 5-15 for fine textures, 15-31
            for medium, 31-51 for coarse. Default: 21.
        standard_deviation: The standard deviation of the Gaussian envelope. Increasing
            creates a wider filter. Typical range: 1.0-20.0. Default: 5.0.
        orientation: The orientation of the filter in degrees. 0° is horizontal,
            90° is vertical. Typical range: 0.0-180.0. Default: 0.0.
        wavelength: The wavelength of the sinusoidal component. Decreasing detects
            finer features. Typical range: 2.0-50.0. Default: 10.0.
        aspect_ratio: The aspect ratio of the filter (width/height). 1.0 is circular,
            <1.0 is elongated. Typical range: 0.1-1.0. Default: 0.5.
        phase_offset: The phase offset of the sinusoidal component in degrees.
            Typical range: 0.0-360.0. Default: 0.0.

    Returns:
        A Image object containing the filtered image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(kernel_size, (datatypes.Int, int)):
        raise TypeError(
            f"kernel_size must be an Int or int, class received: {type(kernel_size).__name__}"
        )
    if not isinstance(standard_deviation, (datatypes.Float, float, int)):
        raise TypeError(
            f"standard_deviation must be a Float, float, or int, class received: {type(standard_deviation).__name__}"
        )
    if not isinstance(orientation, (datatypes.Float, float, int)):
        raise TypeError(
            f"orientation must be a Float, float, or int, class received: {type(orientation).__name__}"
        )
    if not isinstance(wavelength, (datatypes.Float, float, int)):
        raise TypeError(
            f"wavelength must be a Float, float, or int, class received: {type(wavelength).__name__}"
        )
    if not isinstance(aspect_ratio, (datatypes.Float, float, int)):
        raise TypeError(
            f"aspect_ratio must be a Float, float, or int, class received: {type(aspect_ratio).__name__}"
        )
    if not isinstance(phase_offset, (datatypes.Float, float, int)):
        raise TypeError(
            f"phase_offset must be a Float, float, or int, class received: {type(phase_offset).__name__}"
        )
    
    if isinstance(kernel_size, int):
        kernel_size = datatypes.Int(kernel_size)
    if isinstance(standard_deviation, (float, int)):
        standard_deviation = datatypes.Float(standard_deviation)
    if isinstance(orientation, (float, int)):
        orientation = datatypes.Float(orientation)
    if isinstance(wavelength, (float, int)):
        wavelength = datatypes.Float(wavelength)
    if isinstance(aspect_ratio, (float, int)):
        aspect_ratio = datatypes.Float(aspect_ratio)
    if isinstance(phase_offset, (float, int)):
        phase_offset = datatypes.Float(phase_offset)

    # Prepare input data
    input_data = {
        "image": image,
        "kernel_size": kernel_size,
        "standard_deviation": standard_deviation,
        "orientation": orientation,
        "wavelength": wavelength,
        "aspect_ratio": aspect_ratio,
        "phase_offset": phase_offset,
    }

    # Call the API
    end_point = "filter_image_using_gabor"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]


def filter_image_using_scharr(
    image: datatypes.Image,
    dx: datatypes.Int | int = 1,
    dy: datatypes.Int | int = 0,
    scale: datatypes.Float | float | int = 1.0,
    delta: datatypes.Float | float | int = 0.0,
    output_format: datatypes.String | str = "64bit",
    border_type: datatypes.String | str = "default",
) -> datatypes.Image:
    """
    Applies Scharr filter for improved edge detection accuracy.

    Scharr operator is similar to Sobel but with better rotation invariance and more
    accurate gradient estimation.

    Args:
        image: The input image to filter. Should be a grayscale Image object(H, W).
        dx: The order of the derivative in X direction. Typical values:
            0, 1. Default: 1.
        dy: The order of the derivative in Y direction. Typical values:
            0, 1. Default: 0.
        scale: The scale factor for the computed derivative values. Typical range:
            0.1-10.0. Default: 1.0.
        delta: The offset added to the output. Typical range: -128.0 to 128.0.
            Default: 0.0.
        output_format: The output bit depth. Options: "8bit", "16bitS", "16bitU", "32bit", "64bit".
            Must be compatible with input image dtype. "16bitS" is signed 16-bit, "16bitU" is unsigned 16-bit.
            Set using `datatypes.String("format")`. Default: "64bit".
        border_type: The border handling mode. Options: "default", "constant", "replicate",
            "reflect", "wrap". Set using `datatypes.String("mode_name")`.
            Default: "default".

    Returns:
        A Image object containing the edge-detected image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(dx, (datatypes.Int, int)):
        raise TypeError(
            f"dx must be an Int or int, class received: {type(dx).__name__}"
        )
    if not isinstance(dy, (datatypes.Int, int)):
        raise TypeError(
            f"dy must be an Int or int, class received: {type(dy).__name__}"
        )
    if not isinstance(scale, (datatypes.Float, float, int)):
        raise TypeError(
            f"scale must be a Float, float, or int, class received: {type(scale).__name__}"
        )
    if not isinstance(delta, (datatypes.Float, float, int)):
        raise TypeError(
            f"delta must be a Float, float, or int, class received: {type(delta).__name__}"
        )
    if not isinstance(output_format, (datatypes.String, str)):
        raise TypeError(
            f"output_format must be a String or str, class received: {type(output_format).__name__}"
        )
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(
            f"border_type must be a String or str, class received: {type(border_type).__name__}"
        )
    
    # Get output_format as string for validation
    output_format_str = output_format.value if isinstance(output_format, datatypes.String) else output_format
    
    # Validate output_format against input image dtype
    image_np = image.to_numpy()
    input_dtype = image_np.dtype.type
    
    if input_dtype not in IMAGE_TYPE_FORMAT_TABLE:
        raise ValueError(
            f"Unsupported input image dtype: {input_dtype}. Supported dtypes: {list(IMAGE_TYPE_FORMAT_TABLE.keys())}"
        )
    
    allowed_formats = IMAGE_TYPE_FORMAT_TABLE[input_dtype]
    if output_format_str not in allowed_formats:
        raise ValueError(
            f"output_format '{output_format_str}' is not valid for input dtype {input_dtype}. "
            f"Allowed formats: {allowed_formats}"
        )
    
    if isinstance(dx, int):
        dx = datatypes.Int(dx)
    if isinstance(dy, int):
        dy = datatypes.Int(dy)
    if isinstance(scale, (float, int)):
        scale = datatypes.Float(scale)
    if isinstance(delta, (float, int)):
        delta = datatypes.Float(delta)
    if isinstance(output_format, str):
        output_format = datatypes.String(output_format)
    if isinstance(border_type, str):
        border_type = datatypes.String(border_type)

    # Prepare input data
    input_data = {
        "image": image,
        "dx": dx,
        "dy": dy,
        "scale": scale,
        "delta": delta,
        "output_format": output_format,  # API still uses desired_depth
        "border_type": border_type,
    }

    # Call the API
    end_point = "filter_image_using_scharr"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]

# ===================== Smoothing =====================

def filter_image_using_bilateral(
    image: datatypes.Image,
    neighborhood_diameter: datatypes.Int | int = datatypes.Int(9),
    color_intensity_sigma: datatypes.Float | float | int = datatypes.Float(75.0),
    spatial_sigma: datatypes.Float | float | int = datatypes.Float(75.0),
    border_type: datatypes.String | str = datatypes.String("default"),
) -> datatypes.Image:
    """
    Applies a bilateral filter to reduce noise while preserving edges.

    Bilateral filtering is effective for noise reduction while maintaining edge sharpness.
    It considers both spatial proximity and color similarity.

    Args:
        image: The input image to filter. Should be a Image object(H, W) or (H, W, C).
        neighborhood_diameter: The size of the kernel for spatial filtering. Must be odd. Increasing
            increases the spatial smoothing area but is slower. Decreasing is faster but
            less effective at smoothing. Typical range: 3-15. Use 3-5 for small images,
            5-9 for medium, 9-15 for large. Default: 9.
        spatial_sigma: The spatial standard deviation in pixels. Increasing makes
            the filter consider pixels farther away, creating more smoothing. Decreasing
            focuses on nearby pixels only. Typical range: 10.0-150.0. Use 10.0-50.0 for
            fine details, 50.0-100.0 for balanced, 100.0-150.0 for strong smoothing.
            Default: 75.0.
        color_intensity_sigma: The color/intensity standard deviation. Increasing allows
            larger color differences to be smoothed, merging more regions. Decreasing
            preserves more color boundaries. Typical range: 10.0-150.0. Use 10.0-50.0
            for strict color preservation, 50.0-100.0 for balanced, 100.0-150.0 for
            more color blending. Default: 75.0.
        border_type: The border handling mode. Options: "default", "constant", "replicate",
            "reflect", "wrap". "default" uses the library's default. Set using
            `datatypes.String("mode_name")`. Default: "default".

    Returns:
        A Image object containing the filtered image with the same shape as input.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(neighborhood_diameter, (datatypes.Int, int)):
        raise TypeError(
            f"kernel_size must be an Int or int, class received: {type(neighborhood_diameter).__name__}"
        )
    if not isinstance(color_intensity_sigma, (datatypes.Float, float, int)):
        raise TypeError(
            f"spatial_sensitivity must be a Float, float, or int, class received: {type(color_intensity_sigma).__name__}"
        )
    if not isinstance(spatial_sigma, (datatypes.Float, float, int)):
        raise TypeError(
            f"color_sensitivity must be a Float, float, or int, class received: {type(spatial_sigma).__name__}"
        )
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(
            f"border_type must be a String or str, class received: {type(border_type).__name__}"
        )
    
    if isinstance(neighborhood_diameter, int):
        neighborhood_diameter = datatypes.Int(neighborhood_diameter)
    if isinstance(color_intensity_sigma, (float, int)):
        color_intensity_sigma = datatypes.Float(color_intensity_sigma)
    if isinstance(spatial_sigma, (float, int)):
        spatial_sigma = datatypes.Float(spatial_sigma)
    if isinstance(border_type, str):
        border_type = datatypes.String(border_type)

    # Prepare input data
    input_data = {
        "image": image,
        "spatial_sigma": spatial_sigma,
        "color_intensity_sigma": color_intensity_sigma,
        "neighborhood_diameter": neighborhood_diameter,
        "border_type": border_type,
    }

    # Call the API
    end_point = "filter_image_using_bilateral"
    response_data = _send_request(endpoint=end_point, input_data=input_data)

    # _run_arrow_filter default output_key is "filtered_image"
    filtered_image = response_data["filtered_image"]
    return filtered_image


def filter_image_using_blur(
    image: datatypes.Image,
    kernel_size: datatypes.Int | int = datatypes.Int(15),
    border_type: datatypes.String | str = datatypes.String("default"),
) -> datatypes.Image:
    """
    Applies a simple box blur filter to an image.

    Box blur is a basic smoothing operation that averages pixel values within a kernel.
    Fast but can blur edges.

    Args:
        image: The input image to filter. Should be a Image object(H, W) or (H, W, C).
        kernel_size: The size of the blur kernel. Must be odd. Increasing creates more
            blur but is slower. Decreasing is faster but less blur. Typical range: 3-31.
            Use 3-7 for light blur, 7-15 for moderate, 15-31 for heavy blur.
            Default: 15.
        border_type: The border handling mode. Options: "default", "constant", "replicate",
            "reflect", "wrap". Set using `datatypes.String("mode_name")`.
            Default: "default".

    Returns:
        A Image object containing the blurred image with the same shape as input.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(kernel_size, (datatypes.Int, int)):
        raise TypeError(
            f"kernel_size must be an Int or int, class received: {type(kernel_size).__name__}"
        )
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(
            f"border_type must be a String or str, class received: {type(border_type).__name__}"
        )
    
    if isinstance(kernel_size, int):
        kernel_size = datatypes.Int(kernel_size)
    if isinstance(border_type, str):
        border_type = datatypes.String(border_type)

    # Prepare input data
    input_data = {
        "image": image,
        "kernel_size": kernel_size,
        "border_type": border_type,
    }

    # Call the API
    end_point = "filter_image_using_blur"
    response_data = _send_request(endpoint=end_point, input_data=input_data)

    # _run_arrow_filter default output_key is "filtered_image"
    filtered_image = response_data["filtered_image"]
    return filtered_image


def filter_image_using_box(
    image: datatypes.Image,
    kernel_size: datatypes.Int | int = 5,
    normalize: datatypes.Bool | bool = True,
    output_format: datatypes.String | str = "64bit",
    border_type: datatypes.String | str = "default",
) -> datatypes.Image:
    """
    Applies a normalized box filter with configurable depth and normalization.

    Box filter performs normalized averaging within a kernel region. Useful for basic
    smoothing operations.

    Args:
        image: The input image to filter. Should be a Image object(H, W) or (H, W, C).
        kernel_size: The size of the box kernel. Must be odd. Increasing creates larger
            averaging area. Typical range: 3-15. Default: 5.
        normalize: Whether to normalize the kernel so the sum equals 1. When True,
            preserves average brightness. When False, may brighten or darken the image.
            Set using `datatypes.Bool(True)` or `datatypes.Bool(False)`.
            Default: True.
        output_format: The output bit depth. Options: "8bit", "16bitS", "16bitU", "32bit", "64bit".
            Must be compatible with input image dtype. "16bitS" is signed 16-bit, "16bitU" is unsigned 16-bit.
            Higher depth preserves more precision but uses more memory. 
            Set using `datatypes.String("format")`. Default: "64bit".
        border_type: The border handling mode. Options: "default", "constant", "replicate",
            "reflect", "wrap". Set using `datatypes.String("mode_name")`.
            Default: "default".

    Returns:
        A Image object containing the filtered image with the same shape as input.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(kernel_size, (datatypes.Int, int)):
        raise TypeError(
            f"kernel_size must be an Int or int, class received: {type(kernel_size).__name__}"
        )
    if not isinstance(normalize, (datatypes.Bool, bool)):
        raise TypeError(
            f"normalize_kernel must be a Bool or bool, class received: {type(normalize).__name__}"
        )
    if not isinstance(output_format, (datatypes.String, str)):
        raise TypeError(
            f"output_format must be a String or str, class received: {type(output_format).__name__}"
        )
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(
            f"border_type must be a String or str, class received: {type(border_type).__name__}"
        )
    
    # Get output_format as string for validation
    output_format_str = output_format.value if isinstance(output_format, datatypes.String) else output_format
    
    # Validate output_format against input image dtype
    image_np = image.to_numpy()
    input_dtype = image_np.dtype.type
    
    if input_dtype not in IMAGE_TYPE_FORMAT_TABLE:
        raise ValueError(
            f"Unsupported input image dtype: {input_dtype}. Supported dtypes: {list(IMAGE_TYPE_FORMAT_TABLE.keys())}"
        )
    
    allowed_formats = IMAGE_TYPE_FORMAT_TABLE[input_dtype]
    if output_format_str not in allowed_formats:
        raise ValueError(
            f"output_format '{output_format_str}' is not valid for input dtype {input_dtype}. "
            f"Allowed formats: {allowed_formats}"
        )
    
    if isinstance(kernel_size, int):
        kernel_size = datatypes.Int(kernel_size)
    if isinstance(normalize, bool):
        normalize = datatypes.Bool(normalize)
    if isinstance(output_format, str):
        output_format = datatypes.String(output_format)
    if isinstance(border_type, str):
        border_type = datatypes.String(border_type)

    # Prepare input data
    input_data = {
        "image": image,
        "kernel_size": kernel_size,
        "border_type": border_type,
        "normalize": normalize,
        "output_format": output_format,  # API still uses desired_depth
    }

    # Call the API
    end_point = "filter_image_using_box"
    response_data = _send_request(endpoint=end_point, input_data=input_data)

    # _run_arrow_filter default output_key is "filtered_image"
    filtered_image = response_data["filtered_image"]
    return filtered_image


def filter_image_using_gaussian_blur(
    image: datatypes.Image,
    kernel_size: datatypes.Int | int = datatypes.Int(15),
    sigma_x: datatypes.Float | float | int = datatypes.Float(3.0),
    sigma_y: datatypes.Float | float | int = datatypes.Float(3.0),
    border_type: datatypes.String | str = datatypes.String("default"),
) -> datatypes.Image:
    """
    Applies Gaussian blur for smooth noise reduction.

    Gaussian blur uses a Gaussian kernel for weighted averaging, providing natural-looking
    blur with better edge preservation than simple blur.

    Args:
        image: The input image to filter. Should be a Image object(H, W) or (H, W, C).
        kernel_size: The size of the Gaussian kernel. Must be odd. Increasing creates
            more blur. Typical range: 3-31. Use 3-7 for light blur, 7-15 for moderate,
            15-31 for heavy blur. Default: 15.
        sigma_x: The standard deviation in the X direction. Increasing creates
            more horizontal blur. When 0, computed from kernel_size. Typical range: 0.0-10.0.
            Use 0.0 for auto, 1.0-3.0 for light, 3.0-7.0 for moderate, 7.0-10.0 for heavy.
            Default: 3.0.
        sigma_y: The standard deviation in the Y direction. Increasing creates
            more vertical blur. When 0, computed from kernel_size. Typical range: 0.0-10.0.
            Use 0.0 for auto, 1.0-3.0 for light, 3.0-7.0 for moderate, 7.0-10.0 for heavy.
            Default: 3.0.
        border_type: The border handling mode. Options: "default", "constant", "replicate",
            "reflect", "wrap". Set using `datatypes.String("mode_name")`.
            Default: "default".

    Returns:
        A Image object containing the blurred image with the same shape as input.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(kernel_size, (datatypes.Int, int)):
        raise TypeError(
            f"kernel_size must be an Int or int, class received: {type(kernel_size).__name__}"
        )
    if not isinstance(sigma_x, (datatypes.Float, float, int)):
        raise TypeError(
            f"sigma_x must be a Float, float, or int, class received: {type(sigma_x).__name__}"
        )
    if not isinstance(sigma_y, (datatypes.Float, float, int)):
        raise TypeError(
            f"sigma_y must be a Float, float, or int, class received: {type(sigma_y).__name__}"
        )
    if not isinstance(border_type, (datatypes.String, str)):
        raise TypeError(
            f"border_type must be a String or str, class received: {type(border_type).__name__}"
        )
    
    if isinstance(kernel_size, int):
        kernel_size = datatypes.Int(kernel_size)
    if isinstance(sigma_x, (float, int)):
        sigma_x = datatypes.Float(sigma_x)
    if isinstance(sigma_y, (float, int)):
        sigma_y = datatypes.Float(sigma_y)
    if isinstance(border_type, str):
        border_type = datatypes.String(border_type)
    
     # Prepare input data
    input_data = {
        "image": image,
        "kernel_size": kernel_size,
        "sigma_x": sigma_x,
        "sigma_y": sigma_y,
        "border_type": border_type,
    }

    # Call the API
    end_point = "filter_image_using_gaussian_blur"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]


def filter_image_using_median_blur(
    image: datatypes.Image,
    kernel_size: datatypes.Int | int = datatypes.Int(5),
) -> datatypes.Image:
    """
    Applies median blur to reduce salt-and-pepper noise.

    Median blur replaces each pixel with the median of its neighborhood, effectively
    removing impulse noise while preserving edges.

    Args:
        image: The input image to filter. Should be a Image object(H, W) or (H, W, C).
        kernel_size: The size of the median filter kernel. Must be odd. Increasing removes
            larger noise spots but may blur fine details. Typical range: 3-15. Use 3-5
            for small noise, 5-9 for moderate, 9-15 for heavy noise. Default: 5.

    Returns:
        A Image object containing the filtered image with the same shape as input.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(kernel_size, (datatypes.Int, int)):
        raise TypeError(
            f"kernel_size must be an Int or int, class received: {type(kernel_size).__name__}"
        )
    
    if isinstance(kernel_size, int):
        kernel_size = datatypes.Int(kernel_size)
    
    # Prepare input data
    input_data = {"image": image, "kernel_size": kernel_size}

    # Call the API  
    end_point = "filter_image_using_median_blur"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]


def enhance_image_using_auto_gamma_correction(
    image: datatypes.Image,
) -> datatypes.Image:
    """
    Applies gamma correction for brightness adjustment.

    Gamma correction adjusts image brightness non-linearly, useful for display
    calibration and contrast enhancement.

    Args:
        image: The input image to process. Should be a Image object(H, W) or
            (H, W, C).

    Returns:
        A Image object containing the gamma-corrected image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )


    # Prepare input data
    input_data = {"image": image}

    # Call the API
    end_point = "enhance_image_using_auto_gamma_correction"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]


def enhance_image_using_white_balance(
    image: datatypes.Image,
) -> datatypes.Image:
    """
    Applies white balance correction to adjust color temperature.

    White balance removes color casts caused by lighting conditions, making images
    appear more natural.

    Args:
        image: The input image to process. Should be a Image object(H, W, C) with
            color channels.

    Returns:
        A Image object containing the white-balanced image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )

    # Prepare input data
    input_data = {"image": image}

    # Call the API
    end_point = "enhance_image_using_white_balance"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]

# ===================== Thinning =====================

def transform_mask_using_blob_thinning(
    image: datatypes.Image,
    thinning_type: datatypes.String | str,
) -> datatypes.Image:
    """
    Applies skeletonization (thinning) to binary images.

    Thinning reduces binary objects to their skeletons, useful for shape analysis
    and feature extraction.

    Args:
        image: The input binary image to process. Should be a grayscale numpy array
            (H, W) with values 0 and 255.
        thinning_type: The thinning algorithm to use. Options: "thinning_zhangsuen",
            "thinning_guohall". Set using `datatypes.String("method")`.
            Default: "thinning_zhangsuen".

    Returns:
        A Image object containing the skeletonized image.
    """
    if not isinstance(image,datatypes.Image):
        raise TypeError(
            f"image must be a Image object, class received: {type(image).__name__}"
        )
    if not isinstance(thinning_type, (datatypes.String, str)):
        raise TypeError(
            f"thinning_type must be a String or str, class received: {type(thinning_type).__name__}"
        )
    if isinstance(thinning_type, str):
        thinning_type = datatypes.String(thinning_type)

    # Prepare input data
    input_data = {"image": image, "thinning_type": thinning_type}

    # Call the API
    end_point = "transform_mask_using_blob_thinning"
    response_data = _send_request(endpoint=end_point, input_data=input_data)
    return response_data["filtered_image"]


