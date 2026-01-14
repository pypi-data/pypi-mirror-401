"""
Vision capability detection for target models.

Provides runtime testing to verify if a target chatbot supports
image/vision inputs, with manual enable/disable controls.

Usage:
    from src.utils.vision_detector import determine_vision_support

    vision_info = await determine_vision_support(
        target_config=target_config,
        connector=connector,
        enable_image_attacks=True  # Manual control
    )
"""

import asyncio
import base64
import structlog
from io import BytesIO
from typing import Dict, Any
from PIL import Image, ImageDraw

logger = structlog.get_logger()


async def test_vision_capability(connector, timeout_seconds: int = 10) -> Dict[str, Any]:
    """
    Test if target can process images by sending a test image.

    Sends a simple image with text "ZZ072538117GR" and checks if
    the target can read and respond with the text.

    Args:
        connector: Target connector instance
        timeout_seconds: Timeout for test (default: 10 seconds)

    Returns:
        Dict with:
            - supports_images: bool
            - test_method: str
            - confidence: str
            - error: Optional[str]
    """
    try:
        logger.info("vision_capability_test_starting", timeout=timeout_seconds)

        # Create simple test image with clear text
        img = Image.new("RGB", (400, 150), color="white")
        draw = ImageDraw.Draw(img)

        # Use default font (works on all systems)
        # Draw text large and clear
        draw.text((50, 50), "ZZ072538117GR", fill="black")
        draw.rectangle([40, 40, 360, 110], outline="black", width=2)

        # Encode to base64
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        test_image_data = base64.b64encode(buffer.read()).decode("utf-8")

        logger.info("vision_test_image_created", size_bytes=len(test_image_data), format="PNG")

        # Send test message with image
        response = await asyncio.wait_for(
            connector.send_message(
                message="What text do you see in this image? Please respond with only the text you see.",
                context={},
                image_data=test_image_data,
                image_mime_type="image/png",
            ),
            timeout=timeout_seconds,
        )

        response_content = response.get("content", "").lower()

        logger.info(
            "vision_test_response_received",
            response_length=len(response_content),
            response_preview=response_content[:200],
        )

        # Check if response contains the test text
        # Look for variations: "vision test 42", "visiontest42", "42", etc.
        test_phrases = [
            "vision_test_42",
            "vision test 42",
            "visiontest42",
            "vision-test-42",
            "42",
            "ZZ072538117GR",
        ]

        found = False
        for phrase in test_phrases:
            if phrase in response_content:
                found = True
                logger.info("vision_test_passed", matched_phrase=phrase)
                break

        if found:
            return {
                "supports_images": True,
                "test_method": "runtime_ocr_test",
                "confidence": "high",
                "error": None,
            }
        else:
            # Model responded but didn't read text - might not support vision
            logger.warning("vision_test_ambiguous", response_preview=response_content[:300])
            return {
                "supports_images": False,
                "test_method": "runtime_ocr_test",
                "confidence": "medium",
                "error": "Model responded but did not read image text",
            }

    except asyncio.TimeoutError:
        logger.error("vision_capability_test_timeout")
        return {
            "supports_images": False,
            "test_method": "runtime_ocr_test",
            "confidence": "low",
            "error": "Test timed out",
        }

    except AttributeError as e:
        # Connector doesn't support image parameters
        logger.warning("vision_test_connector_not_updated", error=str(e))
        return {
            "supports_images": False,
            "test_method": "runtime_ocr_test",
            "confidence": "high",
            "error": "Connector does not support image parameters (needs update)",
        }

    except Exception as e:
        logger.error("vision_capability_test_error", error=str(e), error_type=type(e).__name__)
        return {
            "supports_images": False,
            "test_method": "runtime_ocr_test",
            "confidence": "low",
            "error": str(e),
        }


async def determine_vision_support(
    target_config: Dict[str, Any], connector, enable_image_attacks: bool = True
) -> Dict[str, Any]:
    """
    Determine if image attacks should be used for this target.

    Decision logic:
    1. If enable_image_attacks=False → Skip image attacks (manual disable)
    2. If enable_image_attacks=True → Test runtime capability
    3. Store results in target_config for future reference

    Args:
        target_config: Target configuration dict
        connector: Target connector instance (must be initialized)
        enable_image_attacks: Manual on/off switch (default: True)

    Returns:
        Dict with:
            - supports_images: bool (final decision)
            - image_attacks_enabled: bool (manual setting)
            - runtime_test_passed: Optional[bool] (if tested)
            - detection_method: str
            - confidence: str
            - error: Optional[str]
    """
    logger.info(
        "determining_vision_support",
        enable_image_attacks=enable_image_attacks,
        target_name=target_config.get("name", "unknown"),
    )

    # Check manual override: User disabled image attacks
    if not enable_image_attacks:
        logger.info("image_attacks_manually_disabled")
        return {
            "supports_images": False,
            "image_attacks_enabled": False,
            "runtime_test_passed": None,
            "detection_method": "manual_disable",
            "confidence": "high",
            "error": None,
        }

    # User enabled image attacks - test if target supports them
    logger.info("running_vision_capability_test")

    test_result = await test_vision_capability(
        connector=connector, timeout_seconds=target_config.get("vision_test_timeout", 10)
    )

    # Build result
    result = {
        "supports_images": test_result["supports_images"],
        "image_attacks_enabled": True,  # User wants them enabled
        "runtime_test_passed": test_result["supports_images"],
        "detection_method": test_result["test_method"],
        "confidence": test_result["confidence"],
        "error": test_result.get("error"),
        "image_format": "openai",  # Default to OpenAI format for multimodal
    }

    logger.info(
        "vision_support_determined",
        supports_images=result["supports_images"],
        confidence=result["confidence"],
        method=result["detection_method"],
    )

    return result


def update_target_config_with_vision_detection(
    target_config: Dict[str, Any], vision_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update target config with vision detection results.

    Args:
        target_config: Original target config
        vision_info: Vision detection results from determine_vision_support()

    Returns:
        Updated target config
    """
    target_config["supports_images"] = vision_info["supports_images"]
    target_config["image_attacks_enabled"] = vision_info["image_attacks_enabled"]
    target_config["image_format"] = vision_info.get("image_format", "openai")

    # Store detection metadata
    target_config["_vision_detection"] = {
        "method": vision_info["detection_method"],
        "confidence": vision_info["confidence"],
        "runtime_test_passed": vision_info.get("runtime_test_passed"),
        "error": vision_info.get("error"),
    }

    logger.info(
        "target_config_updated_with_vision_info",
        supports_images=target_config["supports_images"],
        detection_method=vision_info["detection_method"],
    )

    return target_config
