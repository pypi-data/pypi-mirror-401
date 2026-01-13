#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Element locator - Find clickable element center coordinates by text
"""

import time
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Tuple, List

from .adb_controller import ADBController
from .ui_analyzer import UIAnalyzer


class ElementLocator:
    """Element locator for finding clickable element center coordinates by text"""
    
    def __init__(self):
        """Initialize element locator"""
        self.ui_analyzer = UIAnalyzer()
    
    def _calculate_y_range(self, y_position: str, screen_height: int) -> Tuple[int, int]:
        """
        Calculate Y coordinate range based on position string
        
        Args:
            y_position: Position string - "top", "middle", or "bottom"
            screen_height: Screen height in pixels
        
        Returns:
            (y_min, y_max) tuple
        """
        if y_position == "top":
            return (0, screen_height // 3)
        elif y_position == "middle":
            return (screen_height // 3, 2 * screen_height // 3)
        elif y_position == "bottom":
            return (2 * screen_height // 3, screen_height)
        else:
            raise ValueError(f"Invalid y_position: {y_position}. Must be 'top', 'middle', or 'bottom'")
    
    def find_clickable_element_center(
        self,
        text: str,
        device_id: Optional[str] = None,
        y_position: Optional[str] = None,
        strict_match: bool = True
    ) -> Optional[Tuple[int, int]]:
        """
        Find clickable element center coordinates by text

        Supports OR logic: if text contains "或", "or", or "|", will match any of the alternatives.
        Example: "登录或注册" will match either "登录" or "注册"

        Args:
            text: Text to search for (supports OR logic with "或", "or", "|")
            device_id: Device ID (optional, uses current device if not provided)
            y_position: Y coordinate range limit - "top" (upper third), "middle" (middle third), "bottom" (lower third)
            strict_match: Whether to use strict text matching (default: True)

        Returns:
            (x, y) center coordinates or None if not found

        Example:
            # Find element in upper third
            coords = locator.find_clickable_element_center("登录", device_id="device123", y_position="top")

            # Find element in middle third
            coords = locator.find_clickable_element_center("搜索", y_position="middle")

            # Find element in lower third (bottom navigation)
            coords = locator.find_clickable_element_center("我的", y_position="bottom")

            # No Y range limit
            coords = locator.find_clickable_element_center("设置")

            # OR logic - match any of the alternatives
            coords = locator.find_clickable_element_center("登录或注册")  # Matches "登录" OR "注册"
            coords = locator.find_clickable_element_center("确定 or 确认 or OK")  # Matches any of these
        """
        import re

        try:
            # Check if text contains OR logic (支持中文"或"和英文"or"/"|")
            or_patterns = ['或', ' or ', ' Or ', ' OR ', '|']
            has_or = any(pattern in text for pattern in or_patterns)

            # Split into multiple options if OR logic is detected
            if has_or:
                # Try different patterns to find the best match
                if '|' in text:
                    options = [opt.strip() for opt in text.split('|')]
                elif ' or ' in text.lower():
                    options = re.split(r'\s+or\s+', text, flags=re.IGNORECASE)
                elif '或' in text:
                    options = text.split('或')
                else:
                    options = [text]

                # Clean options
                options = [opt.strip() for opt in options if opt.strip()]

                print(f"  🔀 Detected OR logic in text: '{text}' -> {len(options)} options: {options}")

                # Try each option until one matches
                for option in options:
                    print(f"     Trying option: '{option}'")
                    result = self._find_single_element(
                        text=option,
                        device_id=device_id,
                        y_position=y_position,
                        strict_match=strict_match
                    )
                    if result:
                        x, y = result
                        print(f"     ✅ Matched with option: '{option}' at ({x}, {y})")
                        return result
                    else:
                        print(f"     ❌ No match for option: '{option}'")

                print(f"  ❌ No match found for any option")
                return None
            else:
                # No OR logic, use original single-text logic
                return self._find_single_element(
                    text=text,
                    device_id=device_id,
                    y_position=y_position,
                    strict_match=strict_match
                )

        except Exception as e:
            print(f"  ❌ Error finding element: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _find_single_element(
        self,
        text: str,
        device_id: Optional[str] = None,
        y_position: Optional[str] = None,
        strict_match: bool = True
    ) -> Optional[Tuple[int, int]]:
        """
        Find a single element by text (internal method, no OR logic)

        Args:
            text: Single text to search for
            device_id: Device ID
            y_position: Y coordinate range limit
            strict_match: Whether to use strict text matching

        Returns:
            (x, y) center coordinates or None if not found
        """
        try:
            # Create ADB controller
            adb = ADBController(device_id=device_id)

            # Get screen size for Y range calculation
            screen_width, screen_height = adb.get_screen_size()

            # Calculate Y coordinate range if y_position is provided
            y_range = None
            if y_position:
                if y_position not in ["top", "middle", "bottom"]:
                    print(f"  ⚠️  Invalid y_position: {y_position}. Must be 'top', 'middle', or 'bottom'")
                    return None
                y_range = self._calculate_y_range(y_position, screen_height)
                print(f"  📍 Y range limit: {y_position} ({y_range[0]}-{y_range[1]})")

            # Get UI dump
            temp_xml = Path(tempfile.gettempdir()) / f"ui_locator_{int(time.time())}.xml"
            if not adb.get_ui_xml(temp_xml):
                print(f"  ❌ Failed to get UI dump")
                return None

            # Parse XML to get root element (needed for parent search)
            try:
                tree = ET.parse(temp_xml)
                root = tree.getroot()
            except Exception as e:
                print(f"  ❌ Failed to parse UI XML: {e}")
                try:
                    temp_xml.unlink(missing_ok=True)
                except Exception:
                    pass
                return None

            # Find element by text
            result = self.ui_analyzer.find_element_by_text(
                temp_xml,
                text,
                strict_match=strict_match,
                y_range=y_range
            )

            # Clean up temp file
            try:
                temp_xml.unlink(missing_ok=True)
            except Exception:
                pass

            if not result:
                return None

            bounds, match_type, element = result

            # If element is not clickable, try to find clickable parent
            if match_type in ['not_clickable', 'contains_not_clickable']:
                print(f"  🔍 Element found but not clickable, searching for clickable parent...")
                try:
                    parent_bounds = self.ui_analyzer._find_clickable_parent(element, root)
                    if parent_bounds:
                        bounds = parent_bounds
                        match_type = 'parent_container'
                        print(f"  ✅ Found clickable parent container")
                    else:
                        print(f"  ❌ No clickable parent found")
                        return None
                except Exception as e:
                    print(f"  ⚠️  Failed to find clickable parent: {e}")
                    return None

            # Parse bounds to get center coordinates
            # Note: UI Automator dump returns bounds in physical pixels, not dp
            # These coordinates can be used directly with adb tap command (which expects pixels)
            center_coords = self.ui_analyzer.parse_bounds(bounds)

            if center_coords:
                x, y = center_coords
                print(f"  ✅ Found element '{text}' at center: ({x}, {y}) [match_type: {match_type}, pixel coordinates]")
                return (x, y)
            else:
                print(f"  ❌ Failed to parse bounds: {bounds}")
                return None

        except Exception as e:
            print(f"  ❌ Error finding element: {e}")
            import traceback
            traceback.print_exc()
            return None

    def find_all_elements(
        self,
        text: str,
        device_id: Optional[str] = None,
        y_position: Optional[str] = None,
        strict_match: bool = True
    ) -> Optional[List[Tuple[int, int]]]:
        """
        Find all elements matching the text (returns multiple coordinates)

        Use this method when you expect multiple matches and want to use AI to select the best one.

        Args:
            text: Text to search for
            device_id: Device ID (optional, uses current device if not provided)
            y_position: Y coordinate range limit - "top" (upper third), "middle" (middle third), "bottom" (lower third)
            strict_match: Whether to use strict text matching (default: True)

        Returns:
            List of (x, y) center coordinates, or None if no matches found

        Example:
            >>> # Find all "登录" buttons
            >>> candidates = locator.find_all_elements("登录", y_position="middle")
            >>> print(candidates)  # [(100, 200), (300, 400), (500, 600)]
        """
        import time
        from pathlib import Path

        try:
            # Create ADB controller
            adb = ADBController(device_id=device_id)

            # Get screen size for Y range calculation
            screen_width, screen_height = adb.get_screen_size()

            # Calculate Y coordinate range if y_position is provided
            y_range = None
            if y_position:
                if y_position not in ["top", "middle", "bottom"]:
                    print(f"  ⚠️  Invalid y_position: {y_position}. Must be 'top', 'middle', or 'bottom'")
                    return None
                y_range = self._calculate_y_range(y_position, screen_height)
                print(f"  📍 Y range limit: {y_position} ({y_range[0]}-{y_range[1]})")

            # Get UI dump
            temp_xml = Path(tempfile.gettempdir()) / f"ui_locator_{int(time.time())}.xml"
            if not adb.get_ui_xml(temp_xml):
                print(f"  ❌ Failed to get UI dump")
                return None

            # Parse XML to get root element
            try:
                tree = ET.parse(temp_xml)
                root = tree.getroot()
            except Exception as e:
                print(f"  ❌ Failed to parse UI XML: {e}")
                try:
                    temp_xml.unlink(missing_ok=True)
                except Exception:
                    pass
                return None

            # Find ALL elements by text
            all_results = self.ui_analyzer.find_all_elements_by_text(
                temp_xml,
                text,
                strict_match=strict_match,
                y_range=y_range
            )

            # Clean up temp file
            try:
                temp_xml.unlink(missing_ok=True)
            except Exception:
                pass

            if not all_results:
                return None

            # Parse all results to get center coordinates
            candidates = []
            for bounds, match_type, element in all_results:
                # If element is not clickable, try to find clickable parent
                if match_type in ['not_clickable', 'contains_not_clickable']:
                    try:
                        parent_bounds = self.ui_analyzer._find_clickable_parent(element, root)
                        if parent_bounds:
                            bounds = parent_bounds
                        else:
                            continue  # Skip this element if no clickable parent
                    except Exception:
                        continue  # Skip this element on error

                # Parse bounds to get center coordinates
                center_coords = self.ui_analyzer.parse_bounds(bounds)
                if center_coords:
                    x, y = center_coords
                    candidates.append((x, y))
                    print(f"  ✅ Found element '{text}' at: ({x}, {y}) [match_type: {match_type}]")

            if candidates:
                print(f"  📊 Found {len(candidates)} candidates for '{text}'")
                return candidates
            else:
                print(f"  ❌ No valid candidates found")
                return None

        except Exception as e:
            print(f"  ❌ Error finding all elements: {e}")
            import traceback
            traceback.print_exc()
            return None

