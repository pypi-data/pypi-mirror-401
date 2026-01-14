"""Defines a convenience function to build a modality converter.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    NONE
"""

from __future__ import annotations

from typing import Type

from gllm_multimodal.constants import Modality, ModalityConverterApproach, ModalityConverterTask
from gllm_multimodal.modality_converter.image_to_text.image_to_caption import (
    LMBasedImageToCaption,
)
from gllm_multimodal.modality_converter.image_to_text.image_to_mermaid import (
    LMBasedImageToMermaid,
)
from gllm_multimodal.modality_converter.modality_converter import BaseModalityConverter

ConverterKey = tuple[Modality, Modality, ModalityConverterTask, ModalityConverterApproach | None]

ConverterClass = Type[BaseModalityConverter]

MODALITY_CONVERTER_REGISTRY: dict = {
    Modality.IMAGE: {
        Modality.TEXT: {
            ModalityConverterTask.CAPTIONING: {ModalityConverterApproach.LM_BASED: LMBasedImageToCaption},
            ModalityConverterTask.MERMAID: {ModalityConverterApproach.LM_BASED: LMBasedImageToMermaid},
            ModalityConverterTask.AUTO: {None: LMBasedImageToCaption},
        }
    },
}


def build_modality_converter(
    source_modality: Modality,
    target_modality: Modality,
    task_type: ModalityConverterTask = ModalityConverterTask.AUTO,
    approach_type: ModalityConverterApproach | None = None,
    preset: str | None = None,
    **kwargs,
) -> BaseModalityConverter:
    """Build and initialize a modality converter instance for a given configuration.

    The factory looks up the converter class based on the combination of:
        - source_modality: input modality (e.g., Modality.IMAGE, Modality.AUDIO)
        - target_modality: output modality (e.g., Modality.TEXT)
        - task_type: conversion task (e.g., CAPTIONING, TRANSCRIPT, MERMAID, or AUTO)
        - approach_type: the converter's algorithmic approach; required for non-AUTO tasks, must be None for AUTO

    All supported combinations must be registered in MODALITY_CONVERTER_REGISTRY.

    Args:
        source_modality (Modality): The source modality.
        target_modality (Modality): The output modality.
        task_type (ModalityConverterTask, optional): The conversion task. Defaults to ModalityConverterTask.AUTO.
        approach_type (ModalityConverterApproach | None, optional): The approach for the conversion.
            Required for non-AUTO tasks; must be None for task_type=AUTO.
        preset (str | None, optional): Preset identifier for the converter's .from_preset() method.
            If None, uses the default preset for the class.
        **kwargs: Additional keyword arguments passed to .from_preset().

    Returns:
        BaseModalityConverter: An instance of the matching converter class.

    Raises:
        ValueError: If the configuration is invalid or not registered, including:
            - (source_modality, target_modality, task_type, approach) not registered
            - approach_type missing for non-AUTO task_type
            - approach_type provided when task_type is AUTO
            - Any dimension unsupported for the given combination
    """
    if source_modality not in MODALITY_CONVERTER_REGISTRY:
        raise ValueError(
            f"Unsupported source modality: {source_modality}. Supported: {list(MODALITY_CONVERTER_REGISTRY.keys())}"
        )

    target_map: dict = MODALITY_CONVERTER_REGISTRY[source_modality]
    if target_modality not in target_map:
        raise ValueError(
            f"Cannot convert {source_modality} → {target_modality}. Supported targets: {list(target_map.keys())}"
        )

    task_map: dict[str, dict] = target_map[target_modality]
    if task_type not in task_map:
        raise ValueError(
            f"Unsupported task '{task_type}' for {source_modality} → {target_modality}. "
            f"Available: {list(task_map.keys())}"
        )

    if task_type == ModalityConverterTask.AUTO:
        if approach_type is not None:
            raise ValueError(
                "Cannot specify 'approach_type' when task_type is AUTO. Use a specific task or omit approach_type."
            )
        converter_class = task_map[task_type][None]
    else:
        if approach_type is None:
            raise ValueError(
                f"Must specify 'approach_type' for task '{task_type}'. "
                f"Available: {list(task_map[task_type].keys())}"
            )

        approach_map = task_map[task_type]
        if approach_type not in approach_map:
            raise ValueError(
                f"Unsupported approach '{approach_type}' for task '{task_type}'. "
                f"Available: {list(approach_map.keys())}"
            )
        converter_class = approach_map[approach_type]

    return converter_class.from_preset(preset, **kwargs)
