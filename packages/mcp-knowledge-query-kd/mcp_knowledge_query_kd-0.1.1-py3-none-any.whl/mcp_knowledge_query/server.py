import json
import os
import sys
import logging
import tempfile
from typing import List, Optional

# Configure logging
# 获取系统临时目录，确保在任何环境下（包括打包发布后）都有写入权限
log_file_path = os.path.join(tempfile.gettempdir(), "mcp_knowledge_query.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(log_file_path, encoding='utf-8')
    ],
    force=True
)
logger = logging.getLogger("mcp_knowledge_query.server")

# 在 stderr 中打印日志文件位置，方便用户查找
sys.stderr.write(f"\n[INFO] Logging to file: {log_file_path}\n")

# --- Path Fix Start ---
# 动态添加 src 目录到 sys.path，解决直接运行脚本时的 ModuleNotFoundError
# 这样无论是本地调试还是直接拷贝源码部署，都能找到 mcp_knowledge_query 包
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
# --- Path Fix End ---

from mcp.server import FastMCP
from mcp_knowledge_query.query_knowledge import query_knowledge_base

mcp = FastMCP("KnowledgeQueryService")

# 配置常量 - 优先从环境变量获取，避免硬编码敏感信息
AK = os.getenv("HIAGENT_AK")
SK = os.getenv("HIAGENT_SK")
HOST = os.getenv("HIAGENT_HOST", "https://hiagent-api.x-peng.com")
WORKSPACE_ID = os.getenv("HIAGENT_WORKSPACE_ID")
# 支持从环境变量读取数据集 ID，用逗号分隔
_dataset_ids_env = os.getenv("HIAGENT_DATASET_IDS")
if _dataset_ids_env:
    DEFAULT_DATASET_IDS = [x.strip() for x in _dataset_ids_env.split(",") if x.strip()]
else:
    DEFAULT_DATASET_IDS = []

@mcp.tool()
def query_knowledge(
    query: str,
    dataset_ids: Optional[List[str]] = None,
    top_k: int = 5,
    score_threshold: float = 0.6,
    expand: bool = True,
    expand_num: int = 1
) -> str:
    """
    查询知识库以获取相关信息。
    当用户询问特定领域知识（如离港时间、规则等）时使用此工具。

    Args:
        query: 用户查询语句或关键词
        dataset_ids: (可选) 指定要查询的知识库 ID 列表。如果不填，将使用默认配置的知识库。
        top_k: 返回的最大结果数量，默认为 5
        score_threshold: 相关性分数阈值，推荐 0.6，默认为 0.6
        expand: 是否开启查询膨胀（Query Expansion），默认为 True
        expand_num: 膨胀系数，默认为 1
    """
    # 将单个查询字符串转换为列表，适配底层 API
    keywords = [query]
    logger.info(f"Received query_knowledge request: query='{query}', dataset_ids={dataset_ids}, top_k={top_k}")


    # 运行时检查配置
    if not AK or not SK:
        return "错误: 未配置 AK/SK 环境变量 (HIAGENT_AK, HIAGENT_SK)。请在服务器环境中设置这些变量。"

    if not WORKSPACE_ID:
        return "错误: 未配置 WORKSPACE_ID 环境变量 (HIAGENT_WORKSPACE_ID)。"

    # 确定最终使用的 dataset_ids
    # 优先使用函数传入的参数，如果没有，则使用环境变量配置的默认值
    final_dataset_ids = dataset_ids if dataset_ids else DEFAULT_DATASET_IDS
    logger.info(f"Using final_dataset_ids: {final_dataset_ids}")

    if not final_dataset_ids:
        return "错误: 未提供 dataset_ids，且未配置默认知识库环境变量 (HIAGENT_DATASET_IDS)。"

    try:
        logger.info("Calling query_knowledge_base...")
        result = query_knowledge_base(
            ak=AK,
            sk=SK,
            host=HOST,
            workspace_id=WORKSPACE_ID,
            keywords=keywords,
            dataset_ids=final_dataset_ids,
            top_k=top_k,
            score_threshold=score_threshold,
            Expand=expand,
            ExpandNum=expand_num
        )
        logger.info("query_knowledge_base returned successfully")
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error in query_knowledge: {e}", exc_info=True)
        return f"查询出错: {str(e)}"

def main():
    """入口函数：统一处理 Windows 编码问题"""
    # 修复 Windows 下 'utf-8' codec can't decode byte 0xff 错误
    # MCP 协议强制要求 UTF-8，而 Windows 终端默认可能只有 GBK
    if sys.platform == "win32":
        try:
            sys.stdin.reconfigure(encoding='utf-8')
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception as e:
            logger.warning(f"Failed to reconfigure stdio encoding: {e}")

    # 启动 MCP 服务
    mcp.run()

if __name__ == "__main__":
    main()
