"""Section generation result model."""

from pydantic import BaseModel, ConfigDict, Field

from hezor_common.data_model.creations.core.section_model import SectionModel


class SectionGenerateResult(BaseModel):
    """Section generation result.

    Attributes
    ----------
    section : SectionModel
        解析的 section 模型对象
    data : dict[str, object]
        查询获取的数据字典
    charts : str
        生成的图表内容（Markdown 表格或 ECharts 配置）
    analysis : str
        生成的分析内容（Markdown 格式）
    title : str
        生成的标题
    full_content : str
        完整的 section 内容，格式：### serial. title\n\ncharts\n\nanalysis

    Examples
    --------
    >>> result = SectionGenerateResult(
    ...     section=section_obj,
    ...     data={"revenue": 1000},
    ...     charts="```echarts\n{...}\n```",
    ...     analysis="## 分析\n本季度收入增长显著...",
    ...     title="收入分析",
    ...     full_content="### 1.1 收入分析\n\n```echarts\n{...}\n```\n\n## 分析\n..."
    ... )
    """

    model_config = ConfigDict(frozen=False, extra="forbid")

    section: SectionModel = Field(..., description="解析的 section 模型对象")
    data: dict[str, object] = Field(..., description="查询获取的数据字典")
    charts: str = Field(
        ..., description="生成的图表内容（Markdown 表格或 ECharts 配置）"
    )
    analysis: str = Field(..., description="生成的分析内容（Markdown 格式）")
    title: str = Field(..., description="生成的标题")
    full_content: str = Field(
        ...,
        description="完整的 section 内容，格式：### serial. title\\n\\ncharts\\n\\nanalysis",
    )
