import json
import logging
import os
from contextlib import contextmanager
from datetime import datetime
from typing import List, Optional, Any, Tuple

from filelock import FileLock, Timeout
from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
from pydantic import BaseModel, Field

from app.config import setup_logging
from app.amazon_sp_api import get_all_product_urls
from app.notifier import ding_talk_notifier
from app.spider import run_task
from app.dingtalk_doc_reader import dingtalk_doc_reader

# --- 全局配置 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
PRODUCT_URLS_FILE = os.path.join(DATA_DIR, 'product_urls.json')
LOCK_FILE = os.path.join(DATA_DIR, 'data.lock')
BACKUP_FILE = os.path.join(DATA_DIR, 'dingtalk_doc_backup_ALL.json')

# 数据源显示文本映射
DATA_SOURCE_TEXT_MAP = {
    "request_body": "请求参数",
    "dingtalk_doc_api": "钉钉文档API",
    "dingtalk_backup_file": "钉钉文档备份",
    "product_urls_file": "本地文件"
}

# --- 初始化 ---
os.makedirs(DATA_DIR, exist_ok=True)

# 使用统一的日志配置
setup_logging(os.path.join(DATA_DIR, 'app.log'))
logger = logging.getLogger(__name__)

app = FastAPI()

# --- Pydantic 模型定义 ---

class ProductURLResponse(BaseModel):
    status: str = "success"
    count: int
    urls: List[str]

class ProcessRequest(BaseModel):
    urls: Optional[List[str]] = Field(None, description="要处理的URL列表，如果为空则从文件读取")

class SpiderResult(BaseModel):
    url: str
    result: int
    error: Optional[str] = None

class ProcessResponse(BaseModel):
    status: str = "success"
    message: str
    data: List[SpiderResult]

# --- 并发控制辅助函数 ---

@contextmanager
def file_lock_manager(lock_path: str, timeout: int = 10):
    """上下文管理器，用于获取和释放文件锁"""
    lock = FileLock(lock_path)
    try:
        lock.acquire(timeout=timeout)
        yield
    except Timeout:
        logger.error(f"无法在 {timeout} 秒内获取文件锁: {lock_path}")
        raise HTTPException(status_code=503, detail="Service Unavailable: Could not acquire file lock.")
    finally:
        if lock.is_locked:
            lock.release()

