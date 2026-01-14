"""DOM related models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    """요소의 bounding box."""

    x: float
    y: float
    width: float
    height: float


class InteractiveElement(BaseModel):
    """상호작용 가능한 요소.

    클릭, 입력 등이 가능한 DOM 요소 정보입니다.
    """

    tag: str
    type: str | None = None  # input type
    id: str | None = None
    name: str | None = None
    text: str | None = None
    placeholder: str | None = None
    selector: str
    aria_label: str | None = None
    bounding_box: BoundingBox | None = None
    is_visible: bool = True
    is_enabled: bool = True

    model_config = {"extra": "allow"}


class PageMetadata(BaseModel):
    """페이지 메타데이터."""

    viewport_width: int
    viewport_height: int
    device_pixel_ratio: float = 1.0
    scroll_x: int = 0
    scroll_y: int = 0
    document_width: int | None = None
    document_height: int | None = None


class DomData(BaseModel):
    """추출된 DOM 데이터.

    페이지의 DOM 정보를 담는 모델입니다.
    Runner가 AI 분석을 위해 사용합니다.
    """

    url: str
    title: str
    html: str
    timestamp: str
    viewport: dict[str, int] | None = None
    body_text: str | None = None
    interactive_elements: list[InteractiveElement] = Field(default_factory=list)
    metadata: PageMetadata | None = None

    model_config = {"extra": "allow"}


class Screenshot(BaseModel):
    """스크린샷 데이터."""

    base64: str
    mime_type: str = "image/png"
    width: int | None = None
    height: int | None = None


class DomExtractionResult(BaseModel):
    """DOM 추출 결과.

    DOM 데이터와 스크린샷을 함께 담습니다.
    """

    dom: DomData
    screenshot: Screenshot | None = None
    goal: str | None = None  # 현재 Step의 goal

    model_config = {"extra": "allow"}
