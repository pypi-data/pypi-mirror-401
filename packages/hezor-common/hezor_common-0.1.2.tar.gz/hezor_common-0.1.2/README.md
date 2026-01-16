# Hezor Common

Common utilities and data models for Hezor projects.

## Features

- **Data Models for Creations**: Pydantic-based models for structured content creation
  - Creation models: Top-level model with metadata, authors, and contributors
  - Chapter models: Chapter structure with metadata, summary, and sections
  - Section models: Section structure with data queries, chart suggestions, and analysis guidelines
  - Result models: Generation results for creations, chapters, and sections

## Installation

```bash
pip install hezor-common
```

## Usage

### Data Models

```python
from hezor_common.data_model import (
    CreationModel,
    CreationMeta,
    Author,
    ChapterModel,
    SectionModel,
)

# Create a creation model
author = Author(name="John Doe", avatar="https://example.com/avatar.jpg")
meta = CreationMeta(
    name="Single Store Profit Model",
    description="A comprehensive profit analysis model",
    author=author,
    path="food_beverage/single_store_profit_model",
    domain="food_beverage",
    slug="single_store_profit_model"
)

creation = CreationModel(
    meta=meta,
    summary=None,
    chapters=[]
)
```

## API Reference

All models are exported from `hezor_common.data_model`:

- **Creation**: `CreationModel`, `CreationMeta`, `CreationSummary`, `Author`, `Contributor`
- **Chapter**: `ChapterModel`, `ChapterMeta`, `ChapterSummary`
- **Section**: `SectionModel`, `TitleGuideline`, `DataQuery`, `Dataset`, `ChartSuggestion`, `AnalysisGuideline`
- **Results**: `SectionGenerateResult`, `ChapterGenerateResult`

## Requirements

- Python >= 3.11
- pydantic >= 2.0.0

## License

MIT License - see LICENSE file for details.