def write_json_atomic(file_path: str, data: Any):
    """原子性地写入JSON文件"""
    temp_file_path = f"{file_path}.tmp"
    with open(temp_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    # os.replace 在大多数操作系统上是原子操作
    os.replace(temp_file_path, file_path)
    logger.info(f"数据已原子性写入: {file_path}")

def read_json_safe(file_path: str) -> Optional[Any]:
    """安全地读取JSON文件"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            logger.error(f"JSON解码错误: {file_path}")
            return None


def get_urls_from_sources() -> Tuple[List[str], str]:
    """
    按优先级从多个数据源获取URL列表

    优先级顺序:
    1. 钉钉文档API（如果启用）
    2. 钉钉文档备份文件
    3. product_urls.json 本地文件

    Returns:
        Tuple[List[str], str]: (URL列表, 数据源标识)

    Raises:
        HTTPException: 当所有数据源都无法获取URL时
    """
    # 优先级1: 钉钉文档API
    if dingtalk_doc_reader.is_enabled():
        logger.info("钉钉文档功能已启用，尝试从钉钉文档读取URL")
        try:
            doc_urls = dingtalk_doc_reader.read_urls_from_doc(sheet_name='ALL')
            if doc_urls:
                logger.info(f"从钉钉文档API成功读取 {len(doc_urls)} 个有效URL")
                return doc_urls, "dingtalk_doc_api"
            logger.warning("钉钉文档API返回空URL列表")
        except Exception as e:
            logger.warning(f"从钉钉文档API读取失败: {e}")
    else:
        logger.info("钉钉文档功能未启用")

    # 优先级2: 钉钉文档备份文件
    if os.path.exists(BACKUP_FILE):
        try:
            backup_data = read_json_safe(BACKUP_FILE)
            if backup_data and "urls" in backup_data and isinstance(backup_data["urls"], list):
                urls = backup_data["urls"]
                logger.info(f"从钉钉文档备份文件成功读取 {len(urls)} 个有效URL")
                logger.info(f"备份文件时间戳: {backup_data.get('timestamp', '未知')}")
                return urls, "dingtalk_backup_file"
            logger.warning("钉钉文档备份文件格式不正确")
        except Exception as e:
            logger.warning(f"从钉钉文档备份文件读取失败: {e}")
    else:
        logger.debug(f"钉钉文档备份文件不存在: {BACKUP_FILE}")

    # 优先级3: product_urls.json 本地文件
    logger.info("尝试从product_urls.json文件读取URL")
    with file_lock_manager(LOCK_FILE):
        data = read_json_safe(PRODUCT_URLS_FILE)
        if data and "urls" in data and isinstance(data["urls"], list):
            urls = data["urls"]
            logger.info(f"从product_urls.json文件成功加载 {len(urls)} 个URL")
            return urls, "product_urls_file"

    # 所有数据源都失败
    logger.error("所有数据源都无法获取URL")
    raise HTTPException(status_code=404, detail="No URLs found from any data source.")


# --- API 接口实现 ---

@app.post("/get-all-product-urls", response_model=ProductURLResponse)
async def get_products():
    """
    从SP-API获取所有商品链接，并使用文件锁和原子写入保存到本地。
    """
    try:
        urls = await get_all_product_urls()
        if not urls:
            logger.warning("从SP-API未获取到任何商品链接。")
            return {"status": "success", "count": 0, "urls": []}

        with file_lock_manager(LOCK_FILE):
            write_json_atomic(PRODUCT_URLS_FILE, {"urls": urls})
        
        return {"status": "success", "count": len(urls), "urls": urls}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"获取商品链接时发生未知错误: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/test-dingtalk")
async def test_dingtalk_connection():
    """
    测试钉钉文档API连接
    """
    try:
        if not dingtalk_doc_reader.is_enabled():
            return {
                "status": "disabled",
                "message": "钉钉文档功能未启用或配置不完整",
                "config_check": {
                    "doc_enabled": dingtalk_doc_reader.doc_enabled,
                    "doc_url": bool(dingtalk_doc_reader.doc_url),
                    "app_key": bool(dingtalk_doc_reader.app_key),
                    "app_secret": bool(dingtalk_doc_reader.app_secret),
                    "operator_id": bool(dingtalk_doc_reader.operator_id)
                }
            }
        
        # 测试连接
        connection_ok = dingtalk_doc_reader.test_connection()
        
        if connection_ok:
            # 尝试读取文档
            try:
                urls = dingtalk_doc_reader.read_urls_from_doc('ALL')
                return {
                    "status": "success",
                    "message": "钉钉文档API连接成功",
                    "urls_count": len(urls),
                    "sample_urls": urls[:3] if urls else []
                }
            except Exception as e:
                return {
                    "status": "partial_success",
                    "message": "API连接成功，但读取文档失败",
                    "error": str(e)
                }
        else:
            return {
                "status": "failed",
                "message": "钉钉文档API连接失败，请检查配置"
            }
            
    except Exception as e:
        logger.error(f"测试钉钉连接时发生错误: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"测试过程中发生错误: {e}"
        }

@app.post("/process", response_model=ProcessResponse)
async def process_urls(background_tasks: BackgroundTasks, request_data: ProcessRequest = Body(None)):
    """
    处理商品链接。
    - 如果请求体包含URLs，则处理这些URL。
    - 如果请求体为空，则按优先级从数据源获取URL。
    """
    urls_to_process: List[str] = []
    data_source = "unknown"

    if request_data and request_data.urls:
        logger.info(f"收到 {len(request_data.urls)} 个URL进行处理")
        urls_to_process = request_data.urls
        data_source = "request_body"
    else:
        logger.info("请求体为空，按优先级顺序获取URL数据")
        urls_to_process, data_source = get_urls_from_sources()

    if not urls_to_process:
        return {"status": "success", "message": "No URLs to process.", "data": []}

    try:
        product_count = len(urls_to_process)
        estimated_time = round(product_count * 10 / 60)
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_source_text = DATA_SOURCE_TEXT_MAP.get(data_source, "未知来源")

        title = "监控任务状态"
        text = f"""### 监控任务状态

**任务执行**: 已启用

**数据来源**: {data_source_text}

**商品抓取**: 已获取 {product_count} 个商品页

**预计耗时**: {estimated_time} 分钟

**启动时间**: {start_time}

---

**正在进行**: 正在执行店铺购物车检查，请等待检查结果"""
        ding_talk_notifier.send_markdown(title, text, is_at_all=False)
        background_tasks.add_task(run_task, urls_to_process, data_source)
        return {
            "status": "success",
            "message": f"Processing started in the background. Data source: {data_source}",
            "data": []
        }
    except Exception as e:
        logger.error(f"处理URL时发生爬虫错误: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {e}")


@app.get("/task/progress")
async def get_task_progress():
    """
    获取当前任务进度。
    返回终端UI的统计信息（如果有正在运行的任务）。
    """
    try:
        from app.terminal_ui import get_terminal_ui
        terminal_ui = get_terminal_ui()

        if terminal_ui is None:
            return {
                "status": "no_task",
                "message": "当前没有正在运行的任务"
            }

        stats = terminal_ui.get_stats()
        total = stats.get('total', 0)
        current = stats.get('current', 0)
        progress_pct = (current / max(total, 1)) * 100

        return {
            "status": "running",
            "progress": {
                "total": total,
                "current": current,
                "percentage": round(progress_pct, 1),
                "success": stats.get('success', 0),
                "out_of_stock": stats.get('out_of_stock', 0),
                "cart_missing": stats.get('cart_missing', 0),
                "failed": stats.get('failed', 0),
                "captcha": stats.get('captcha', 0)
            },
            "data_source": stats.get('data_source', 'unknown'),
            "current_url": stats.get('current_url', ''),
            "start_time": stats.get('start_time').isoformat() if stats.get('start_time') else None
        }

    except ImportError:
        return {
            "status": "unavailable",
            "message": "终端UI模块未安装"
        }
    except Exception as e:
        logger.error(f"获取任务进度时发生错误: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"获取进度失败: {e}"
        }


@app.get("/health")
async def health_check():
    """
    健康检查接口，返回系统状态。
    """
    return {
        "status": "healthy",
        "service": "AmazonMonitor",
        "endpoints": {
            "get_products": "/get-all-product-urls",
            "process": "/process",
            "task_progress": "/task/progress",
            "test_dingtalk": "/test-dingtalk"
        }
    }


# --- 启动命令 ---
# uvicorn app.main:app --reload
