export const FACT_RECORD_TYPE_DISPLAY: Record<string, string> = {
  construction_record: "施工记录",
  financial_record: "财务记录",
  material_flow_record: "材料流转记录",
  document_record: "资料记录",
  communication_service_record: "沟通与服务记录",
  issue_risk_record: "问题与风险记录",
  decision_change_record: "决策与变更记录",
  relationship_record: "关系记录",
  attendance_record: "出勤记录",
  resume_record: "履历记录",
  business_maintenance_record: "商务维护记录",
  acceptance_delivery_record: "验收与交付记录",
  purchase_record: "采购记录",
  other_fact_record: "其他事实记录",
};

export const FACT_RECORD_TYPE_KEYWORDS: Record<string, readonly string[]> = {
  construction_record: ["施工", "防水", "维修", "整改", "安装", "开工", "完工", "现场", "返工", "工序"],
  financial_record: ["收款", "付款", "尾款", "结算", "费用", "金额", "发票", "报价", "预算", "支付"],
  material_flow_record: ["到货", "入场", "出库", "领用", "退料", "库存", "材料", "水泥", "砂浆", "板材"],
  document_record: ["合同", "图纸", "资料", "文件", "签证单", "照片", "截图", "凭证", "附件", "归档"],
  communication_service_record: ["沟通", "回复", "说明", "反馈", "协调", "服务", "跟进", "客户说", "客户说明", "电话", "微信"],
  issue_risk_record: ["风险", "问题", "投诉", "延期", "延误", "赔偿", "质量", "安全", "漏水", "阻断", "预警"],
  decision_change_record: ["决定", "决策", "变更", "调整", "改方案", "改动", "签证", "新增", "取消", "确认方案"],
  relationship_record: ["关系", "绑定", "联系人", "负责人关系", "责任关系", "归属", "角色", "授权关系"],
  attendance_record: ["到场", "出勤", "考勤", "请假", "缺勤", "工时", "上班", "下班", "加班", "人数"],
  resume_record: ["履历", "经历", "历史", "做过", "服务过", "负责过", "过往", "档案", "背景", "资历"],
  business_maintenance_record: ["商机", "维护", "回访", "续约", "报价跟进", "商务", "客情", "拜访", "转介绍", "复购"],
  acceptance_delivery_record: ["验收", "交付", "移交", "签收", "交接", "收尾", "竣工", "验收单", "交付清单", "移交单"],
  purchase_record: ["采购", "购买", "买了", "下单", "订货", "询价", "供应商报价", "采购价", "采购单", "订购"],
  other_fact_record: [],
};

export const FACT_RECORD_TYPE_BOUNDARIES: Record<string, string> = {
  construction_record: "不包含单纯材料采购、付款收款或客户沟通。",
  financial_record: "不包含材料采购动作本身，采购动作归入采购记录或材料流转记录。",
  material_flow_record: "只描述购买下单时优先归入采购记录；含到货或领用时归入材料流转记录。",
  document_record: "资料承载的风险事项仍应优先识别为问题与风险记录。",
  communication_service_record: "出现投诉、风险、延期、质量问题时优先归入问题与风险记录。",
  issue_risk_record: "普通沟通不归入本类，必须存在问题、风险或负面后果信号。",
  decision_change_record: "仅执行既定施工动作不归入本类。",
  relationship_record: "只出现主体名称但描述施工、财务、采购等事项时按具体事项分类。",
  attendance_record: "施工动作中提到人员但不描述出勤时不归入本类。",
  resume_record: "当前发生的施工、沟通、财务等事实不归入履历记录。",
  business_maintenance_record: "已经发生的收付款归入财务记录。",
  acceptance_delivery_record: "施工过程进展未到验收交付节点时归入施工记录。",
  purchase_record: "材料到货、入库、领用等现场流转归入材料流转记录。",
  other_fact_record: "仅当 13 类明确类型均无法命中时使用，不替代明确分类。",
};

export const FACT_RECORD_TYPE_RULES = Object.fromEntries(
  Object.keys(FACT_RECORD_TYPE_DISPLAY).map((factType) => [
    factType,
    {
      displayName: FACT_RECORD_TYPE_DISPLAY[factType],
      keywords: FACT_RECORD_TYPE_KEYWORDS[factType],
      boundary: FACT_RECORD_TYPE_BOUNDARIES[factType],
    },
  ]),
) as Record<string, { displayName: string; keywords: readonly string[]; boundary: string }>;
