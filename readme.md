# FastAPI Template

一个快速构建 FastAPI app 的模板:
- 基于 SQLAlchemy 的 async ORM 支持
- alembic 实现数据库迁移
- FastAPI 生态: `typer, pydantic[dotenv]` 
- fastapi-utils 提供基于类的视图 `cbv` 和自动解析返回值 type hint 的 `InferringRouter`
- view - service - dao - model 分层, 快速构建 CRUD API
- 自定义的返回格式 `core.responses`
- 基础的用户登录注册 api
- 异常处理
- CORS
- ...

