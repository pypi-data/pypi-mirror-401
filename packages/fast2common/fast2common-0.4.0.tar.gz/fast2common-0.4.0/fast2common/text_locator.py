#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Text Locator - Use AI to find the best text element when multiple matches exist

When ElementLocator finds multiple text matches, this locator uses AI to analyze
the screenshot and determine which match is most appropriate based on:
- Visual context (surrounding elements)
- Position relevance (top/middle/bottom)
- User intent (action context)
"""

import json
import os
import sys
import logging
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any

# Setup logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class TextLocator:
    """AI-powered text locator for finding the best match when multiple text elements exist"""

    def __init__(self, api_key: str = None, ai_client=None):
        """
        初始化AI文字定位器

        Args:
            api_key: 智谱 API Key，如果为None则从环境变量获取
            ai_client: 可选的 AIClient 实例用于复用
        """
        self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 ZHIPU_API_KEY 环境变量或传入 api_key 参数")

        # 使用传入的 ai_client 或创建新的
        if ai_client:
            self.ai_client = ai_client
        else:
            # 导入 AI 客户端
            try:
                from .ai_client import AIClient
                self.ai_client = AIClient(api_key=self.api_key, enable_analysis=True)
            except ImportError as e:
                logger.error(f"Failed to import AIClient: {e}")
                raise

    def find_best_text_match(
        self,
        text: str,
        candidates: List[Tuple[int, int]],
        screenshot_path: Path,
        context: Optional[str] = None,
        position_hint: Optional[str] = None
    ) -> Optional[Tuple[int, int]]:
        """
        在多个候选坐标中找到最合适的文字位置

        当XML解析找到多个相同文字的元素时，用AI分析截图来判断哪个最合适

        Args:
            text: 要查找的文字（如"考必过"）
            candidates: 候选坐标列表 [(x1, y1), (x2, y2), ...]
            screenshot_path: 截图路径
            context: 上下文描述（如"点击进入学习模式"）
            position_hint: 位置提示（如"顶部"、"中间"、"底部"）

        Returns:
            最佳匹配的坐标 (x, y)，如果无法确定则返回None

        Example:
            >>> candidates = [(100, 200), (300, 400), (500, 600)]
            >>> locator = TextLocator()
            >>> best = locator.find_best_text_match(
            ...     text="考必过",
            ...     candidates=candidates,
            ...     screenshot_path=Path("screenshot.png"),
            ...     context="点击进入测试",
            ...     position_hint="中间"
            ... )
            >>> print(best)  # (300, 400)
        """
        if not candidates:
            logger.error("❌ No candidates provided")
            return None

        if len(candidates) == 1:
            logger.info(f"✅ Only one candidate, returning: {candidates[0]}")
            return candidates[0]

        if not screenshot_path.exists():
            logger.error(f"❌ Screenshot not found: {screenshot_path}")
            return None

        try:
            # 构建AI提示词
            prompt = self._build_prompt(text, candidates, context, position_hint)

            # 调用AI分析
            logger.info(f"🔍 Using AI to find best match for text '{text}' from {len(candidates)} candidates")
            analysis_result = self.ai_client.analyze_screen(
                screenshot_path,
                task=prompt,
                response_format="json_object"
            )

            if not analysis_result.get('success'):
                error = analysis_result.get('error', 'Unknown error')
                logger.error(f"❌ AI analysis failed: {error}")
                # Fallback: return first candidate
                logger.warning(f"⚠️ Falling back to first candidate: {candidates[0]}")
                return candidates[0]

            # 解析AI返回的JSON
            analysis_text = analysis_result.get('analysis', '')
            if not analysis_text:
                logger.error("❌ AI returned empty analysis")
                return candidates[0]

            # 解析坐标
            best_coords = self._parse_ai_response(analysis_text, candidates)

            if best_coords:
                logger.info(f"✅ AI selected best match: {best_coords}")
                return best_coords
            else:
                logger.warning(f"⚠️ AI could not determine best match, using first candidate: {candidates[0]}")
                return candidates[0]

        except Exception as e:
            logger.error(f"❌ Error in find_best_text_match: {e}")
            import traceback
            traceback.print_exc()
            return candidates[0] if candidates else None

    def _build_prompt(
        self,
        text: str,
        candidates: List[Tuple[int, int]],
        context: Optional[str],
        position_hint: Optional[str]
    ) -> str:
        """
        构建AI分析提示词

        Args:
            text: 要查找的文字
            candidates: 候选坐标列表
            context: 上下文描述
            position_hint: 位置提示

        Returns:
            AI提示词字符串
        """
        # 构建候选位置描述
        candidates_desc = "\n".join([
            f"  候选{i+1}: ({x}, {y})"
            for i, (x, y) in enumerate(candidates)
        ])

        # 构建位置提示
        position_guidance = ""
        if position_hint:
            position_map = {
                "顶部": "screen top",
                "中间": "screen middle",
                "底部": "screen bottom",
                "top": "screen top",
                "middle": "screen middle",
                "bottom": "screen bottom"
            }
            position_guidance = f"\n位置提示：用户期望在屏幕{position_map.get(position_hint, position_hint)}找到元素"

        # 构建上下文描述
        context_desc = ""
        if context:
            context_desc = f"\n上下文：{context}"

        prompt = f"""请分析截图，帮我找到最合适的"{text}"文字位置。

