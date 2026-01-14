"""This module provides a preset configuration for generating video captions.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    NONE
"""

import os
from typing import Any

from gllm_inference.builder import build_lm_invoker
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker
from gllm_inference.output_parser import JSONOutputParser
from gllm_inference.output_parser.output_parser import BaseOutputParser
from gllm_inference.prompt_builder import PromptBuilder

DEFAULT_SYSTEM_PROMPT = """
<INSTRUCTIONS>
You are a chatbot that analyzes short videos and generates captions based on the video frames and speech.
Your task is to:

- Break the video into coherent **event segments**.
- Produce a short **video summary** in {language} describing the overall video content.
- For each event segment, produce {number_of_captions} captions in {language} (each caption describes a specific sub-moment within that segment).
- For each caption also include a **keyframes** entry containing the `keyframe` that points to the time of the representative frame for that caption. The caption metadata for single range time can contains multiple keyframes, and you must specify all of it.

The video may contain several events. Each event can include multiple actions, scenes, people, or objects. Use both the speech content and the visual context to create accurate and descriptive captions. Speech content should be rewritten into natural, fluent {language} and blended into the description of the scene.

Describe what happens in each event segment in **narrative style** and **third-person point of view**. Mention what is visible on screen, such as actions, appearance, clothing, objects, and environment. If someone speaks but is not visible, describe it as narration or background voice.

Ensure each event segment is distinct and covers a continuous action or topic. **Do not** create events or captions beyond what is shown or heard. **Do not** include conclusions or summaries at the end.

<OUTPUT_FORMAT>
```json
{{
  "video_summary": "Ringkasan singkat video",
  "segments": [
    {{
      "start_time": 0.0,
      "end_time": 10.0,
      "transcripts": [
        {{
          "text": "string (Full text of the spoken dialogue during the segment.)",
          "start_time": 1.0,
          "end_time": 3.0,
          "lang_id": "id"
        }},
        {{
          "text": "string (Full text of the spoken dialogue during the segment.)",
          "start_time": 5.0,
          "end_time": 8.0,
          "lang_id": "id"
        }}
       ],
      "keyframes": [
        {{
          "caption": "keyframe caption",
          "time_offset": 5.2
        }},
        {{
          "caption": "keyframe caption",
          "time_offset": 7.6
        }}
      ]
    }},
    {{
      "start_time": 11.0,
      "end_time": 15.0,
      "transcripts": [...],
      "keyframes": [
        {{
          "caption": "keyframe caption",
          "time_offset": 7.6
        }}
      ]
    }}
  ]
}}
</OUTPUT_FORMAT>
</INSTRUCTIONS>
"""  # noqa: E501

DEFAULT_USER_PROMPT = """
<INPUT_STRUCTURE>
Title: {image_one_liner}
Content: {image_description}
Main Video Filename: {filename}
Metadata: {image_metadata}
Injected Domain Knowledge: {domain_knowledge}
</INPUT_STRUCTURE>
"""


def create_default_prompt_builder(**kwargs: Any) -> PromptBuilder:
    """Create a default prompt builder with templates for generating video captions.

    This function creates and returns a PromptBuilder instance configured with
    default templates for video captioning tasks. The templates are structured to:

    System prompt:
    1. Instructs the model to generate the specified number of captions.
    2. Specifies output format as a JSON list of captions.

    User prompt:
    1. Provides structured input format with fields for:
        1. Video one-liner
        2. Video description
        3. Domain knowledge (will be generated from the video given)
        4. Filename (will be generated from the video given)
        5. Video metadata (will be generated from the video given)

    Returns:
        PromptBuilder: A prompt builder instance configured with default
            templates for video captioning.
    """
    system_prompt = DEFAULT_SYSTEM_PROMPT
    user_prompt = DEFAULT_USER_PROMPT

    return PromptBuilder(system_template=system_prompt, user_template=user_prompt, **kwargs)


def get_preset_video_to_caption(
    preset_name: str,
    lm_invoker_kwargs: dict | None = None,
    prompt_builder_kwargs: dict | None = None,
) -> tuple[BaseLMInvoker, PromptBuilder, BaseOutputParser]:
    """Get the preset configuration for generating video captions.

    Args:
        preset_name (str): The name of the preset to get.
        lm_invoker_kwargs: dict | None: Additional arguments for lm invoker.
        prompt_builder_kwargs: dict | None: Additional arguments for prompt builder.

    Returns:
        tuple[BaseLMInvoker, PromptBuilder, BaseOutputParser]: A tuple containing the preset
            configuration for video captioning.
    """
    lm_invoker_kwargs = lm_invoker_kwargs or {}
    prompt_builder_kwargs = prompt_builder_kwargs or {}

    model_id = os.getenv("DEFAULT_VIDEO_CAPTIONING_MODEL_ID", "google/gemini-2.5-flash")
    lm_invoker_kwargs["model_id"] = lm_invoker_kwargs.get("model_id", model_id)

    if preset_name == "default":
        return (
            build_lm_invoker(**lm_invoker_kwargs),
            create_default_prompt_builder(**prompt_builder_kwargs),
            JSONOutputParser(),
        )

    raise ValueError(f"Invalid preset name: {preset_name}")
