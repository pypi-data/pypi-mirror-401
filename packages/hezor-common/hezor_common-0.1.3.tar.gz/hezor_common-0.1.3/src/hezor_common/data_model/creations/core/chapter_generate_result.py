"""Chapter generation result model."""

from pydantic import BaseModel, ConfigDict, Field

from hezor_common.data_model.creations.core.chapter_model import ChapterModel
from hezor_common.data_model.creations.core.section_generate_result import (
    SectionGenerateResult,
)


class ChapterGenerateResult(BaseModel):
    """Chapter generation result.

    Attributes
    ----------
    chapter : ChapterModel
        解析的 chapter 模型对象
    section_results : list[SectionGenerateResult]
        所有子 section 的生成结果列表
    summary : str
        生成的章节摘要内容
    full_content : str
        完整的 chapter 内容，格式：## chapter.meta.name\n\nsummary\n\n所有 sections 的 full_content

    Examples
    --------
    >>> result = ChapterGenerateResult(
    ...     chapter=chapter_obj,
    ...     section_results=[section_result1, section_result2],
    ...     summary="本章节分析了单店现金流与投资回报情况...",
    ...     full_content="## 现金流与投资回报分析\n\n本章节分析了...\n\n### 1.1 现金概览\n\n..."
    ... )
    """

    model_config = ConfigDict(frozen=False, extra="forbid")

    chapter: ChapterModel = Field(..., description="解析的 chapter 模型对象")
    section_results: list[SectionGenerateResult] = Field(
        ..., description="所有子 section 的生成结果列表"
    )
    summary: str = Field(..., description="生成的章节摘要内容")
    full_content: str = Field(
        ...,
        description="完整的 chapter 内容，格式：## chapter.meta.name\\n\\nsummary\\n\\n所有 sections 的 full_content",
    )
