from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import Middleware, MiddlewareContext

from src.config import settings
from src.utils import create_finam_client


class FinamCredentialsMiddleware(Middleware):
    """Middleware для создания FinamClient из заголовков и добавления в контекст."""

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        """Перехватываем все вызовы tools."""

        # Получаем заголовки из HTTP запроса
        headers = get_http_headers()

        # Извлекаем необходимые заголовки
        api_key = headers.get("finam-api-key") or settings.FINAM_API_KEY
        account_id = headers.get("finam-account-id") or settings.FINAM_ACCOUNT_ID

        # 检查是否为测试模式（如果没有提供凭据）
        if not api_key or not account_id:
            # 在测试模式下，跳过客户端创建，直接继续执行
            # 这样可以让MCP服务器启动并显示工具列表
            return await call_next(context)

        # 创建客户端 Finam
        try:
            finam_client = await create_finam_client(
                api_key=api_key, account_id=account_id
            )
        except Exception as e:
            raise ToolError(str(e)) from e

        # Сохраняем клиента в state контекста
        if context.fastmcp_context:
            context.fastmcp_context.set_state("finam_client", finam_client)

        # Продолжаем выполнение
        return await call_next(context)