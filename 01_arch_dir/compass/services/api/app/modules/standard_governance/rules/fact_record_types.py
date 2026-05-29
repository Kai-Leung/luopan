"""事实记录类型规则表。

只用于 L1 候选分类、S2 字段规则选择和前端展示映射；不生成正式事实。
"""

FACT_RECORD_TYPE_DISPLAY = {
    "construction_record": "施工记录",
    "financial_record": "财务记录",
    "material_flow_record": "材料流转记录",
    "document_record": "资料记录",
    "communication_service_record": "沟通与服务记录",
    "issue_risk_record": "问题与风险记录",
    "decision_change_record": "决策与变更记录",
    "relationship_record": "关系记录",
    "attendance_record": "出勤记录",
    "resume_record": "履历记录",
    "business_maintenance_record": "商务维护记录",
    "acceptance_delivery_record": "验收与交付记录",
    "purchase_record": "采购记录",
    "other_fact_record": "其他事实记录",
}

FACT_RECORD_TYPE_RULES = {
    "construction_record": {
        "description": "记录现场施工、维修、整改、工序进展和施工动作。",
        "keywords": ("施工", "防水", "维修", "整改", "安装", "开工", "完工", "现场", "返工", "工序"),
        "boundaries": "不包含单纯材料采购、付款收款或客户沟通。",
    },
    "financial_record": {
        "description": "记录收款、付款、尾款、结算、费用、金额和财务确认。",
        "keywords": ("收款", "付款", "尾款", "结算", "费用", "金额", "发票", "报价", "预算", "支付"),
        "boundaries": "不包含材料采购动作本身，采购动作归入采购记录或材料流转记录。",
    },
    "material_flow_record": {
        "description": "记录材料入场、出库、领用、退料、库存和现场材料流转。",
        "keywords": ("到货", "入场", "出库", "领用", "退料", "库存", "材料", "水泥", "砂浆", "板材"),
        "boundaries": "只描述购买下单时优先归入采购记录；含到货或领用时归入材料流转记录。",
    },
    "document_record": {
        "description": "记录合同、图纸、签证单、验收单、照片、聊天记录等资料归集。",
        "keywords": ("合同", "图纸", "资料", "文件", "签证单", "照片", "截图", "凭证", "附件", "归档"),
        "boundaries": "资料承载的风险事项仍应优先识别为问题与风险记录。",
    },
    "communication_service_record": {
        "description": "记录客户、甲方、供应商、班组等沟通、服务和跟进过程。",
        "keywords": ("沟通", "回复", "说明", "反馈", "协调", "服务", "跟进", "客户说", "客户说明", "电话", "微信"),
        "boundaries": "出现投诉、风险、延期、质量问题时优先归入问题与风险记录。",
    },
    "issue_risk_record": {
        "description": "记录质量、安全、投诉、延期、赔偿、阻断和风险预警。",
        "keywords": ("风险", "问题", "投诉", "延期", "延误", "赔偿", "质量", "安全", "漏水", "阻断", "预警"),
        "boundaries": "普通沟通不归入本类，必须存在问题、风险或负面后果信号。",
    },
    "decision_change_record": {
        "description": "记录方案决策、范围调整、设计变更、签证变更和口径变更。",
        "keywords": ("决定", "决策", "变更", "调整", "改方案", "改动", "签证", "新增", "取消", "确认方案"),
        "boundaries": "仅执行既定施工动作不归入本类。",
    },
    "relationship_record": {
        "description": "记录客户、供应商、班组、责任主体之间的关系和角色绑定。",
        "keywords": ("关系", "绑定", "联系人", "负责人关系", "责任关系", "归属", "角色", "授权关系"),
        "boundaries": "只出现主体名称但描述施工、财务、采购等事项时按具体事项分类。",
    },
    "attendance_record": {
        "description": "记录人员到场、请假、出勤、考勤和工时。",
        "keywords": ("到场", "出勤", "考勤", "请假", "缺勤", "工时", "上班", "下班", "加班", "人数"),
        "boundaries": "施工动作中提到人员但不描述出勤时不归入本类。",
    },
    "resume_record": {
        "description": "记录人员、项目、供应商或对象的履历、经历、历史表现。",
        "keywords": ("履历", "经历", "历史", "做过", "服务过", "负责过", "过往", "档案", "背景", "资历"),
        "boundaries": "当前发生的施工、沟通、财务等事实不归入履历记录。",
    },
    "business_maintenance_record": {
        "description": "记录商机维护、客户维护、回访、续约、报价跟进和商务动作。",
        "keywords": ("商机", "维护", "回访", "续约", "报价跟进", "商务", "客情", "拜访", "转介绍", "复购"),
        "boundaries": "已经发生的收付款归入财务记录。",
    },
    "acceptance_delivery_record": {
        "description": "记录验收、交付、移交、签收、收尾和交接。",
        "keywords": ("验收", "交付", "移交", "签收", "交接", "收尾", "竣工", "验收单", "交付清单", "移交单"),
        "boundaries": "施工过程进展未到验收交付节点时归入施工记录。",
    },
    "purchase_record": {
        "description": "记录采购下单、购买、订货、询价、供应商采购和采购价格。",
        "keywords": ("采购", "购买", "买了", "下单", "订货", "询价", "供应商报价", "采购价", "采购单", "订购"),
        "boundaries": "材料到货、入库、领用等现场流转归入材料流转记录。",
    },
    "other_fact_record": {
        "description": "无法命中明确分类时的兜底候选类型。",
        "keywords": (),
        "boundaries": "仅当 13 类明确类型均无法命中时使用，不替代明确分类。",
    },
}

FACT_RECORD_TYPE_KEYWORDS = {
    fact_type: tuple(rule["keywords"]) for fact_type, rule in FACT_RECORD_TYPE_RULES.items()
}

FACT_RECORD_TYPE_BOUNDARIES = {
    fact_type: str(rule["boundaries"]) for fact_type, rule in FACT_RECORD_TYPE_RULES.items()
}

FACT_RECORD_TYPE_PRIORITY = (
    "issue_risk_record",
    "acceptance_delivery_record",
    "decision_change_record",
    "purchase_record",
    "material_flow_record",
    "financial_record",
    "attendance_record",
    "document_record",
    "business_maintenance_record",
    "resume_record",
    "relationship_record",
    "communication_service_record",
    "construction_record",
)


def classify_fact_record_type(text: str) -> str:
    for fact_type in FACT_RECORD_TYPE_PRIORITY:
        if _matches_keywords(text, FACT_RECORD_TYPE_KEYWORDS[fact_type]):
            return fact_type
    return "other_fact_record"


def get_fact_record_type_display(fact_record_type: str) -> str:
    return FACT_RECORD_TYPE_DISPLAY.get(fact_record_type, FACT_RECORD_TYPE_DISPLAY["other_fact_record"])


def is_known_fact_record_type(fact_record_type: str) -> bool:
    return fact_record_type in FACT_RECORD_TYPE_RULES


def _matches_keywords(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)
