"""Schema for image to mermaid operations in Gen AI applications.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    NONE
"""

from pydantic import BaseModel, Field


class Mermaid(BaseModel):
    """Mermaid additional metadata.

    Attributes:
        diagram_type (str): type of the diagram to be generated.
        context (str): additional context to generate mermaid.
    """

    diagram_type: str | None = Field(default=None)
    context: str | None = Field(default=None)
