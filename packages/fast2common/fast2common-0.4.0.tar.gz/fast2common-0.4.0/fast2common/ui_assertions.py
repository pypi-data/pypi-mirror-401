#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI Assertions - Verify UI state and elements
Provides assertion methods for validating page content and UI state
"""

import time
import tempfile
import logging
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from xml.etree import ElementTree as ET

from .element_locator import ElementLocator
from .adb_controller import ADBController

# Setup logger
logger = logging.getLogger(__name__)


class UIAssertions:
    """UI assertions for verifying page content and elements"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize UI assertions

        Args:
            api_key: Zhipu AI API key for icon recognition (optional)
        """
        self.element_locator = ElementLocator()
        self.icon_locator = None
        if api_key:
            try:
                from .icon_locator import IconLocator
                self.icon_locator = IconLocator(api_key=api_key)
                logger.info("IconLocator initialized with AI capability")
            except Exception as e:
                logger.warning(f"Failed to initialize IconLocator: {e}")

    def assert_element_present(
        self,
        element: str,
        device_id: Optional[str] = None,
        element_type: str = "auto",
        position_hint: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Assert that an element (text or icon) is present on current page
        Automatically detects element type and uses appropriate method

        Args:
            element: Element text or icon description
            device_id: Device ID (optional)
            element_type: Element type - "text", "icon", or "auto" (default: "auto")
            position_hint: Position hint for icon (e.g., "top", "bottom", "left", "right")

        Returns:
            Dict with assertion result:
            {
                "success": bool,              # True if element found
                "element": str,               # Searched element
                "element_type": str,          # Detected or specified type ("text" or "icon")
                "coordinates": tuple or None, # (x, y) if found
                "method": str,                # Method used ("ocr", "ai", "hybrid")
                "message": str,               # Result message
                "search_time": float,         # Time taken for search
                "confidence": float           # Confidence score (0.0-1.0) if AI used
            }
        """
        start_time = time.time()
        search_element = element.strip()

        try:
            # Determine element type if auto
            detected_type = element_type
            if element_type == "auto":
                # Simple heuristic: if contains Chinese char and length <= 4, likely icon
                has_chinese = any('\u4e00' <= c <= '\u9fff' for c in search_element)
                if has_chinese and len(search_element) <= 4:
                    detected_type = "icon"
                else:
                    detected_type = "text"

            logger.info(f"Searching for element '{search_element}' (type: {detected_type})")

            # Strategy 1: Try OCR/text-based search first (fast)
            if detected_type in ["text", "auto"]:
                coords = self.element_locator.find_clickable_element_center(
                    text=search_element,
                    device_id=device_id,
                    strict_match=False
                )

                if coords:
                    search_time = time.time() - start_time
                    return {
                        "success": True,
                        "element": search_element,
                        "element_type": "text",
                        "coordinates": coords,
                        "method": "ocr",
                        "message": f"Element '{search_element}' found at {coords} (OCR)",
                        "search_time": search_time,
                        "confidence": 0.95
                    }

            # Strategy 2: Try AI icon recognition (slower but more powerful)
            if detected_type in ["icon", "auto"] and self.icon_locator:
                logger.info(f"Using AI to locate icon: {search_element}")
                coords = self.icon_locator.find_icon_center(
                    icon_description=search_element,
                    position_description=position_hint,
                    device_id=device_id
                )

                if coords:
                    search_time = time.time() - start_time
                    return {
                        "success": True,
                        "element": search_element,
                        "element_type": "icon",
                        "coordinates": coords,
                        "method": "ai",
                        "message": f"Element '{search_element}' found at {coords} (AI)" +
                                  (f" at {position_hint}" if position_hint else ""),
                        "search_time": search_time,
                        "confidence": 0.85
                    }

            # Element not found
            search_time = time.time() - start_time
            return {
                "success": False,
                "element": search_element,
                "element_type": detected_type,
                "coordinates": None,
                "method": "hybrid",
                "message": f"Element '{search_element}' not found (tried OCR + AI)" +
                          (f" at {position_hint}" if position_hint else ""),
                "search_time": search_time,
                "confidence": 0.0
            }

        except Exception as e:
            search_time = time.time() - start_time
            logger.error(f"Error searching for element '{search_element}': {e}")
            return {
                "success": False,
                "element": search_element,
                "element_type": detected_type if 'detected_type' in locals() else "unknown",
                "coordinates": None,
                "method": "error",
                "message": f"Error: {str(e)}",
                "search_time": search_time,
                "confidence": 0.0
            }

    def assert_text_present(
        self,
        text: str,
        device_id: Optional[str] = None,
        timeout: int = 5,
        strict_match: bool = False
    ) -> Dict[str, Any]:
        """
        Assert that specified text is present on current page (legacy method, uses OCR only)

        Args:
            text: Text to search for
            device_id: Device ID (optional)
            timeout: Retry timeout in seconds (default: 5)
            strict_match: Whether to use strict text matching (default: False)

        Returns:
            Dict with assertion result
        """
        start_time = time.time()
        search_text = text.strip()

        try:
            # Try to find element with text using OCR
            coords = self.element_locator.find_clickable_element_center(
                text=search_text,
                device_id=device_id,
                strict_match=strict_match
            )

            search_time = time.time() - start_time

            if coords:
                return {
                    "success": True,
                    "text": search_text,
                    "coordinates": coords,
                    "message": f"Text '{search_text}' found at ({coords[0]}, {coords[1]})",
                    "search_time": search_time,
                    "method": "ocr"
                }
            else:
                return {
                    "success": False,
                    "text": search_text,
                    "coordinates": None,
                    "message": f"Text '{search_text}' not found on current page",
                    "search_time": search_time,
                    "method": "ocr"
                }

        except Exception as e:
            search_time = time.time() - start_time
            return {
                "success": False,
                "text": search_text,
                "coordinates": None,
                "message": f"Error searching for text '{search_text}': {str(e)}",
                "search_time": search_time,
                "method": "error"
            }

    def assert_text_absent(
        self,
        text: str,
        device_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Assert that specified text is NOT present on current page

        Args:
            text: Text to verify absence of
            device_id: Device ID (optional)

        Returns:
            Dict with assertion result (same format as assert_text_present)
        """
        result = self.assert_text_present(text, device_id)

        # Invert success flag
        result["success"] = not result["success"]

        if result["success"]:
            result["message"] = f"Text '{text}' correctly absent from page"
        else:
            result["message"] = f"Text '{text}' unexpectedly found on page"

        return result

    def assert_texts_present(
        self,
        texts: list,
        device_id: Optional[str] = None,
        require_all: bool = True
    ) -> Dict[str, Any]:
        """
        Assert that multiple texts are present on current page

        Args:
            texts: List of texts to search for
            device_id: Device ID (optional)
            require_all: If True, all texts must be found; if False, at least one must be found

        Returns:
            Dict with assertion result:
            {
                "success": bool,
                "found_count": int,
                "total_count": int,
                "found_texts": list,
                "missing_texts": list,
                "results": list  # Individual results for each text
            }
        """
        results = []
        found_texts = []
        missing_texts = []

        for text in texts:
            result = self.assert_text_present(text, device_id)
            results.append(result)

            if result["success"]:
                found_texts.append(text)
            else:
                missing_texts.append(text)

        if require_all:
            success = len(missing_texts) == 0
        else:
            success = len(found_texts) > 0

        return {
            "success": success,
            "found_count": len(found_texts),
            "total_count": len(texts),
            "found_texts": found_texts,
            "missing_texts": missing_texts,
            "results": results
        }

    def assert_element_visible(
        self,
        text: str,
        device_id: Optional[str] = None,
        y_position: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Assert that an element with specified text is visible on screen

        Args:
            text: Element text to search for
            device_id: Device ID (optional)
            y_position: Y position range - "top", "middle", or "bottom" (optional)

        Returns:
            Dict with assertion result:
            {
                "success": bool,
                "text": str,
                "coordinates": tuple or None,
                "y_position": str,
                "message": str
            }
        """
        try:
            coords = self.element_locator.find_clickable_element_center(
                text=text,
                device_id=device_id,
                y_position=y_position
            )

            if coords:
                return {
                    "success": True,
                    "text": text,
                    "coordinates": coords,
                    "y_position": y_position or "any",
                    "message": f"Element '{text}' visible at ({coords[0]}, {coords[1]})" +
                              (f" in {y_position} region" if y_position else "")
                }
            else:
                return {
                    "success": False,
                    "text": text,
                    "coordinates": None,
                    "y_position": y_position or "any",
                    "message": f"Element '{text}' not visible" +
                              (f" in {y_position} region" if y_position else "")
                }

        except Exception as e:
            return {
                "success": False,
                "text": text,
                "coordinates": None,
                "y_position": y_position or "any",
                "message": f"Error checking element visibility: {str(e)}"
            }