{candidates_desc}
{position_guidance}
{context_desc}

请根据以下标准选择最合适的位置：
1. **可见性**：该位置的文字是否清晰可见、未被遮挡
2. **可点击性**：该位置是否是可点击的按钮或元素
3. **位置合理性**：该位置是否符合常见UI布局规范
4. **上下文匹配**：如果提供了上下文，选择最符合上下文的位置

请返回JSON格式：
{{
  "selected_index": <选择的候选索引，从1开始>,
  "coordinates": {{"x": <x坐标>, "y": <y坐标>}},
  "reason": "<选择理由，用中文说明>"
}}

注意：
- 只返回数字索引，不要返回其他内容
- 如果多个位置都合适，选择最显眼、最容易点击的那个
- 索引从1开始（候选1对应索引1）"""

        return prompt

    def _parse_ai_response(
        self,
        response_text: str,
        candidates: List[Tuple[int, int]]
    ) -> Optional[Tuple[int, int]]:
        """
        解析AI返回的JSON响应

        Args:
            response_text: AI返回的JSON文本
            candidates: 候选坐标列表（用于验证）

        Returns:
            解析出的坐标，如果解析失败则返回None
        """
        try:
            # 清理响应文本
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            # 解析JSON
            result = json.loads(response_text)

            # 提取选择的索引
            selected_index = result.get('selected_index')
            if selected_index is None:
                logger.error("❌ AI response missing 'selected_index'")
                return None

            # 索引从1开始，转换为0-based
            index = int(selected_index) - 1
            if index < 0 or index >= len(candidates):
                logger.error(f"❌ AI returned invalid index: {selected_index}, candidates: {len(candidates)}")
                return None

            # 提取坐标
            coords = result.get('coordinates')
            if coords:
                x = coords.get('x')
                y = coords.get('y')
                if x is not None and y is not None:
                    # 验证坐标是否在候选列表中
                    if (x, y) in candidates:
                        reason = result.get('reason', '')
                        logger.info(f"✅ AI selected candidate {selected_index} at ({x}, {y}): {reason}")
                        return (x, y)
                    else:
                        logger.warning(f"⚠️ AI returned coordinates not in candidates list: ({x}, {y})")
                        return candidates[index]

            # Fallback: 使用索引
            return candidates[index]

        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse AI response as JSON: {e}")
            logger.debug(f"Response text: {response_text}")
            return None
        except Exception as e:
            logger.error(f"❌ Error parsing AI response: {e}")
            return None

    def find_text_with_ai(
        self,
        text: str,
        screenshot_path: Path,
        position_hint: Optional[str] = None,
        context: Optional[str] = None
    ) -> Optional[Tuple[int, int]]:
        """
        直接使用AI查找文字位置（不需要候选列表）

        当XML解析完全失败时，用AI直接在截图中找文字

        Args:
            text: 要查找的文字
            screenshot_path: 截图路径
            position_hint: 位置提示（如"顶部"、"中间"、"底部"）
            context: 上下文描述

        Returns:
            文字中心坐标 (x, y)，如果未找到则返回None

        Example:
            >>> locator = TextLocator()
            >>> coords = locator.find_text_with_ai(
            ...     text="考必过",
            ...     screenshot_path=Path("screenshot.png"),
            ...     position_hint="中间"
            ... )
        """
        if not screenshot_path.exists():
            logger.error(f"❌ Screenshot not found: {screenshot_path}")
            return None

        try:
            # 构建AI提示词
            prompt = self._build_direct_search_prompt(text, position_hint, context)

            # 调用AI分析
            logger.info(f"🔍 Using AI to directly find text '{text}' in screenshot")
            analysis_result = self.ai_client.analyze_screen(
                screenshot_path,
                task=prompt,
                response_format="json_object"
            )

            if not analysis_result.get('success'):
                error = analysis_result.get('error', 'Unknown error')
                logger.error(f"❌ AI analysis failed: {error}")
                return None

            # 解析AI返回的JSON
            analysis_text = analysis_result.get('analysis', '')
            if not analysis_text:
                logger.error("❌ AI returned empty analysis")
                return None

            # 解析坐标
            coords = self._parse_direct_search_response(analysis_text, text)

            if coords:
                logger.info(f"✅ AI found text '{text}' at: {coords}")
                return coords
            else:
                logger.warning(f"⚠️ AI could not find text '{text}'")
                return None

        except Exception as e:
            logger.error(f"❌ Error in find_text_with_ai: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _build_direct_search_prompt(
        self,
        text: str,
        position_hint: Optional[str],
        context: Optional[str]
    ) -> str:
        """构建直接搜索提示词"""
        position_desc = ""
        if position_hint:
            position_desc = f"\n位置提示：请在屏幕{position_hint}区域查找"

        context_desc = ""
        if context:
            context_desc = f"\n上下文：{context}"

        prompt = f"""请在截图中找到文字"{text}"的中心位置。

