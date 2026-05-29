"""系统级非业务常量边界。

本包只允许放置跨模块通用、与业务规则无关的系统级常量。

允许示例：DEFAULT_PAGE_SIZE、TIME_FORMAT、MAX_UPLOAD_SIZE、SYSTEM_NAME、请求超时、编码格式。
禁止内容：业务枚举、事实类型、字段规则、风险等级、业务关键词、治理规则。

全局标准治理规则统一归口到 standard_governance，业务模块只消费规则，不重复定义。
"""
