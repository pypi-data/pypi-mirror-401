# service/core/lifespan.py
"""
应用生命周期管理（精简版）

职责：
- 协调各个服务的启动和关闭
- 不包含具体的连接逻辑
- 支持可选依赖的优雅降级
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from infoman.config import settings

# ========== 数据库（必需） ==========
if settings.USE_PRO_ORM:
    from infoman.service.infrastructure.db_relation.manager_pro import db_manager
    _DB_MANAGER_TYPE = "pro"
else:
    from infoman.service.infrastructure.db_relation.manager import db_manager
    _DB_MANAGER_TYPE = "basic"

# ========== Redis（可选） ==========
try:
    from infoman.service.infrastructure.db_cache.manager import RedisManager
    REDIS_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ Redis 依赖未安装，缓存功能将不可用 (需要: redis, fastapi-cache2)")
    RedisManager = None
    REDIS_AVAILABLE = False

# ========== 向量数据库（可选） ==========
try:
    from infoman.service.infrastructure.db_vector.manager import VectorDBManager
    VECTOR_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ 向量数据库依赖未安装，向量搜索功能将不可用 (需要: qdrant-client)")
    VectorDBManager = None
    VECTOR_AVAILABLE = False

# ========== 消息队列（可选） ==========
try:
    from infoman.service.infrastructure.mq import NATSManager
    MQ_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ 消息队列依赖未安装，NATS 功能将不可用 (需要: nats-py)")
    NATSManager = None
    MQ_AVAILABLE = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理（支持可选依赖）"""

    # ========== 启动 ==========
    logger.info(f"🚀 应用启动中 [{settings.APP_NAME} v{settings.APP_VERSION}]")
    logger.info(f"   环境: {settings.ENV}")
    logger.info(f"   数据库管理器: {_DB_MANAGER_TYPE}")
    logger.info(f"   可选功能: Redis={REDIS_AVAILABLE}, Vector={VECTOR_AVAILABLE}, MQ={MQ_AVAILABLE}")

    # 初始化管理器（仅限已安装的）
    managers = {}

    # 数据库（必需）
    managers['db'] = db_manager
    app.state.db_manager = db_manager

    # Redis（可选）
    if REDIS_AVAILABLE:
        redis_manager = RedisManager()
        managers['redis'] = redis_manager
        app.state.redis_manager = redis_manager

    # 向量数据库（可选）
    if VECTOR_AVAILABLE:
        vector_manager = VectorDBManager()
        managers['vector'] = vector_manager
        app.state.vector_manager = vector_manager

    # 消息队列（可选）
    if MQ_AVAILABLE:
        nats_manager = NATSManager()
        managers['mq'] = nats_manager
        app.state.nats_manager = nats_manager

    try:
        # 1. 数据库
        await db_manager.startup(app)

        # 2. Redis（如果可用）
        if 'redis' in managers:
            await managers['redis'].startup(app)

        # 3. 向量数据库（如果可用）
        if 'vector' in managers:
            await managers['vector'].startup(app)

        # 4. 消息队列（如果可用）
        if 'mq' in managers:
            await managers['mq'].startup(app)

        logger.success("✅ 所有服务启动完成")

    except Exception as e:
        logger.error(f"❌ 服务启动失败: {e}")
        raise

    # ========== 运行 ==========
    yield

    # ========== 关闭 ==========
    logger.info("⏹️ 应用关闭中...")

    try:
        # 按相反顺序关闭（仅关闭已启动的）
        if 'mq' in managers:
            await managers['mq'].shutdown()

        if 'vector' in managers:
            await managers['vector'].shutdown()

        if 'redis' in managers:
            await managers['redis'].shutdown()

        await db_manager.shutdown()

        logger.success("✅ 所有服务已关闭")

    except Exception as e:
        logger.error(f"❌ 服务关闭失败: {e}")
