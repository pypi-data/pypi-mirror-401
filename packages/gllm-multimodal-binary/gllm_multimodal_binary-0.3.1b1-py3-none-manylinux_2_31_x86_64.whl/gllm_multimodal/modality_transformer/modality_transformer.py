"""Base any modality transformer.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    None
"""

from abc import ABC, abstractmethod
from typing import Any

from gllm_core.schema import Component


class BaseModalityTransformer(Component, ABC):
    """An abstract base class for the modality transformers used in Gen AI applications.

    Using the implementations of this class, users can transform a any source into a specific string/bytes.
    Each modality transformer comes with a default extractor function that extracts the source.
    Users can also supply their own extractor function to customize the extraction process.
    """

    async def _run(self, **kwargs: Any) -> str | bytes:
        """Executes the query transformation process.

        Args:
            **kwargs (Any): A dictionary of arguments required for the modality transformation. Must include `source`.

        Returns:
            str | bytes: The result of the `transform` method.

        Raises:
            KeyError: If `source` is missing from the input kwargs.
        """
        if "source" not in kwargs:
            raise ValueError("The input kwargs for modality transformer must include a `source` key.")
        return await self.transform(**kwargs)

    @abstractmethod
    async def transform(self, source: bytes | str, query: str | None = None, **kwargs: Any) -> str | bytes:
        """Transforms the given any modality source into a string or bytes.

        This abstract method must be implemented by subclasses to define how the input source is transformed.

        Args:
            source (bytes | str | dict[str, bytes | str]): Any modality source, dict of any modality source
                to be transformed.
            query (str | None): Input query that will be used as additional information for modality transformation.
            kwargs (Any): additional args for transformer.

        Returns:
            str | bytes: A string or bytes of transformed str or bytes source(s).

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError
