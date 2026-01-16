"""Data models for chapter XML structure."""

from typing import Optional
from pydantic import BaseModel, Field

from hezor_common.data_model.creations.core.section_model import SectionModel


class ChapterMeta(BaseModel):
    """Chapter metadata.

    目录命名约定: [serial]__[slug]/
    例如: 1__cash_and_investment/
    - serial: 1 (用于排序)
    - slug: cash_and_investment (目录标识名)
    - name: 现金流与投资回报分析 (来自 meta.xml)
    """

    name: str = Field(..., description="章节名称(来自 meta.xml)")
    serial: Optional[str] = Field(
        default=None, description="章节序号，如 '1'(从目录名解析)"
    )
    slug: Optional[str] = Field(
        default=None, description="目录标识名，如 'cash_and_investment'(从目录名解析)"
    )


class ChapterSummary(BaseModel):
    """Chapter summary content."""

    content: Optional[str] = Field(default=None, description="章节总结内容")


class ChapterModel(BaseModel):
    """Chapter data model representing a directory with meta, summary, and multiple sections."""

    meta: ChapterMeta = Field(..., description="章节元数据")
    summary: Optional[ChapterSummary] = Field(default=None, description="章节总结")
    sections: list[SectionModel] = Field(
        default_factory=list, description="章节下的所有小节"
    )

    def get_section_count(self) -> int:
        """获取章节数量."""
        return len(self.sections)

    def get_section_by_name(self, name: str) -> Optional[SectionModel]:
        """根据名称获取指定小节."""
        for section in self.sections:
            if section.name == name:
                return section
        return None

    def get_all_dataset_names(self) -> list[str]:
        """获取所有小节中的数据集名称."""
        dataset_names = []
        for section in self.sections:
            dataset_names.extend(section.get_dataset_names())
        return dataset_names

    def has_summary(self) -> bool:
        """检查是否有总结内容."""
        return self.summary is not None and self.summary.content is not None

    def get_sorted_sections(self) -> list[SectionModel]:
        """获取按序号排序的小节列表."""
        return sorted(self.sections, key=lambda s: s.serial if s.serial else "")
