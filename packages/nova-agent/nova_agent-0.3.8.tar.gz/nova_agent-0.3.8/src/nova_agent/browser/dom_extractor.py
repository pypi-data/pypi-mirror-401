"""DOM extraction utilities.

Extracts filtered interactive elements from Playwright pages for AI code generation.
Mirrors the Cloud mode DomParserService logic.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import structlog
from playwright.async_api import Page

logger = structlog.get_logger(__name__)


# =============================================================================
# Constants (same as Cloud mode DomParserService)
# =============================================================================

# 추출 대상 셀렉터 - 모든 웹사이트에서 인터랙티브 요소 캡처
INTERACTIVE_SELECTORS = [
    # 폼 입력 요소
    "input",
    "textarea",
    "select",
    "option",
    "datalist",
    "output",
    # 버튼 및 링크
    "button",
    "a",
    '[role="button"]',
    '[role="link"]',
    '[role="menuitem"]',
    '[role="menuitemcheckbox"]',
    '[role="menuitemradio"]',
    '[role="option"]',
    '[role="tab"]',
    '[role="switch"]',
    '[role="checkbox"]',
    '[role="radio"]',
    '[role="slider"]',
    '[role="spinbutton"]',
    '[role="combobox"]',
    '[role="listbox"]',
    '[role="searchbox"]',
    '[role="textbox"]',
    # 폼 컨테이너
    "form",
    "label",
    "fieldset",
    "legend",
    # 인터랙티브 속성
    "[onclick]",
    "[onchange]",
    "[onsubmit]",
    "[tabindex]",
    "[contenteditable]",
    "[draggable='true']",
    # 클릭 가능한 요소 (SPA 프레임워크)
    "span[class*='cursor-pointer']",
    "div[class*='cursor-pointer']",
    "span[class*='clickable']",
    "div[class*='clickable']",
    "[class*='btn']",
    "[class*='button']",
    "[class*='click']",
    "[class*='action']",
    "[class*='interactive']",
    "[class*='card']",
    "[class*='item']",
    "[class*='menu']",
    "[class*='link']",
    "[class*='trigger']",
    "[class*='toggle']",
    # 이미지 (클릭 가능한 경우 많음)
    "img",
    # iframe
    "iframe",
    # SVG 인터랙티브 요소
    "svg[onclick]",
    "svg[role]",
    # 데이터 속성
    "[data-action]",
    "[data-click]",
    "[data-clickable]",
    "[data-interactive]",
    "[data-href]",
    "[data-url]",
    "[data-link]",
    # 미디어 컨트롤
    "video",
    "audio",
    # 확장/축소 요소
    "details",
    "summary",
    # 대화상자/모달
    "dialog",
    '[role="dialog"]',
    '[role="alertdialog"]',
    # 탐색 요소
    "nav",
    "main",
    "header",
    "footer",
    "aside",
    "section",
    "article",
    # 테이블
    "table",
    "th",
    '[role="grid"]',
    '[role="row"]',
    '[role="gridcell"]',
    # 리스트
    '[role="listitem"]',
    # 트리뷰
    '[role="tree"]',
    '[role="treeitem"]',
    # 툴바
    '[role="toolbar"]',
    # 탭 패널
    '[role="tablist"]',
    '[role="tabpanel"]',
    # 프로그레스/상태
    "progress",
    "meter",
    '[role="progressbar"]',
    '[role="status"]',
    '[role="alert"]',
    # 상태 표시 요소
    "[id*='loading']",
    "[class*='loading']",
    "[id*='spinner']",
    "[class*='spinner']",
    "[id*='result']",
    "[class*='result']",
    "[id*='error']",
    "[class*='error']",
    "[id*='success']",
    "[class*='success']",
    "[id*='message']",
    "[class*='message']",
    "[id*='notification']",
    "[class*='notification']",
    "[id*='toast']",
    "[class*='toast']",
    "[id*='alert']",
    "[class*='alert']",
    "[id*='status']",
    "[class*='status']",
    "[aria-live]",
    "[aria-busy]",
    "[data-loading]",
    "[data-status]",
    "[data-state]",
    # 헤드라인
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    # 리스트 아이템
    "li",
    # 테이블 데이터
    "td",
    "tr",
]

# 추출할 속성 목록
ATTRIBUTES_TO_EXTRACT = [
    # 기본 식별자
    "id",
    "class",
    "name",
    "type",
    # 폼 관련
    "placeholder",
    "value",
    "min",
    "max",
    "step",
    "minlength",
    "maxlength",
    "pattern",
    "autocomplete",
    "inputmode",
    "accept",
    "multiple",
    # Label 연결
    "for",
    # 링크/네비게이션
    "href",
    "target",
    "download",
    "rel",
    # 접근성 (ARIA)
    "aria-label",
    "aria-labelledby",
    "aria-describedby",
    "aria-placeholder",
    "aria-valuemin",
    "aria-valuemax",
    "aria-valuenow",
    "aria-valuetext",
    "aria-expanded",
    "aria-selected",
    "aria-checked",
    "aria-pressed",
    "aria-hidden",
    "aria-disabled",
    "aria-required",
    "aria-invalid",
    "aria-busy",
    "aria-live",
    "aria-haspopup",
    "aria-controls",
    "aria-owns",
    "aria-current",
    # 상태
    "disabled",
    "readonly",
    "required",
    "checked",
    "selected",
    "open",
    "hidden",
    # 데이터 속성
    "data-testid",
    "data-test",
    "data-cy",
    "data-qa",
    "data-id",
    "data-value",
    "data-state",
    "data-status",
    "data-selected",
    "data-active",
    "data-disabled",
    # 역할
    "role",
    # 미디어
    "src",
    "alt",
    "title",
    # 기타
    "contenteditable",
    "tabindex",
    "draggable",
    "spellcheck",
]


class DomExtractor:
    """DOM 추출기.

    Playwright Page에서 필터링된 인터랙티브 요소를 추출합니다.
    Cloud 모드의 DomParserService와 동일한 로직 사용.

    Responsibilities:
        1. 인터랙티브 요소 필터링 및 추출
        2. URL, 타이틀 등 메타데이터 수집
        3. DOM 데이터 구조화
    """

    def __init__(
        self,
        page: Page,
        max_elements: int = 1000,
        max_text_length: int = 200,
        include_hidden: bool = False,
    ) -> None:
        """Initialize DOM extractor.

        Args:
            page: Playwright 페이지
            max_elements: 최대 추출 요소 수 (default: 1000)
            max_text_length: 요소별 최대 텍스트 길이 (default: 200)
            include_hidden: 숨겨진 요소 포함 여부
        """
        self._page = page
        self._max_elements = max_elements
        self._max_text_length = max_text_length
        self._include_hidden = include_hidden

    async def extract(self) -> dict[str, Any]:
        """DOM 추출.

        Cloud 모드와 동일한 방식으로 필터링된 인터랙티브 요소를 추출합니다.

        Returns:
            DOM 데이터 딕셔너리:
            - url: 현재 URL
            - title: 페이지 타이틀
            - elements: 필터링된 인터랙티브 요소 목록
            - html: 페이지 전체 HTML (fallback용)
            - timestamp: 추출 시간 (ISO 8601)
            - viewport: 뷰포트 크기
            - scroll_info: 스크롤 정보
            - modal_open: 모달 열림 여부
        """
        logger.debug("extracting_dom")

        # 페이지 정보 수집
        url = self._page.url
        title = await self._page.title()

        # 뷰포트 크기
        viewport = self._page.viewport_size

        # 타임스탬프
        timestamp = datetime.now(UTC).isoformat()

        # 모달 감지
        modal_info = await self._detect_modal()

        # 필터링된 인터랙티브 요소 추출
        elements, scroll_info = await self._extract_elements(modal_info)

        # HTML (fallback용 - 30KB로 제한)
        html = await self._extract_raw_html(max_length=30000)

        dom_data = {
            "url": url,
            "title": title,
            "elements": elements,
            "html": html,
            "timestamp": timestamp,
            "viewport": viewport,
            "scroll_info": scroll_info,
            "modal_open": modal_info.get("isOpen", False),
            "modal_z_index": modal_info.get("modalZIndex"),
        }

        # Log warning if max_elements limit was reached
        if len(elements) >= self._max_elements:
            logger.warning(
                "DOM extraction hit max_elements limit",
                element_count=len(elements),
                max_elements=self._max_elements,
                url=url,
                hint="Some elements may be missing. Consider increasing max_elements.",
            )

        logger.info(
            "dom_extracted",
            url=url,
            title=title,
            element_count=len(elements),
            max_elements=self._max_elements,
            html_length=len(html),
        )

        return dom_data

    async def _detect_modal(self) -> dict[str, Any]:
        """모달/다이얼로그 감지."""
        js_code = """
        () => {
            // Semantic modal selectors
            const semanticSelectors = [
                '[role="dialog"]',
                '[role="alertdialog"]',
                '[aria-modal="true"]'
            ];

            for (const selector of semanticSelectors) {
                const modal = document.querySelector(selector);
                if (modal) {
                    const style = window.getComputedStyle(modal);
                    if (style.display !== 'none' && style.visibility !== 'hidden') {
                        const zIndex = parseInt(style.zIndex) || 0;
                        return {
                            isOpen: true,
                            modalSelector: selector,
                            modalZIndex: zIndex
                        };
                    }
                }
            }

            // Class-based selectors
            const classSelectors = [
                '.modal:not(.hidden)',
                '.modal-overlay',
                'div[class*="modal"][class*="open"]',
                'div[class*="dialog"][class*="open"]'
            ];

            for (const selector of classSelectors) {
                const modal = document.querySelector(selector);
                if (modal) {
                    const style = window.getComputedStyle(modal);
                    if (style.display !== 'none' && style.visibility !== 'hidden') {
                        const zIndex = parseInt(style.zIndex) || 0;
                        return {
                            isOpen: true,
                            modalSelector: selector,
                            modalZIndex: zIndex
                        };
                    }
                }
            }

            return { isOpen: false, modalSelector: null, modalZIndex: null };
        }
        """
        try:
            return await self._page.evaluate(js_code)
        except Exception:
            return {"isOpen": False, "modalSelector": None, "modalZIndex": None}

    async def _extract_elements(
        self, modal_info: dict[str, Any]
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """인터랙티브 요소 추출 (Cloud 모드 DomParserService 로직).

        Args:
            modal_info: 모달 감지 정보

        Returns:
            Tuple of (elements list, scroll_info dict)
        """
        combined_selector = ", ".join(INTERACTIVE_SELECTORS)

        js_code = """
        (config) => {
            const { selector, attributes, maxElements, maxTextLength, includeHidden, modalInfo } = config;
            const elements = [];

            // Find modal element if open
            let modalElement = null;
            if (modalInfo && modalInfo.isOpen) {
                const semanticSelectors = [
                    '[role="dialog"]',
                    '[role="alertdialog"]',
                    '[aria-modal="true"]'
                ];

                for (const sel of semanticSelectors) {
                    const el = document.querySelector(sel);
                    if (el) {
                        const style = window.getComputedStyle(el);
                        if (style.display !== 'none' && style.visibility !== 'hidden') {
                            modalElement = el;
                            break;
                        }
                    }
                }

                if (!modalElement) {
                    const classSelectors = [
                        '.modal:not(.hidden)',
                        '.modal-overlay',
                        'div[class*="modal"][class*="open"]',
                        'div[class*="dialog"][class*="open"]'
                    ];

                    for (const sel of classSelectors) {
                        const el = document.querySelector(sel);
                        if (el) {
                            const style = window.getComputedStyle(el);
                            if (style.display !== 'none' && style.visibility !== 'hidden') {
                                modalElement = el;
                                break;
                            }
                        }
                    }
                }
            }

            // Viewport dimensions
            const viewW = window.innerWidth;
            const viewH = window.innerHeight;

            // Helper: Position label (9-grid)
            const getPositionLabel = (rect) => {
                const centerX = rect.x + rect.width / 2;
                const centerY = rect.y + rect.height / 2;
                let posLabel = '';

                if (centerY < viewH / 3) posLabel += 'top-';
                else if (centerY > viewH * 2 / 3) posLabel += 'bottom-';
                else posLabel += 'center-';

                if (centerX < viewW / 3) posLabel += 'left';
                else if (centerX > viewW * 2 / 3) posLabel += 'right';
                else posLabel += 'center';

                return posLabel;
            };

            // Helper: Simplify color
            const simplifyColor = (rgbStr) => {
                if (!rgbStr || rgbStr === 'rgba(0, 0, 0, 0)' || rgbStr === 'transparent') return null;
                const match = rgbStr.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/);
                if (!match) return rgbStr;

                const r = parseInt(match[1]);
                const g = parseInt(match[2]);
                const b = parseInt(match[3]);

                if (r > 200 && g < 80 && b < 80) return 'red';
                if (r < 80 && g > 200 && b < 80) return 'green';
                if (r < 80 && g < 80 && b > 200) return 'blue';
                if (r > 200 && g > 200 && b < 80) return 'yellow';
                if (r > 200 && g > 200 && b > 200) return 'white';
                if (r < 50 && g < 50 && b < 50) return 'black';
                if (Math.abs(r - g) < 20 && Math.abs(g - b) < 20 && r > 50 && r < 200) return 'gray';

                return `rgb(${r},${g},${b})`;
            };

            // Query all matching elements
            const nodes = document.querySelectorAll(selector);

            for (const node of nodes) {
                if (elements.length >= maxElements) break;

                // Skip only truly hidden elements (display:none, visibility:hidden)
                // Removed checkVisibility() - it's too strict and excludes clickable elements
                // that are clipped by overflow:hidden (e.g., calendar items in applyhome.co.kr)
                if (!includeHidden) {
                    const style = window.getComputedStyle(node);
                    if (style.display === 'none' || style.visibility === 'hidden') {
                        continue;
                    }
                }

                const rect = node.getBoundingClientRect();
                const tag = node.tagName.toLowerCase();

                // Size check
                const isFormElement = ['input', 'select', 'option', 'textarea', 'button'].includes(tag);
                const hasInteractiveRole = node.getAttribute('role') && ['button', 'link', 'menuitem', 'tab'].includes(node.getAttribute('role'));
                const hasText = node.textContent?.trim().length > 0;
                const hasClickHandler = node.hasAttribute('onclick') || node.hasAttribute('data-testid');

                if (rect.width === 0 && rect.height === 0) {
                    // Keep elements that are interactive or have text content
                    if (!isFormElement && !hasInteractiveRole && !hasClickHandler && !hasText) {
                        continue;
                    }
                }

                // Viewport position
                const viewportHeight = window.innerHeight;
                const viewportWidth = window.innerWidth;

                let outOfView = null;
                if (rect.top > viewportHeight) {
                    outOfView = 'below';
                } else if (rect.bottom < 0) {
                    outOfView = 'above';
                } else if (rect.left > viewportWidth) {
                    outOfView = 'right';
                } else if (rect.right < 0) {
                    outOfView = 'left';
                }

                // Skip elements very far outside viewport
                if (!includeHidden) {
                    const viewportBuffer = viewportHeight * 5;
                    if (rect.bottom < -viewportBuffer || rect.top > viewportHeight + viewportBuffer) continue;
                    if (rect.right < -viewportWidth * 2 || rect.left > viewportWidth * 3) continue;
                }

                // Modal context
                let isInModal = false;
                let isBlocked = false;
                if (modalElement) {
                    isInModal = modalElement.contains(node);
                    isBlocked = !isInModal;
                }

                // Extract attributes
                const attrs = {};
                for (const attr of attributes) {
                    const value = node.getAttribute(attr);
                    if (value) {
                        attrs[attr] = value;
                    }
                }

                // Get text content
                let text = '';
                if (node.textContent) {
                    text = node.textContent.trim().substring(0, maxTextLength);
                    text = text.replace(/\\s+/g, ' ');
                }

                // For empty-text elements
                if (!text || text.length === 0) {
                    const ariaLabel = node.getAttribute('aria-label');
                    const title = node.getAttribute('title');
                    const role = node.getAttribute('role');

                    const descriptions = [];
                    if (ariaLabel) descriptions.push(`aria: ${ariaLabel}`);
                    if (title) descriptions.push(`title: ${title}`);
                    if (role) descriptions.push(`role: ${role}`);

                    const hasSvg = node.querySelector('svg');
                    const hasImg = node.querySelector('img');
                    const classStr = typeof node.className === 'string' ? node.className : (node.className?.baseVal || '');
                    const hasIcon = node.querySelector('[class*="icon"]') || classStr.includes('icon');

                    if (hasSvg) descriptions.push('SVG icon');
                    if (hasImg) descriptions.push('image icon');
                    if (hasIcon && descriptions.length === 0) descriptions.push('icon button');

                    if (descriptions.length > 0) {
                        text = `[${descriptions.join(', ')}]`;
                    }
                }

                // Dynamic state extraction
                if (tag === 'select') {
                    if (node.selectedIndex >= 0 && node.options[node.selectedIndex]) {
                        const selectedOption = node.options[node.selectedIndex];
                        attrs['_selected-value'] = selectedOption.value;
                        attrs['_selected-text'] = selectedOption.text;
                    }
                }

                if (tag === 'input' || tag === 'textarea') {
                    if (node.value) {
                        attrs['_value'] = node.value.substring(0, maxTextLength);
                    }
                    if (node.type === 'checkbox' || node.type === 'radio') {
                        attrs['_checked'] = node.checked ? 'true' : 'false';
                    }
                    if (node.validity && !node.validity.valid) {
                        attrs['_invalid'] = 'true';
                    }
                }

                if (tag === 'details') {
                    attrs['_open'] = node.open ? 'true' : 'false';
                }

                if (tag === 'dialog') {
                    attrs['_open'] = node.open ? 'true' : 'false';
                }

                if (node.disabled) attrs['_disabled'] = 'true';
                if (node.readOnly) attrs['_readonly'] = 'true';
                if (document.activeElement === node) attrs['_focused'] = 'true';

                // Out of viewport indicator
                if (outOfView) {
                    attrs['_outOfView'] = outOfView;
                }

                // Position label
                attrs['_pos'] = getPositionLabel(rect);

                // Bounding box
                if (rect.width > 0 && rect.height > 0) {
                    attrs['_bbox'] = JSON.stringify([
                        Math.round(rect.x),
                        Math.round(rect.y),
                        Math.round(rect.width),
                        Math.round(rect.height)
                    ]);
                }

                // Color info
                const style = window.getComputedStyle(node);
                const bgColor = simplifyColor(style.backgroundColor);
                const textColor = simplifyColor(style.color);
                if (bgColor) attrs['_bg'] = bgColor;
                if (textColor) attrs['_fg'] = textColor;

                elements.push({
                    tag: tag,
                    attributes: attrs,
                    text: text,
                    rect: {
                        x: rect.x,
                        y: rect.y,
                        width: rect.width,
                        height: rect.height
                    },
                    isInModal: isInModal,
                    isBlocked: isBlocked,
                    index: elements.length
                });
            }

            // Scroll info
            const scrollHeight = document.documentElement.scrollHeight;
            const scrollTop = window.scrollY || document.documentElement.scrollTop;
            const viewportH = window.innerHeight;

            const inView = elements.filter(e => !e.attributes._outOfView);
            const belowView = elements.filter(e => e.attributes._outOfView === 'below');
            const aboveView = elements.filter(e => e.attributes._outOfView === 'above');

            const scrollInfo = {
                scrollTop: scrollTop,
                scrollHeight: scrollHeight,
                viewportHeight: viewportH,
                hasMoreAbove: scrollTop > 10,
                hasMoreBelow: (scrollTop + viewportH) < (scrollHeight - 10),
                scrollPercent: Math.round((scrollTop / Math.max(1, scrollHeight - viewportH)) * 100),
                elementsInView: inView.length,
                elementsBelowView: belowView.length,
                elementsAboveView: aboveView.length,
            };

            return { elements, scrollInfo };
        }
        """

        try:
            config = {
                "selector": combined_selector,
                "attributes": ATTRIBUTES_TO_EXTRACT,
                "maxElements": self._max_elements,
                "maxTextLength": self._max_text_length,
                "includeHidden": self._include_hidden,
                "modalInfo": modal_info,
            }

            result = await self._page.evaluate(js_code, config)

            elements = result.get("elements", [])
            scroll_info = result.get("scrollInfo", {})

            return elements, scroll_info

        except Exception as e:
            logger.error("element_extraction_failed", error=str(e))
            return [], {}

    async def _extract_raw_html(self, max_length: int = 30000) -> str:
        """Clean raw HTML 추출 (fallback용).

        Args:
            max_length: 최대 HTML 길이

        Returns:
            정리된 HTML 문자열
        """
        js_code = """
        (maxLength) => {
            const clone = document.documentElement.cloneNode(true);

            // Remove unwanted elements
            const removeSelectors = ['script', 'style', 'noscript', 'link[rel="stylesheet"]', 'meta', 'head'];
            removeSelectors.forEach(sel => {
                clone.querySelectorAll(sel).forEach(el => el.remove());
            });

            // Remove non-interactive SVGs
            clone.querySelectorAll('svg').forEach(svg => {
                const hasInteractive = svg.hasAttribute('onclick') ||
                                      svg.hasAttribute('role') ||
                                      svg.closest('[onclick]') ||
                                      svg.closest('button') ||
                                      svg.closest('a');

                if (!hasInteractive) {
                    svg.remove();
                }
            });

            // Remove comments
            const walker = document.createTreeWalker(clone, NodeFilter.SHOW_COMMENT, null, false);
            const comments = [];
            while (walker.nextNode()) {
                comments.push(walker.currentNode);
            }
            comments.forEach(c => c.remove());

            // Get HTML and clean up
            let html = clone.outerHTML;
            html = html.replace(/\\n\\s*\\n/g, '\\n');
            html = html.replace(/\\t/g, ' ');
            html = html.replace(/  +/g, ' ');
            html = html.replace(/> +</g, '><');

            if (html.length > maxLength) {
                html = html.substring(0, maxLength) + '\\n<!-- ... truncated -->';
            }

            return html;
        }
        """
        try:
            return await self._page.evaluate(js_code, max_length)
        except Exception as e:
            logger.warning("raw_html_extraction_failed", error=str(e))
            return ""

    async def extract_element(self, selector: str) -> dict[str, Any] | None:
        """특정 요소의 DOM 추출.

        Args:
            selector: CSS 선택자

        Returns:
            요소 정보 또는 None
        """
        element = await self._page.query_selector(selector)
        if not element:
            logger.debug("element_not_found", selector=selector)
            return None

        outer_html = await element.evaluate("el => el.outerHTML")
        inner_text = await element.inner_text()
        bounding_box = await element.bounding_box()

        return {
            "selector": selector,
            "outer_html": outer_html,
            "inner_text": inner_text,
            "bounding_box": bounding_box,
        }

    async def extract_interactive_elements(self) -> list[dict[str, Any]]:
        """상호작용 가능한 요소들 추출.

        Returns:
            상호작용 가능한 요소 목록
        """
        # extract()의 elements를 그대로 반환
        dom_data = await self.extract()
        return dom_data.get("elements", [])