{position_desc}
{context_desc}

请返回JSON格式：
{{
  "found": <true/false, 是否找到文字>,
  "coordinates": {{"x": <中心x坐标>, "y": <中心y坐标>}},
  "confidence": <高/中/低, 匹配置信度>,
  "reason": "<选择理由，用中文说明>"
}}

注意：
- 如果找到多个相同的文字，选择最显眼、最容易点击的那个
- 如果找不到文字，found返回false
- 坐标是文字元素的中心点，用于点击"""

        return prompt

    def _parse_direct_search_response(
        self,
        response_text: str,
        text: str
    ) -> Optional[Tuple[int, int]]:
        """解析直接搜索的AI响应"""
        try:
            # 清理响应文本
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            # 解析JSON
            result = json.loads(response_text)

            # 检查是否找到
            found = result.get('found', False)
            if not found:
                return None

            # 提取坐标
            coords = result.get('coordinates')
            if coords:
                x = coords.get('x')
                y = coords.get('y')
                if x is not None and y is not None:
                    confidence = result.get('confidence', 'unknown')
                    reason = result.get('reason', '')
                    logger.info(f"✅ AI found text '{text}' with confidence {confidence}: {reason}")
                    return (x, y)

            return None

        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse AI response as JSON: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error parsing AI response: {e}")
            return None
