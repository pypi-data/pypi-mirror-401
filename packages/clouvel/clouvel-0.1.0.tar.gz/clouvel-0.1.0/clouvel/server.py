import re
from pathlib import Path
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("clouvel")

# 필수 문서 정의
REQUIRED_DOCS = [
    {"type": "prd", "name": "PRD", "patterns": [r"prd", r"product.?requirement"], "priority": "critical"},
    {"type": "architecture", "name": "아키텍처", "patterns": [r"architect", r"module"], "priority": "critical"},
    {"type": "api_spec", "name": "API 스펙", "patterns": [r"api", r"swagger", r"openapi"], "priority": "critical"},
    {"type": "db_schema", "name": "DB 스키마", "patterns": [r"schema", r"database", r"db"], "priority": "critical"},
    {"type": "verification", "name": "검증 계획", "patterns": [r"verif", r"test.?plan"], "priority": "critical"},
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="scan_docs",
            description="프로젝트 docs 폴더 스캔. 파일 목록 반환.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "docs 폴더 경로"}
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="analyze_docs",
            description="docs 폴더 분석. 필수 문서 있는지 체크하고 빠진 거 알려줌.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "docs 폴더 경로"}
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="get_prd_guide",
            description="PRD 작성 가이드. step-by-step으로 뭘 써야 하는지.",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_verify_checklist",
            description="PRD 검증 체크리스트. 빠뜨리기 쉬운 것들.",
            inputSchema={"type": "object", "properties": {}}
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "scan_docs":
        return await _scan_docs(arguments.get("path", ""))
    elif name == "analyze_docs":
        return await _analyze_docs(arguments.get("path", ""))
    elif name == "get_prd_guide":
        return await _get_prd_guide()
    elif name == "get_verify_checklist":
        return await _get_verify_checklist()
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def _scan_docs(path: str) -> list[TextContent]:
    docs_path = Path(path)

    if not docs_path.exists():
        return [TextContent(type="text", text=f"경로 없음: {path}")]

    if not docs_path.is_dir():
        return [TextContent(type="text", text=f"디렉토리 아님: {path}")]

    files = []
    for f in sorted(docs_path.iterdir()):
        if f.is_file():
            stat = f.stat()
            files.append(f"{f.name} ({stat.st_size:,} bytes)")

    result = f"📁 {path}\n총 {len(files)}개 파일\n\n"
    result += "\n".join(files)

    return [TextContent(type="text", text=result)]


async def _analyze_docs(path: str) -> list[TextContent]:
    docs_path = Path(path)

    if not docs_path.exists():
        return [TextContent(type="text", text=f"경로 없음: {path}")]

    files = [f.name.lower() for f in docs_path.iterdir() if f.is_file()]

    detected = []
    missing = []

    for req in REQUIRED_DOCS:
        found = False
        for filename in files:
            for pattern in req["patterns"]:
                if re.search(pattern, filename, re.IGNORECASE):
                    detected.append(req["name"])
                    found = True
                    break
            if found:
                break
        if not found:
            missing.append(req["name"])

    critical_total = len([r for r in REQUIRED_DOCS if r["priority"] == "critical"])
    critical_found = len([r for r in REQUIRED_DOCS if r["priority"] == "critical" and r["name"] in detected])
    coverage = critical_found / critical_total if critical_total > 0 else 1.0

    result = f"## 분석 결과: {path}\n\n"
    result += f"커버리지: {coverage:.0%}\n\n"

    if detected:
        result += "### 있음\n" + "\n".join(f"- {d}" for d in detected) + "\n\n"

    if missing:
        result += "### 없음 (작성 필요)\n" + "\n".join(f"- {m}" for m in missing) + "\n\n"

    if not missing:
        result += "필수 문서 다 있음. 바이브코딩 시작해도 됨.\n"
    else:
        result += f"⚠️ {len(missing)}개 문서 먼저 작성하고 코딩 시작할 것.\n"

    return [TextContent(type="text", text=result)]


async def _get_prd_guide() -> list[TextContent]:
    guide = """## PRD 작성법

> 이 문서가 법. 여기 없으면 안 만듦.

### Step 1: 한 줄 요약
프로젝트가 뭔지 한 문장으로. 못 쓰면 정리 안 된 거임.
```
예: "한 번 라이브로 일주일치 콘텐츠"
```

### Step 2: 핵심 원칙 3개
절대 안 변하는 것들. 이거 기준으로 기능 판단.
```
예: 원가 보호 / 무료 체험 / 현금 유입
```

### Step 3: 입력 스펙 테이블
필드 | 타입 | 필수 | 제한 | 검증 | 예시
```
예: productName | string | O | 1~100자 | 빈문자열X | '코코넛오일'
```

### Step 4: 출력 JSON
말로 설명 X. 실제 응답 그대로.
```json
{"id": "abc123", "status": "completed", "result": {...}}
```

### Step 5: 에러 테이블
상황 | 코드 | 메시지. SNAKE_CASE 통일.
```
예: 잔액부족 | INSUFFICIENT_CREDITS | '크레딧 부족. 필요: {n}'
```

### Step 6: 상태 머신
복잡한 플로우는 ASCII로.
```
[available] --reserve--> [reserved] --capture--> [done]
```
"""
    return [TextContent(type="text", text=guide)]


async def _get_verify_checklist() -> list[TextContent]:
    checklist = """## PRD 검증 체크리스트

> 빠뜨리면 나중에 다시 짬

### 스펙
- [ ] 입력 제한값 다 있음? (1~100자, 최대 10개 같은 거)
- [ ] enum 옵션표 있음? (tone: friendly|expert|urgent)
- [ ] 출력 JSON 필드 다 나옴? (metadata, createdAt 빠뜨리기 쉬움)

### 에러
- [ ] 에러코드 SNAKE_CASE? (INSUFFICIENT_CREDITS ⭕)
- [ ] 동적 값 들어감? ('필요: {required}, 보유: {available}')

### 돈
- [ ] 무료/유료 구분표? (Free: 미리보기 / Paid: 다운로드)
- [ ] 크레딧 차감 시점? (reserve -> capture -> release)
- [ ] 실패 시 환불? (작업 실패하면 release)

### API
- [ ] /v1/ 붙어있음? (POST /v1/scripts ⭕)
- [ ] 202 맞게 씀? (비동기는 202 + jobId)

### 데이터
- [ ] 보관 기간? (무료 24시간, 유료 7일)
- [ ] 만료 알림? (24시간 전 푸시)
"""
    return [TextContent(type="text", text=checklist)]


async def run_server():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    import asyncio
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
