"""标准治理只读约束层：来源类型枚举。"""

from enum import Enum


class SourceType(str, Enum):
    """source_type"""
    MANUAL_INPUT = "manual_input"
    UPLOADED_DOCUMENT = "uploaded_document"
    IMAGE_INPUT = "image_input"
    AUDIO_INPUT = "audio_input"
    CHAT_RECORD = "chat_record"
    EXTERNAL_FEEDBACK = "external_feedback"
    SYSTEM_GENERATED = "system_generated"
    AI_ASSISTED = "ai_assisted"
    INTERFACE_CALLBACK = "interface_callback"
    TEMPLATE_OUTPUT = "template_output"
    VIEW_OUTPUT = "view_output"
    MANUAL_CONFIRMATION = "manual_confirmation"
    SYSTEM_VALIDATION = "system_validation"
    FEEDBACK_RETURN = "feedback_return"
    EXTERNAL_COLLABORATION = "external_collaboration"
