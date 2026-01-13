"""
NexAgent WebServer - 集成 API 和前端的 Web 服务器
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import json
import os
from .framework import NexFramework
from ._version import __version__
from .openapi_server import router as openapi_router

app = FastAPI(title="NexAgent WebServer", version=__version__)

# 使用当前工作目录
nex = NexFramework(os.getcwd())

# 将nex实例存储到app.state中，供OpenAPI路由使用
app.state.nex = nex

# 注册OpenAPI路由
app.include_router(openapi_router)

# 静态文件目录
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')


class ChatRequest(BaseModel):
    user: str = "guest"
    message: str
    session_id: Optional[int] = None
    stream: bool = False
    save_user_message: bool = True  # 重新生成时设为False
    use_system_prompt: bool = False  # 是否使用系统提示词
    model_key: Optional[str] = None  # 指定使用的模型


class DeleteRequest(BaseModel):
    id: Optional[int] = None


class CreateSessionRequest(BaseModel):
    name: str = "新会话"
    user: str = "guest"

class UpdateSessionRequest(BaseModel):
    name: str


class DeleteMessageRequest(BaseModel):
    message_id: int


class EditMessageRequest(BaseModel):
    content: str
    regenerate: bool = False


class RegenerateRequest(BaseModel):
    session_id: int


# 服务商相关请求模型
class AddProviderRequest(BaseModel):
    id: str
    name: str
    api_key: str
    base_url: str


class UpdateProviderRequest(BaseModel):
    name: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None


# 模型相关请求模型
class AddModelRequest(BaseModel):
    provider_id: str
    model_id: str
    display_name: str
    tags: Optional[list] = None
    model_type: str = "chat"  # "chat" 或 "embedding"


class UpdateModelRequest(BaseModel):
    model_id: Optional[str] = None
    display_name: Optional[str] = None
    tags: Optional[list] = None
    model_type: Optional[str] = None


# MCP 服务器相关请求模型
class AddMCPServerRequest(BaseModel):
    id: str
    name: str
    url: str
    server_type: str = "sse"  # "sse" 或 "streamable_http"
    headers: Optional[dict] = None


class UpdateMCPServerRequest(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    server_type: Optional[str] = None
    headers: Optional[dict] = None
    enabled: Optional[bool] = None


# 角色卡相关请求模型
class CreatePersonaRequest(BaseModel):
    name: str
    system_prompt: str
    avatar: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None


class UpdatePersonaRequest(BaseModel):
    name: Optional[str] = None
    system_prompt: Optional[str] = None
    avatar: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None


class SetSessionPersonaRequest(BaseModel):
    persona_id: Optional[int] = None


# ========== API 接口 ==========
@app.post("/nex/chat")
async def chat(req: ChatRequest):
    """对话接口"""
    try:
        if req.stream:
            def generate():
                tool_events = []
                thinking_events = []
                def collect_tool(event, data):
                    tool_events.append((event, data))
                def collect_thinking(event, data):
                    thinking_events.append((event, data))
                for chunk in nex.chat_stream(req.user, req.message, session_id=req.session_id, on_tool_call=collect_tool, save_user_message=req.save_user_message, on_thinking=collect_thinking, use_system_prompt=req.use_system_prompt, model_key=req.model_key):
                    # 先处理思考事件（实时输出）
                    while thinking_events:
                        e, d = thinking_events.pop(0)
                        if e == 'thinking_start':
                            yield f"data: {json.dumps({'type': 'thinking_start'}, ensure_ascii=False)}\n\n"
                        elif e == 'thinking':
                            yield f"data: {json.dumps({'type': 'thinking', 'data': d}, ensure_ascii=False)}\n\n"
                        elif e == 'thinking_end':
                            yield f"data: {json.dumps({'type': 'thinking_end'}, ensure_ascii=False)}\n\n"
                    # 处理工具事件
                    while tool_events:
                        e, d = tool_events.pop(0)
                        yield f"data: {json.dumps({'type': e, 'data': d}, ensure_ascii=False)}\n\n"
                    # 输出内容（只有非空时才输出）
                    if chunk:
                        yield f"data: {json.dumps({'type': 'content', 'data': chunk}, ensure_ascii=False)}\n\n"
                # 返回当前会话ID和tokens
                tokens = getattr(nex, '_last_tokens', None)
                yield f"data: {json.dumps({'type': 'done', 'session_id': nex._current_session_id, 'tokens': tokens}, ensure_ascii=False)}\n\n"
            return StreamingResponse(generate(), media_type="text/event-stream")
        else:
            reply = nex.chat(req.user, req.message, session_id=req.session_id, use_system_prompt=req.use_system_prompt, model_key=req.model_key)
            return {"code": 0, "data": {"reply": reply, "session_id": nex._current_session_id}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class SaveMessageRequest(BaseModel):
    session_id: int
    content: str
    content_parts: Optional[List[Dict]] = None
    tokens: Optional[Dict] = None
    interrupted: Optional[bool] = False


@app.post("/nex/messages/save")
async def save_message(req: SaveMessageRequest):
    """保存中断的消息（用于停止生成时保存已生成的内容）"""
    try:
        extra = {}
        if req.content_parts:
            extra["content_parts"] = req.content_parts
        if req.tokens:
            extra["tokens"] = req.tokens
        if req.interrupted:
            extra["interrupted"] = True  # 标记为被中断
        
        nex.db.add_message(req.session_id, 'assistant', req.content, extra=extra)
        return {"code": 0, "message": "消息已保存"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/nex/history")
async def get_history(limit: Optional[int] = None):
    return {"code": 0, "data": nex.get_history(limit)}


@app.delete("/nex/history")
async def delete_history(req: DeleteRequest = None):
    if nex.delete_history(req.id if req else None):
        return {"code": 0, "message": "删除成功"}
    raise HTTPException(status_code=404, detail="记录不存在")


@app.get("/nex/models")
async def get_models():
    current = nex.get_current_model()
    return {
        "code": 0, 
        "data": {
            "models": nex.get_models(), 
            "current": current
        }
    }


@app.post("/nex/models")
async def add_model(req: AddModelRequest):
    """添加新模型"""
    # 检查服务商是否存在
    provider = nex.get_provider(req.provider_id)
    if not provider:
        raise HTTPException(status_code=400, detail="服务商不存在")
    
    # 自动生成模型key: provider_id + model_id (去除特殊字符)
    import re
    model_key = f"{req.provider_id}_{re.sub(r'[^a-zA-Z0-9_-]', '_', req.model_id)}"
    
    if not nex.add_model(model_key, req.provider_id, req.model_id, req.display_name, req.tags, req.model_type):
        raise HTTPException(status_code=400, detail="该模型已存在")
    return {"code": 0, "message": "添加成功"}


@app.put("/nex/models/{model_key}")
async def update_model(model_key: str, req: UpdateModelRequest):
    """更新模型配置"""
    import re
    
    # 如果模型ID变更，需要生成新的 key
    new_key = None
    if req.model_id:
        # 获取当前模型的 provider_id
        model_detail = nex.get_model_detail(model_key)
        if not model_detail:
            raise HTTPException(status_code=404, detail="模型不存在")
        new_key = f"{model_detail['provider_id']}_{re.sub(r'[^a-zA-Z0-9_-]', '_', req.model_id)}"
        if new_key == model_key:
            new_key = None  # key 没变化
    
    result = nex.update_model_config(model_key, new_key, req.model_id, req.display_name, req.tags, req.model_type)
    if not result:
        raise HTTPException(status_code=400, detail="更新失败，可能模型ID已被使用")
    return {"code": 0, "message": "更新成功", "data": {"new_key": result}}


@app.delete("/nex/models/{model_key}")
async def delete_model(model_key: str):
    """删除模型"""
    models = nex.get_models()
    if len(models) <= 1:
        raise HTTPException(status_code=400, detail="至少保留一个模型")
    if not nex.delete_model_config(model_key):
        raise HTTPException(status_code=404, detail="模型不存在")
    return {"code": 0, "message": "删除成功"}


@app.get("/nex/models/{model_key}")
async def get_model_detail(model_key: str):
    """获取模型详情"""
    config = nex.get_model_detail(model_key)
    if not config:
        raise HTTPException(status_code=404, detail="模型不存在")
    return {"code": 0, "data": {
        "key": model_key,
        "display_name": config.get("display_name", model_key),
        "model_id": config.get("model_id", ""),
        "provider_id": config.get("provider_id", ""),
        "provider_name": config.get("provider_name", ""),
        "tags": config.get("tags", []),
        "model_type": config.get("model_type", "chat")
    }}


# ========== 服务商管理 API ==========
@app.get("/nex/providers")
async def get_providers():
    """获取所有服务商"""
    providers = nex.get_providers()
    # 隐藏部分 API key
    for p in providers:
        if p.get('api_key'):
            p['api_key'] = p['api_key'][:8] + '***' if len(p['api_key']) > 8 else '***'
    return {"code": 0, "data": providers}


@app.post("/nex/providers")
async def add_provider(req: AddProviderRequest):
    """添加服务商"""
    if not nex.add_provider(req.id, req.name, req.api_key, req.base_url):
        raise HTTPException(status_code=400, detail="服务商ID已存在")
    return {"code": 0, "message": "添加成功"}


@app.get("/nex/providers/{provider_id}")
async def get_provider(provider_id: str):
    """获取服务商详情"""
    provider = nex.get_provider(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="服务商不存在")
    # 隐藏部分 API key
    if provider.get('api_key'):
        provider['api_key_masked'] = provider['api_key'][:8] + '***' if len(provider['api_key']) > 8 else '***'
    return {"code": 0, "data": provider}


@app.put("/nex/providers/{provider_id}")
async def update_provider(provider_id: str, req: UpdateProviderRequest):
    """更新服务商"""
    if not nex.update_provider(provider_id, req.name, req.api_key, req.base_url):
        raise HTTPException(status_code=404, detail="服务商不存在或更新失败")
    return {"code": 0, "message": "更新成功"}


@app.delete("/nex/providers/{provider_id}")
async def delete_provider(provider_id: str):
    """删除服务商（同时删除关联的模型）"""
    if not nex.delete_provider(provider_id):
        raise HTTPException(status_code=404, detail="服务商不存在")
    return {"code": 0, "message": "删除成功"}


@app.get("/nex/providers/{provider_id}/models")
async def get_provider_models(provider_id: str):
    """获取供应商的模型列表（通过 /v1/models API）"""
    result = nex.fetch_provider_models(provider_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "获取失败"))
    return {"code": 0, "data": result["models"]}


@app.get("/nex/tools")
async def get_tools():
    """获取所有可用工具列表"""
    disabled_tools = json.loads(nex.db.get_setting('disabled_tools', '[]'))
    tools_list = []
    # 内置和自定义工具
    for tool in nex.tools:
        func = tool.get("function", {})
        name = func.get("name")
        tools_list.append({
            "name": name,
            "description": func.get("description"),
            "parameters": func.get("parameters"),
            "type": "builtin" if name in ["execute_shell", "http_request"] else "custom",
            "has_handler": name in nex._custom_tools or name in ["execute_shell", "http_request"],
            "enabled": name not in disabled_tools
        })
    # MCP 工具
    for tool in nex.get_mcp_tools():
        func = tool.get("function", {})
        name = func.get("name")
        tools_list.append({
            "name": name,
            "description": func.get("description"),
            "parameters": func.get("parameters"),
            "type": "mcp",
            "has_handler": True,
            "enabled": name not in disabled_tools
        })
    # 获取工具总开关状态
    tools_enabled = nex.db.get_setting('tools_enabled', 'true') == 'true'
    return {"code": 0, "data": tools_list, "enabled": tools_enabled}


@app.put("/nex/tools/toggle")
async def toggle_tools(enabled: bool):
    """切换工具总开关"""
    nex.db.set_setting('tools_enabled', 'true' if enabled else 'false')
    return {"code": 0, "enabled": enabled}


@app.post("/nex/tools/reload")
async def reload_tools():
    """热加载自定义工具"""
    try:
        result = nex.reload_custom_tools()
        return {"code": 0, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/nex/tools/{tool_name}/toggle")
async def toggle_single_tool(tool_name: str, enabled: bool):
    """切换单个工具开关"""
    disabled_tools = json.loads(nex.db.get_setting('disabled_tools', '[]'))
    if enabled:
        disabled_tools = [t for t in disabled_tools if t != tool_name]
    else:
        if tool_name not in disabled_tools:
            disabled_tools.append(tool_name)
    nex.db.set_setting('disabled_tools', json.dumps(disabled_tools))
    return {"code": 0, "enabled": enabled}


@app.put("/nex/tools/toggle-all")
async def toggle_all_tools(enabled: bool, tool_type: str = None):
    """批量切换工具开关"""
    if tool_type:
        # 获取指定类型的工具名
        tools_list = []
        if tool_type == 'builtin':
            tools_list = ["execute_shell", "http_request"]
        elif tool_type == 'custom':
            for tool in nex.tools:
                name = tool.get("function", {}).get("name")
                if name and name not in ["execute_shell", "http_request"]:
                    tools_list.append(name)
        
        disabled_tools = json.loads(nex.db.get_setting('disabled_tools', '[]'))
        if enabled:
            disabled_tools = [t for t in disabled_tools if t not in tools_list]
        else:
            for name in tools_list:
                if name not in disabled_tools:
                    disabled_tools.append(name)
        nex.db.set_setting('disabled_tools', json.dumps(disabled_tools))
    else:
        # 全部开关
        if enabled:
            nex.db.set_setting('disabled_tools', '[]')
        else:
            all_names = [t.get("function", {}).get("name") for t in nex.tools]
            nex.db.set_setting('disabled_tools', json.dumps(all_names))
    return {"code": 0, "enabled": enabled}


# ========== MCP 服务器管理 API ==========
@app.get("/nex/mcp/servers")
async def get_mcp_servers():
    """获取所有 MCP 服务器"""
    servers = nex.get_mcp_servers()
    return {"code": 0, "data": servers}


@app.post("/nex/mcp/servers")
async def add_mcp_server(req: AddMCPServerRequest):
    """添加 MCP 服务器"""
    result = nex.add_mcp_server(req.id, req.name, req.url, req.server_type, req.headers)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "添加失败"))
    return {"code": 0, "data": result, "message": "添加成功"}


@app.put("/nex/mcp/servers/{server_id}")
async def update_mcp_server(server_id: str, req: UpdateMCPServerRequest):
    """更新 MCP 服务器"""
    if not nex.update_mcp_server(server_id, req.name, req.url, req.server_type, req.headers, req.enabled):
        raise HTTPException(status_code=404, detail="服务器不存在或更新失败")
    return {"code": 0, "message": "更新成功"}


@app.delete("/nex/mcp/servers/{server_id}")
async def delete_mcp_server(server_id: str):
    """删除 MCP 服务器"""
    if not nex.delete_mcp_server(server_id):
        raise HTTPException(status_code=404, detail="服务器不存在")
    return {"code": 0, "message": "删除成功"}


@app.post("/nex/mcp/servers/{server_id}/reconnect")
async def reconnect_mcp_server(server_id: str):
    """重新连接 MCP 服务器"""
    if nex.reconnect_mcp_server(server_id):
        return {"code": 0, "message": "重新连接成功"}
    raise HTTPException(status_code=400, detail="重新连接失败")


# ========== 会话管理 API ==========
@app.get("/nex/sessions")
async def get_sessions(user: Optional[str] = None, limit: Optional[int] = None):
    """获取会话列表"""
    sessions = nex.get_sessions(user, limit)
    current = nex.get_current_session()
    return {"code": 0, "data": {"sessions": sessions, "current_id": current['id'] if current else None}}


@app.get("/nex/sessions/grouped")
async def get_sessions_grouped():
    """获取按角色卡分组的会话列表"""
    sessions = nex.get_sessions()
    personas = nex.get_personas()
    
    # 创建角色卡ID到角色卡的映射
    persona_map = {p['id']: p for p in personas}
    
    # 按角色卡分组
    grouped = {}
    ungrouped = []  # 没有角色卡的会话
    
    for session in sessions:
        persona_id = session.get('persona_id')
        if persona_id and persona_id in persona_map:
            if persona_id not in grouped:
                grouped[persona_id] = {
                    'persona': persona_map[persona_id],
                    'sessions': []
                }
            grouped[persona_id]['sessions'].append(session)
        else:
            ungrouped.append(session)
    
    # 转换为列表格式
    result = []
    
    # 先添加有角色卡的分组
    for persona_id, group in grouped.items():
        result.append({
            'persona': group['persona'],
            'sessions': group['sessions']
        })
    
    # 添加默认分组（没有角色卡的会话）
    if ungrouped:
        result.insert(0, {
            'persona': None,
            'sessions': ungrouped
        })
    
    return {"code": 0, "data": result}


@app.post("/nex/sessions")
async def create_session(req: CreateSessionRequest):
    """创建新会话"""
    session_id = nex.create_session(req.name, req.user)
    return {"code": 0, "data": {"session_id": session_id}, "message": "创建成功"}


@app.get("/nex/sessions/{session_id}")
async def get_session(session_id: int):
    """获取单个会话详情"""
    session = nex.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    return {"code": 0, "data": session}


@app.put("/nex/sessions/{session_id}")
async def update_session(session_id: int, req: UpdateSessionRequest):
    """更新会话名称"""
    if nex.update_session(session_id, req.name):
        return {"code": 0, "message": "更新成功"}
    raise HTTPException(status_code=404, detail="会话不存在")


@app.delete("/nex/sessions/{session_id}")
async def delete_session(session_id: int):
    """删除会话"""
    if nex.delete_session(session_id):
        return {"code": 0, "message": "删除成功"}
    raise HTTPException(status_code=404, detail="会话不存在")


@app.get("/nex/sessions/{session_id}/messages")
async def get_session_messages(session_id: int, limit: Optional[int] = None):
    """获取会话消息"""
    messages = nex.get_session_messages(session_id, limit)
    return {"code": 0, "data": messages}


@app.delete("/nex/sessions/{session_id}/messages")
async def clear_session_messages(session_id: int):
    """清空会话消息"""
    count = nex.clear_session_messages(session_id)
    return {"code": 0, "message": f"已删除 {count} 条消息"}


@app.delete("/nex/messages/{message_id}")
async def delete_message(message_id: int):
    """删除单条消息"""
    if nex.delete_message(message_id):
        return {"code": 0, "message": "删除成功"}
    raise HTTPException(status_code=404, detail="消息不存在")


@app.get("/nex/messages/{message_id}")
async def get_message(message_id: int):
    """获取单条消息"""
    msg = nex.get_message(message_id)
    if msg:
        return {"code": 0, "data": msg}
    raise HTTPException(status_code=404, detail="消息不存在")


@app.put("/nex/messages/{message_id}")
async def update_message(message_id: int, req: EditMessageRequest):
    """编辑消息内容"""
    msg = nex.get_message(message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="消息不存在")
    
    # 更新消息内容
    if not nex.update_message(message_id, req.content):
        raise HTTPException(status_code=500, detail="更新失败")
    
    # 如果需要重新生成，删除该消息之后的所有消息
    if req.regenerate and msg['role'] == 'user':
        nex.delete_messages_after(msg['session_id'], message_id)
    
    return {"code": 0, "message": "更新成功", "data": {"regenerate": req.regenerate, "session_id": msg['session_id']}}


@app.post("/nex/sessions/{session_id}/regenerate")
async def regenerate_response(session_id: int):
    """重新生成最后一条回复（流式）"""
    # 获取最后一条用户消息
    last_user_msg = nex.get_last_user_message(session_id)
    if not last_user_msg:
        raise HTTPException(status_code=400, detail="没有可重新生成的消息")
    
    # 删除该用户消息之后的所有消息（即AI回复）
    nex.delete_messages_after(session_id, last_user_msg['id'])
    
    # 返回需要重新发送的消息信息
    return {
        "code": 0, 
        "data": {
            "message": last_user_msg['content'],
            "user": last_user_msg['user'] or "guest",
            "message_id": last_user_msg['id']
        }
    }


# ========== 系统信息 API ==========
@app.get("/nex/version")
async def get_version():
    """获取版本号"""
    return {"code": 0, "data": {"version": __version__}}


# ========== 角色卡管理 API ==========
@app.get("/nex/personas")
async def get_personas():
    """获取所有角色卡"""
    personas = nex.get_personas()
    return {"code": 0, "data": personas}


@app.post("/nex/personas")
async def create_persona(req: CreatePersonaRequest):
    """创建角色卡"""
    persona_id = nex.create_persona(req.name, req.system_prompt, req.avatar, req.max_tokens, req.temperature, req.top_p)
    return {"code": 0, "data": {"id": persona_id}, "message": "创建成功"}


@app.get("/nex/personas/{persona_id}")
async def get_persona(persona_id: int):
    """获取单个角色卡"""
    persona = nex.get_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="角色卡不存在")
    return {"code": 0, "data": persona}


@app.put("/nex/personas/{persona_id}")
async def update_persona(persona_id: int, req: UpdatePersonaRequest):
    """更新角色卡"""
    if not nex.update_persona(persona_id, req.name, req.system_prompt, req.avatar, req.max_tokens, req.temperature, req.top_p):
        raise HTTPException(status_code=404, detail="角色卡不存在")
    return {"code": 0, "message": "更新成功"}


@app.delete("/nex/personas/{persona_id}")
async def delete_persona(persona_id: int):
    """删除角色卡"""
    if not nex.delete_persona(persona_id):
        raise HTTPException(status_code=404, detail="角色卡不存在")
    return {"code": 0, "message": "删除成功"}


@app.put("/nex/sessions/{session_id}/persona")
async def set_session_persona(session_id: int, req: SetSessionPersonaRequest):
    """设置会话的角色卡"""
    if not nex.set_session_persona(session_id, req.persona_id):
        raise HTTPException(status_code=404, detail="会话不存在")
    return {"code": 0, "message": "设置成功"}


@app.get("/nex/sessions/{session_id}/persona")
async def get_session_persona(session_id: int):
    """获取会话的角色卡"""
    persona = nex.get_session_persona(session_id)
    return {"code": 0, "data": persona}


# ========== 用户设置 API ==========
class UpdateSettingsRequest(BaseModel):
    settings: dict


@app.get("/nex/settings")
async def get_settings():
    """获取所有用户设置"""
    settings = nex.get_all_settings()
    return {"code": 0, "data": settings}


@app.put("/nex/settings")
async def update_settings(req: UpdateSettingsRequest):
    """更新用户设置"""
    for key, value in req.settings.items():
        nex.set_setting(key, str(value) if value is not None else "")
    return {"code": 0, "message": "保存成功"}


@app.get("/nex/settings/{key}")
async def get_setting(key: str):
    """获取单个设置"""
    value = nex.get_setting(key)
    return {"code": 0, "data": {"key": key, "value": value}}


@app.put("/nex/settings/{key}")
async def set_setting(key: str, value: str):
    """设置单个值"""
    nex.set_setting(key, value)
    return {"code": 0, "message": "保存成功"}


# ========== 记忆管理 API ==========
class AddMemoryRequest(BaseModel):
    content: str
    importance: int = 5


class UpdateMemoryRequest(BaseModel):
    content: Optional[str] = None
    importance: Optional[int] = None
    regenerate_embedding: bool = False


@app.get("/nex/memories")
async def get_memories(user: str = "guest", limit: int = 50):
    """获取用户的所有记忆"""
    memories = nex.get_memories(user, limit)
    # 移除向量数据（太大了）
    for m in memories:
        m.pop('embedding', None)
    return {"code": 0, "data": memories}


@app.post("/nex/memories")
async def add_memory(req: AddMemoryRequest, user: str = "guest"):
    """添加记忆"""
    memory_id = nex.add_memory(user, req.content, req.importance)
    if memory_id:
        return {"code": 0, "data": {"id": memory_id}, "message": "添加成功"}
    raise HTTPException(status_code=500, detail="添加失败，可能未配置嵌入模型")


@app.get("/nex/memories/{memory_id}")
async def get_memory(memory_id: int):
    """获取单条记忆"""
    memory = nex.get_memory(memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="记忆不存在")
    memory.pop('embedding', None)
    return {"code": 0, "data": memory}


@app.put("/nex/memories/{memory_id}")
async def update_memory(memory_id: int, req: UpdateMemoryRequest):
    """更新记忆"""
    if not nex.update_memory(memory_id, req.content, req.importance, req.regenerate_embedding):
        raise HTTPException(status_code=404, detail="记忆不存在")
    return {"code": 0, "message": "更新成功"}


@app.delete("/nex/memories/{memory_id}")
async def delete_memory(memory_id: int):
    """删除记忆"""
    if not nex.delete_memory(memory_id):
        raise HTTPException(status_code=404, detail="记忆不存在")
    return {"code": 0, "message": "删除成功"}


@app.delete("/nex/memories")
async def delete_all_memories(user: str = "guest"):
    """删除用户的所有记忆"""
    count = nex.delete_user_memories(user)
    return {"code": 0, "data": {"deleted": count}, "message": f"已删除 {count} 条记忆"}


@app.post("/nex/memories/search")
async def search_memories(query: str, user: str = "guest", top_k: int = 5):
    """搜索相关记忆"""
    memories = nex.search_memories(user, query, top_k)
    for m in memories:
        m.pop('embedding', None)
    return {"code": 0, "data": memories}


@app.get("/nex/embedding/status")
async def get_embedding_status():
    """获取嵌入模型状态"""
    model = nex.get_embedding_model()
    models = nex.get_embedding_models()
    return {
        "code": 0,
        "data": {
            "available": model is not None,
            "model": model['display_name'] if model else None,
            "model_id": model['id'] if model else None,
            "models": [{"id": m['id'], "name": m['display_name']} for m in models]
        }
    }


@app.put("/nex/embedding/model")
async def set_embedding_model(model_key: str):
    """设置嵌入模型"""
    nex.set_setting('embedding_model', model_key)
    return {"code": 0, "message": "设置成功"}


# ========== 系统提示词 ==========
@app.get("/nex/prompts")
async def get_system_prompt():
    """获取系统提示词"""
    from .prompts import get_system_prompt
    return {"code": 0, "data": {"prompt": get_system_prompt()}}


# ========== 前端页面 ==========
@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = os.path.join(STATIC_DIR, 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})


@app.get("/style.css")
async def get_css():
    css_path = os.path.join(STATIC_DIR, 'style.css')
    return FileResponse(css_path, media_type='text/css', headers={"Cache-Control": "no-cache, no-store, must-revalidate"})


@app.get("/app.js")
async def get_js():
    js_path = os.path.join(STATIC_DIR, 'app.js')
    return FileResponse(js_path, media_type='application/javascript', headers={"Cache-Control": "no-cache, no-store, must-revalidate"})


# ========== OpenAPI 配置管理 ==========
class OpenAPIConfigRequest(BaseModel):
    api_model_id: str
    internal_model_key: str
    persona_id: Optional[int] = None
    use_system_prompt: bool = False


class UpdateOpenAPIConfigRequest(BaseModel):
    internal_model_key: Optional[str] = None
    persona_id: Optional[int] = None
    use_system_prompt: Optional[bool] = None


@app.get("/nex/openapi/configs")
async def get_openapi_configs():
    """获取所有OpenAPI配置"""
    try:
        configs = nex.db.get_openapi_configs()
        return {"code": 0, "data": configs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/nex/openapi/configs")
async def create_openapi_config(req: OpenAPIConfigRequest):
    """创建OpenAPI配置"""
    try:
        config_id = nex.db.create_openapi_config(
            req.api_model_id,
            req.internal_model_key,
            req.persona_id,
            req.use_system_prompt
        )
        return {"code": 0, "data": {"id": config_id}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/nex/openapi/configs/{api_model_id}")
async def update_openapi_config(api_model_id: str, req: UpdateOpenAPIConfigRequest):
    """更新OpenAPI配置"""
    try:
        nex.db.update_openapi_config(
            api_model_id,
            req.internal_model_key,
            req.persona_id,
            req.use_system_prompt
        )
        return {"code": 0, "message": "更新成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/nex/openapi/configs/{api_model_id}")
async def delete_openapi_config(api_model_id: str):
    """删除OpenAPI配置"""
    try:
        nex.db.delete_openapi_config(api_model_id)
        return {"code": 0, "message": "删除成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/nex/openapi/dialogs")
async def get_api_dialogs(time_range: str = "week", model_filter: str = ""):
    """获取API对话记录"""
    try:
        # 根据时间范围计算开始时间
        import datetime
        now = datetime.datetime.now()
        if time_range == "today":
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif time_range == "week":
            start_time = now - datetime.timedelta(days=7)
        elif time_range == "month":
            start_time = now - datetime.timedelta(days=30)
        else:  # all
            start_time = None
        
        # 获取API会话（用户名为api_user的会话）
        sessions = nex.db.get_api_sessions(start_time, model_filter)
        
        dialogs = []
        for session in sessions:
            messages = nex.db.get_session_messages(session['id'])
            if messages:
                # 获取会话的角色卡信息
                persona = None
                if session.get('persona_id'):
                    persona = nex.db.get_persona(session['persona_id'])
                
                dialogs.append({
                    'session_id': session['id'],
                    'session_name': session['name'],
                    'created_at': session['created_at'],
                    'persona': persona,
                    'messages': messages
                })
        
        return {"code": 0, "data": dialogs}
    except Exception as e:
        return {"code": 1, "message": str(e)}
