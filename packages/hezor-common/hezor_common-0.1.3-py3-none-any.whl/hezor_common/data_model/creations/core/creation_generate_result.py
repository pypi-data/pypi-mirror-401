"""Creation generation result model."""

from pydantic import BaseModel, ConfigDict, Field

from hezor_common.data_model.creations.core.chapter_generate_result import (
    ChapterGenerateResult,
)
from hezor_common.data_model.creations.core.creation_model import CreationModel
from hezor_common.data_model.creations.core.creation_params import CreationParams


class CreationGenerateResult(BaseModel):
    """Creation generation result.

    Attributes
    ----------
    original_query : str
        原始查询字符串
    creation : CreationModel
        解析的 creation 模型对象
    params : CreationParams
        生成参数（subject, period, data_coverage）
    chapter_results : list[ChapterGenerateResult]
        所有子 chapter 的生成结果列表
    summary : str
        生成的作品摘要内容
    title : str
        完整标题，格式：{subject} {creation.meta.name} {period}
    data_coverage : str
        数据周期文本
    full_content : str
        完整的 creation 内容（不含 prefix 和 postfix）
    creation_id : str
        生成的唯一 ID（使用 snowflake）
    prefix : str
        MDX 文件前置内容（frontmatter）
    postfix : str
        MDX 文件后置内容（报告生成信息）
    file_path : str
        保存的文件路径

    Examples
    --------
    >>> result = CreationGenerateResult(
    ...     creation=creation_obj,
    ...     params=params_obj,
    ...     chapter_results=[chapter_result1, chapter_result2],
    ...     summary="本报告深入分析了...",
    ...     title="鮨大山 单店盈利模型 2025 年 12 月",
    ...     data_coverage="202512-202512",
    ...     full_content="# 鮨大山 单店盈利模型 2025 年 12 月\n\n...",
    ...     creation_id="abc123",
    ...     prefix="---\ntitle: ...\n---\n",
    ...     postfix="\n[报告生成日期：2026-01-05]\n",
    ...     file_path="website/src/content/reports/abc123.mdx"
    ... )
    """

    original_query: str = Field(..., description="原始查询字符串")
    model_config = ConfigDict(frozen=False, extra="forbid")

    creation: CreationModel = Field(..., description="解析的 creation 模型对象")
    params: CreationParams = Field(..., description="生成参数")
    chapter_results: list[ChapterGenerateResult] = Field(
        ..., description="所有子 chapter 的生成结果列表"
    )
    summary: str = Field(..., description="生成的作品摘要内容")
    title: str = Field(
        ..., description="完整标题，格式：{subject} {creation.meta.name} {period}"
    )
    data_coverage: str = Field(..., description="数据周期文本")
    full_content: str = Field(
        ..., description="完整的 creation 内容（不含 prefix 和 postfix）"
    )
    creation_id: str = Field(..., description="生成的唯一 ID")
    prefix: str = Field(..., description="MDX 文件前置内容（frontmatter）")
    postfix: str = Field(..., description="MDX 文件后置内容")
    file_path: str = Field(..., description="保存的文件路径")
