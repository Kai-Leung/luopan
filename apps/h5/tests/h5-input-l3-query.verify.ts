import { resolveTextInputIntent, getActionFromTextIntent } from '../src/modules/input_flow/h5Interaction';
import { buildL3FactListPath } from '../src/modules/l3_query_view/api';

type CaseResult = {
  name: string;
  passed: boolean;
  detail: string;
};

function check(name: string, passed: boolean, detail: string): CaseResult {
  return { name, passed, detail };
}

export function verifyH5InputL3QueryRouting(): CaseResult[] {
  const recordIntent = resolveTextInputIntent('今天现场完成防水施工记录');
  const queryIntent = resolveTextInputIntent('查防水记录');
  const analysisIntent = resolveTextInputIntent('帮我分析一下防水风险');
  const queryPath = buildL3FactListPath({ keyword: '查防水记录', limit: 5, offset: 0 });

  return [
    check(
      'record input stays on record action',
      recordIntent === 'record' && getActionFromTextIntent(recordIntent) === '录入',
      `intent=${recordIntent}`,
    ),
    check(
      'query input maps to L3 readonly query action',
      queryIntent === 'query' && getActionFromTextIntent(queryIntent) === '查',
      `intent=${queryIntent}`,
    ),
    check(
      'analysis input remains waiting for future analysis action',
      analysisIntent === 'analysis' && getActionFromTextIntent(analysisIntent) === '问',
      `intent=${analysisIntent}`,
    ),
    check(
      'L3 list path uses existing readonly endpoint',
      queryPath === '/api/v1/l3/facts?keyword=%E6%9F%A5%E9%98%B2%E6%B0%B4%E8%AE%B0%E5%BD%95&limit=5&offset=0',
      queryPath,
    ),
  ];
}
