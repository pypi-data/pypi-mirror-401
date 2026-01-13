"""
Code generation utilities for Assembly API Client.
"""
import keyword
import re
from pathlib import Path

from ..parser import APISpec, load_service_map


def sanitize_name(name: str) -> str:
    """Sanitize a string to be a valid Python identifier."""
    # Remove invalid characters
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    # Ensure it doesn't start with a number
    if name[0].isdigit():
        name = f"_{name}"
    # Check for keywords
    if keyword.iskeyword(name):
        name = f"{name}_"
    return name


def generate_services_enum(cache_dir: Path) -> str:
    """Generate the Service enum code."""
    service_map = load_service_map(cache_dir)

    lines = [
        "from enum import StrEnum",
        "",
        "class Service(StrEnum):",
        '    """Enumeration of all available Assembly API Services."""',
    ]

    # Sort by name for stability
    # We need to create valid enum member names from the service names
    # e.g. "국회의원발의법률안" -> "BILL_INFO"? No, that's hard to automate perfectly.
    # Maybe we just use the Service ID as the value, and try to make a readable key?
    # Or just use the ID as the key if we can't make a good name?
    # User wants "readable".
    # Let's try to transliterate or just use the Korean name if Python 3 supports unicode identifiers (it does!)
    # But usually English is preferred.
    # Since we don't have English names, maybe we can use the Korean name as the key?
    # Python 3 allows unicode variable names.
    # Class attributes can be unicode.

    # Let's try to make English-like keys if possible, or just use the Korean name sanitized?
    # "국회의원발의법률안" -> valid python identifier? Yes.

    for service_id, name in sorted(service_map.items(), key=lambda x: x[1]):
        # Sanitize name for Python identifier
        # Remove spaces, special chars
        safe_name = re.sub(r"[^a-zA-Z0-9가-힣]", "_", name)
                # Remove leading/trailing underscores and collapse multiple underscores
                safe_name = re.sub(r"_+", "_", safe_name).strip("_")
        
                # If it starts with digit, prefix with S to avoid starting with underscore (private)
                if safe_name and safe_name[0].isdigit():
                    safe_name = f"S{safe_name}"
        
                if not safe_name:
                    safe_name = f"Service_{service_id}"
        
                lines.append(f'    {safe_name} = "{service_id}"')
    return "\n".join(lines)


def generate_model_code(spec: APISpec) -> str:
    """Generate Pydantic model code for a single spec."""
    class_name = f"Model_{spec.service_id}"

    lines = [
        f"class {class_name}(BaseModel):",
        f'    """Response model for {spec.service_id}"""',
    ]

    if not spec.response_fields:
        lines.append("    pass")
        return "\n".join(lines)

    for field in spec.response_fields:
        field_name = sanitize_name(field.name)
        # Determine type (default to Union[str, int, float, None] for safety)
        # API often returns numbers as strings or vice versa, so we must be lenient.
        py_type = "Union[str, int, float, None]"

        lines.append(
            f'    {field_name}: {py_type} = Field(None, description="{field.description}", alias="{field.name}")'
        )

    return "\n".join(lines)


def generate_params_model_code(spec: APISpec) -> str:
    """Generate Pydantic model code for request parameters."""
    class_name = f"Params_{spec.service_id}"

    lines = [
        f"class {class_name}(BaseModel):",
        f'    """Request parameters for {spec.service_id}"""',
    ]

    if not spec.request_params:
        lines.append("    pass")
        return "\n".join(lines)

    for param in spec.request_params:
        field_name = sanitize_name(param.name)

        # Determine type
        # Most params are strings in this API, even numbers are often passed as strings
        # But we can try to be smarter if needed. For now, str is safest.
        py_type = "str"

        default_val = "..." if param.required else "None"
        if not param.required:
            py_type += " | None"

        lines.append(
            f"    {field_name}: {py_type} = Field({default_val}, "
            f'description="{param.description}", alias="{param.name}")'
        )

    return "\n".join(lines)
