import json
import logging
from mcp_knowledge_query.client import HiAgentAuth

logger = logging.getLogger(__name__)


def query_knowledge_base(ak, sk, host, workspace_id, keywords, dataset_ids=None, top_k=10, score_threshold=0.6,
                         **kwargs):
    """
    执行知识库检索 (Action: Query)

    :param ak: Access Key
    :param sk: Secret Key
    :param host: API Host (例如 https://hiagent-api.x-peng.com)
    :param workspace_id: 工作空间ID (WorkspaceID)
    :param keywords: 查询关键词列表 (Keywords)
    :param dataset_ids: 知识库ID列表 (DatasetIds)
    :param top_k: 返回结果数量 (TopK)
    :param score_threshold: 分数阈值 (ScoreThreshold)
    :param kwargs: 其他可选参数，如 RerankID, Expand, UserInfo 等
    :return: 响应 JSON 数据
    """

    # 构造请求体 (Body)
    data = {
        "WorkspaceID": workspace_id,
        "Keywords": keywords,
        "TopK": top_k,
        "ScoreThreshold": score_threshold,
        "DatasetIds": dataset_ids if dataset_ids else []
    }

    # 合并其他可选参数
    if kwargs:
        data.update(kwargs)

    logger.info(f"Querying knowledge base with data: {json.dumps(data, ensure_ascii=False)}")

    # 实例化鉴权类并发送请求
    client = HiAgentAuth(ak, sk)
    return client.make_request(
        host=host,
        action='Query',
        version='2023-08-01',  # 固定版本号
        data=data,
        method='POST'
    )

