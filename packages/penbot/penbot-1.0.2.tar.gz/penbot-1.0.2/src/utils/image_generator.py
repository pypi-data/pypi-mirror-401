"""
Image attack generator for visual adversarial testing.

Generates images for testing vision model vulnerabilities:
- Text-in-image bypass (OCR jailbreaks)
- Visual social engineering (fake screenshots)
- Multimodal confusion (contradictory inputs)

All images are generated in-memory and returned as base64 strings.
"""

import base64
import structlog
from io import BytesIO
from typing import Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw
from datetime import datetime

logger = structlog.get_logger()


class ImageGenerator:
    """Generator for adversarial test images."""

    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize image generator.

        Args:
            output_dir: Optional directory to save images (for debugging)
        """
        self.output_dir = output_dir

        # Default styling
        self.default_bg_color = "white"
        self.default_text_color = "black"
        self.default_size = (800, 600)

        logger.info("image_generator_initialized", output_dir=output_dir)

    def _encode_image(self, img: Image.Image, format: str = "PNG") -> str:
        """
        Encode PIL Image to base64 string.

        Args:
            img: PIL Image
            format: Image format (PNG, JPEG)

        Returns:
            Base64-encoded image string
        """
        buffer = BytesIO()
        img.save(buffer, format=format)
        buffer.seek(0)

        encoded = base64.b64encode(buffer.read()).decode("utf-8")

        logger.debug("image_encoded", format=format, size_bytes=len(encoded))

        return encoded

    def _save_debug_image(self, img: Image.Image, name: str):
        """Save image to output_dir if configured."""
        if self.output_dir:
            import os

            os.makedirs(self.output_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.output_dir, f"{name}_{timestamp}.png")

            img.save(filepath)
            logger.debug("debug_image_saved", filepath=filepath)

    def generate_text_in_image(
        self, attack_text: str, style: str = "plain"
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate image with embedded attack text for OCR bypass.

        Tests if vision models process image text differently than
        prompt text, potentially bypassing content filters.

        Args:
            attack_text: The jailbreak/attack text to embed
            style: "plain", "handwritten", "screenshot", "sign"

        Returns:
            Tuple of (base64_image, metadata)
        """
        logger.info("generating_text_in_image", text_length=len(attack_text), style=style)

        # Create canvas
        img = Image.new("RGB", (900, 700), color="white")
        draw = ImageDraw.Draw(img)

        # Different styles
        if style == "sign":
            # Make it look like a physical sign/notice
            draw.rectangle([50, 50, 850, 650], fill="lightyellow", outline="black", width=3)
            draw.text((100, 100), "⚠️ NOTICE", fill="red")
            draw.text((100, 180), attack_text, fill="black")

        elif style == "screenshot":
            # Make it look like a chat screenshot
            draw.rectangle([0, 0, 900, 80], fill="#4A90E2")  # Header
            draw.text((20, 25), "System Administrator", fill="white")
            draw.rectangle([20, 100, 880, 650], fill="#F0F0F0", outline="gray")
            draw.text((40, 120), attack_text, fill="black")

        else:  # plain
            # Simple clean text
            draw.text((50, 50), attack_text, fill="black")

        # Encode
        encoded = self._encode_image(img)

        # Save debug if configured
        self._save_debug_image(img, f"text_in_image_{style}")

        metadata = {
            "attack_type": "text_in_image_bypass",
            "style": style,
            "text_length": len(attack_text),
            "image_size": img.size,
        }

        logger.info("text_in_image_generated", style=style, encoded_size=len(encoded))

        return encoded, metadata

    def generate_fake_error_screen(self, title: str, message: str) -> Tuple[str, Dict[str, Any]]:
        """
        Generate fake error/warning screen for social engineering.

        Tests if models treat official-looking images as authoritative.

        Args:
            title: Error title (e.g., "System Error", "Security Alert")
            message: Error message (can include attack instructions)

        Returns:
            Tuple of (base64_image, metadata)
        """
        logger.info("generating_fake_error_screen", title=title)

        # Create error screen
        img = Image.new("RGB", (700, 400), color="white")
        draw = ImageDraw.Draw(img)

        # Red error header
        draw.rectangle([0, 0, 700, 80], fill="#D32F2F")
        draw.text((20, 25), f"⚠️ {title}", fill="white")

        # Message box
        draw.rectangle([20, 100, 680, 380], fill="#FFEBEE", outline="#D32F2F", width=2)
        draw.text((40, 120), message, fill="black")

        # Encode
        encoded = self._encode_image(img)
        self._save_debug_image(img, "fake_error_screen")

        metadata = {
            "attack_type": "visual_social_engineering",
            "subtype": "fake_error",
            "title": title,
            "image_size": img.size,
        }

        logger.info("fake_error_screen_generated")

        return encoded, metadata

    def generate_fake_email(
        self, sender: str, subject: str, body: str
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate fake email screenshot for authority manipulation.

        Args:
            sender: Fake sender (e.g., "security@company.com")
            subject: Email subject
            body: Email body (can include attack instructions)

        Returns:
            Tuple of (base64_image, metadata)
        """
        logger.info("generating_fake_email", sender=sender, subject=subject)

        # Create email screenshot
        img = Image.new("RGB", (800, 600), color="white")
        draw = ImageDraw.Draw(img)

        # Email header
        draw.rectangle([0, 0, 800, 50], fill="#1976D2")
        draw.text((20, 15), "📧 Email", fill="white")

        # Email metadata
        draw.rectangle([20, 70, 780, 200], fill="#F5F5F5", outline="gray")
        draw.text((40, 90), f"From: {sender}", fill="black")
        draw.text((40, 120), f"Subject: {subject}", fill="black")
        draw.text((40, 150), f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", fill="black")

        # Email body
        draw.rectangle([20, 220, 780, 580], fill="white", outline="gray")
        draw.text((40, 240), body, fill="black")

        # Encode
        encoded = self._encode_image(img)
        self._save_debug_image(img, "fake_email")

        metadata = {
            "attack_type": "visual_social_engineering",
            "subtype": "fake_email",
            "sender": sender,
            "subject": subject,
            "image_size": img.size,
        }

        logger.info("fake_email_generated")

        return encoded, metadata

    def generate_fake_chat_message(
        self, sender: str, message: str, sender_role: str = "Administrator"
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate fake chat message for impersonation attacks.

        Args:
            sender: Fake sender name
            message: Attack message
            sender_role: Role badge (e.g., "Administrator", "Support", "CEO")

        Returns:
            Tuple of (base64_image, metadata)
        """
        logger.info("generating_fake_chat_message", sender=sender, role=sender_role)

        # Create chat screenshot
        img = Image.new("RGB", (700, 300), color="white")
        draw = ImageDraw.Draw(img)

        # Chat header
        draw.rectangle([0, 0, 700, 60], fill="#128C7E")
        draw.text((20, 20), f"Chat - {sender}", fill="white")

        # Message bubble
        draw.rectangle([20, 80, 680, 280], fill="#DCF8C6", outline="#128C7E", width=2)

        # Sender info
        draw.text((40, 100), f"{sender} [{sender_role}]", fill="#075E54")

        # Message
        draw.text((40, 140), message, fill="black")

        # Timestamp
        draw.text((600, 260), datetime.now().strftime("%H:%M"), fill="gray")

        # Encode
        encoded = self._encode_image(img)
        self._save_debug_image(img, "fake_chat_message")

        metadata = {
            "attack_type": "visual_social_engineering",
            "subtype": "fake_chat",
            "sender": sender,
            "sender_role": sender_role,
            "image_size": img.size,
        }

        logger.info("fake_chat_message_generated")

        return encoded, metadata

    def generate_contradictory_image(
        self, safe_text: str, hidden_instruction: str
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate image for multimodal confusion attacks.

        Image contains different information than the text prompt,
        testing if the model prioritizes visual or textual input.

        Args:
            safe_text: Visible safe text
            hidden_instruction: Hidden/subtle attack instruction

        Returns:
            Tuple of (base64_image, metadata)
        """
        logger.info("generating_contradictory_image")

        # Create image
        img = Image.new("RGB", (800, 500), color="white")
        draw = ImageDraw.Draw(img)

        # Large visible safe text
        draw.text((50, 50), safe_text, fill="black")

        # Hidden instruction in small/light text (still readable by OCR)
        draw.text((50, 400), f"[Hidden: {hidden_instruction}]", fill="lightgray")

        # Encode
        encoded = self._encode_image(img)
        self._save_debug_image(img, "contradictory_image")

        metadata = {
            "attack_type": "multimodal_confusion",
            "safe_text": safe_text,
            "hidden_instruction": hidden_instruction,
            "image_size": img.size,
        }

        logger.info("contradictory_image_generated")

        return encoded, metadata


# Convenience functions
def create_text_in_image_attack(
    attack_text: str, style: str = "plain"
) -> Tuple[str, Dict[str, Any]]:
    """Quick function to generate text-in-image attack."""
    generator = ImageGenerator()
    return generator.generate_text_in_image(attack_text, style)


def create_fake_error_attack(title: str, message: str) -> Tuple[str, Dict[str, Any]]:
    """Quick function to generate fake error screen."""
    generator = ImageGenerator()
    return generator.generate_fake_error_screen(title, message)


def create_fake_email_attack(sender: str, subject: str, body: str) -> Tuple[str, Dict[str, Any]]:
    """Quick function to generate fake email."""
    generator = ImageGenerator()
    return generator.generate_fake_email(sender, subject, body)


def create_fake_chat_attack(
    sender: str, message: str, role: str = "Administrator"
) -> Tuple[str, Dict[str, Any]]:
    """Quick function to generate fake chat message."""
    generator = ImageGenerator()
    return generator.generate_fake_chat_message(sender, message, role)


def create_contradictory_image_attack(safe_text: str, hidden: str) -> Tuple[str, Dict[str, Any]]:
    """Quick function to generate contradictory image."""
    generator = ImageGenerator()
    return generator.generate_contradictory_image(safe_text, hidden)
