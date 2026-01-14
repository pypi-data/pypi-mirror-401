"""
File Access Skill - File path and data URI access capability.

This skill provides the ability to retrieve file paths and convert files
to data URIs for embedding in HTML/PDF documents.
It wraps the GetFilePathTool and GetFileAsDataURITool with detailed instructions.
"""

from ..base import Skill, SkillMetadata, SkillCategory
from ...tools import GetFilePathTool, GetFileAsDataURITool


FILE_ACCESS_INSTRUCTIONS = """
## File Access Instructions

You can retrieve file paths and convert stored files to data URIs for embedding
in HTML, PDF, or other documents.

### Available Tools

1. **get_file_path** - Get an accessible path or data URI for a stored file
2. **get_file_as_data_uri** - Convert any stored file to a base64 data URI

### Get File Path Tool

Use `get_file_path` to get an accessible reference to a stored file.

**Behavior by storage backend:**
- **Local storage**: Returns an absolute file path with `file://` protocol
- **S3/MinIO**: Returns a base64 data URI

**Parameters:**
- `file_id` (required): The file ID returned from file storage operations

**Returns:**
- For local: `file:///absolute/path/to/file.png`
- For S3/MinIO: `data:image/png;base64,<encoded_content>`

**Example Usage:**
```python
# Get path for a chart image
path = await get_file_path("chart_abc123")
# Use in HTML: <img src="{path}">
```

### Get File As Data URI Tool

Use `get_file_as_data_uri` to always get a data URI regardless of storage backend.

**Parameters:**
- `file_id` (required): The file ID returned from file storage operations

**Returns:**
- Data URI string: `data:mime/type;base64,<encoded_content>`

**Example Usage:**
```python
# Convert image to data URI
data_uri = await get_file_as_data_uri("image_xyz789")
# Embed in HTML: <img src="{data_uri}">
```

### Common Use Cases

#### 1. Embedding Images in HTML

```html
<!-- Using file path (local storage) -->
<img src="file:///path/to/image.png" alt="Chart">

<!-- Using data URI (works everywhere) -->
<img src="data:image/png;base64,iVBORw0KGgo..." alt="Chart">
```

#### 2. Creating PDFs with Images

When generating PDFs that include stored images:
1. Create the image (chart, diagram, etc.) and get the file_id
2. Use `get_file_path` or `get_file_as_data_uri` to get a reference
3. Include the reference in your HTML/Markdown for PDF generation

```python
# Step 1: Create chart and get file_id
chart_file_id = await save_chart_as_image(chart_config, "sales_chart")

# Step 2: Get accessible path
image_path = await get_file_path(chart_file_id)

# Step 3: Use in HTML for PDF
html = f'''
<h1>Sales Report</h1>
<img src="{image_path}" alt="Sales Chart">
'''
```

#### 3. Embedding Multiple Images

```python
# Get paths for multiple images
chart_path = await get_file_path(chart_id)
diagram_path = await get_file_path(diagram_id)
logo_path = await get_file_as_data_uri(logo_id)  # Always use data URI for logos

html = f'''
<img src="{logo_path}" class="logo">
<img src="{chart_path}" class="chart">
<img src="{diagram_path}" class="diagram">
'''
```

### When to Use Each Tool

| Scenario | Recommended Tool |
|----------|------------------|
| Local development | `get_file_path` |
| Production (S3/MinIO) | Either (both return data URI) |
| Guaranteed portability | `get_file_as_data_uri` |
| Large files | `get_file_path` (smaller response) |
| Email/external sharing | `get_file_as_data_uri` |

### Best Practices

1. **Use data URIs for portability**: Data URIs work regardless of storage backend
2. **Check file existence**: Handle cases where file_id may be invalid
3. **Consider file size**: Large files create large data URIs
4. **Cache paths**: If using the same file multiple times, cache the path/URI
5. **Verify MIME types**: Ensure the MIME type matches the expected format

### Error Handling

Common errors:
- "File with ID 'xxx' not found" → Invalid file_id
- "File exists in metadata but not on disk" → File was deleted
- "Failed to get file path" → Storage access error

### Limitations

- Data URIs increase document size (base64 encoding adds ~33%)
- Very large files may cause memory issues when converted to data URI
- File paths only work on the same machine (not portable)
- Some email clients have data URI size limits
"""


def create_file_access_skill() -> Skill:
    """
    Create the file access skill.

    Returns:
        Skill instance for file path and data URI access
    """
    return Skill(
        metadata=SkillMetadata(
            name="file_access",
            description="Get file paths and data URIs for embedding files in documents",
            trigger_patterns=[
                "file path",
                "data uri",
                "file access",
                "embed file",
                "file url",
                "base64",
                "embed image",
                "image path",
                "file reference",
            ],
            category=SkillCategory.DOCUMENT,
            version="1.0.0",
        ),
        instructions=FILE_ACCESS_INSTRUCTIONS,
        tools=[GetFilePathTool(), GetFileAsDataURITool()],
        dependencies=[],
        config={},
    )


__all__ = ["create_file_access_skill", "FILE_ACCESS_INSTRUCTIONS"]
