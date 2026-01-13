"""Mobile-friendly API server with FastAPI."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel as PydanticBaseModel, Field


# Request/Response Models

class AnalyzeCodeRequest(PydanticBaseModel):
    """Request for code analysis."""
    code: str = Field(..., description="Source code to analyze")
    language: str = Field(..., description="Programming language")
    file_path: Optional[str] = Field(None, description="Optional file path")


class ReviewCodeRequest(PydanticBaseModel):
    """Request for code review."""
    code: str = Field(..., description="Source code to review")
    language: str = Field(..., description="Programming language")
    file_path: Optional[str] = Field(None, description="Optional file path")
    context_files: Optional[List[str]] = Field(None, description="Related files")


class GenerateTestsRequest(PydanticBaseModel):
    """Request for test generation."""
    code: str = Field(..., description="Source code to generate tests for")
    language: str = Field(..., description="Programming language")
    test_framework: Optional[str] = Field(None, description="Test framework")


class CompleteCodeRequest(PydanticBaseModel):
    """Request for code completion."""
    code_prefix: str = Field(..., description="Code before cursor")
    code_suffix: str = Field("", description="Code after cursor")
    language: str = Field(..., description="Programming language")
    file_path: Optional[str] = Field(None, description="Optional file path")


class ScanVulnerabilitiesRequest(PydanticBaseModel):
    """Request for vulnerability scanning."""
    code: str = Field(..., description="Source code to scan")
    language: str = Field(..., description="Programming language")


class QueryRequest(PydanticBaseModel):
    """Generic query request."""
    query: str = Field(..., description="Query text")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class HealthResponse(PydanticBaseModel):
    """Health check response."""
    status: str
    model_online: bool
    model_offline: bool
    version: str


class AnalyzeCodeResponse(PydanticBaseModel):
    """Response for code analysis."""
    file_path: str
    language: str
    issues: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    suggestions: List[str]


class ReviewCodeResponse(PydanticBaseModel):
    """Response for code review."""
    file_path: str
    comments: List[Dict[str, Any]]
    overall_score: float
    summary: str


class GenerateTestsResponse(PydanticBaseModel):
    """Response for test generation."""
    test_code: str
    test_cases: List[str]
    coverage_targets: List[str]


class CompleteCodeResponse(PydanticBaseModel):
    """Response for code completion."""
    completion: str


class ScanVulnerabilitiesResponse(PydanticBaseModel):
    """Response for vulnerability scanning."""
    vulnerabilities: List[Dict[str, Any]]


class QueryResponse(PydanticBaseModel):
    """Response for generic query."""
    response: str
    decision: str
    risk_level: str


def create_mobile_api_app():
    """
    Create FastAPI application for mobile access.
    
    This provides a mobile-friendly REST API for AXON capabilities.
    """
    try:
        from fastapi import FastAPI, HTTPException, Depends, Header
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import JSONResponse
    except ImportError:
        print("⚠️  FastAPI not installed. Install with: pip install fastapi uvicorn")
        return None

    from core.orchestrator_factory import create_orchestrator, get_kill_switch
    from intel.code_intelligence import CodeIntelligence
    from models.offline_llama import OfflineLlamaAdapter
    from models.online_api import OnlineAPIAdapter
    from models.router import ModelRouter

    app = FastAPI(
        title="AXON Mobile API",
        description="Mobile-friendly API for AXON AI Brain",
        version="1.0.0",
    )

    # Enable CORS for mobile apps
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize components
    _orchestrator = None
    _code_intelligence = None
    _kill_switch = None

    def get_orchestrator():
        """Get or initialize the orchestrator."""
        global _orchestrator, _code_intelligence, _kill_switch
        
        if _orchestrator is None:
            # Initialize models
            offline_model = OfflineLlamaAdapter()
            online_model = OnlineAPIAdapter(
                provider="openai",
                model_name="gpt-3.5-turbo",
            )
            model_router = ModelRouter(
                offline_model=offline_model,
                online_model=online_model,
            )

            # Use factory to create orchestrator (eliminates duplication)
            _orchestrator = create_orchestrator(model_router)
            
            # Get kill switch reference
            _kill_switch = get_kill_switch()

            # Initialize code intelligence
            worker_model = model_router.select_worker()
            _code_intelligence = CodeIntelligence(worker_model)

        return _orchestrator

    def get_code_intelligence():
        """Get code intelligence engine."""
        if _orchestrator is None:
            get_orchestrator()
        return _code_intelligence

    async def verify_api_key(x_api_key: Optional[str] = Header(None)):
        """Simple API key verification (optional)."""
        # In production, implement proper authentication
        # For now, allow access if AXON_API_KEY is not set
        expected_key = os.environ.get("AXON_API_KEY")
        if expected_key and x_api_key != expected_key:
            raise HTTPException(status_code=401, detail="Invalid API key")
        return True

    # Health check endpoint
    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint."""
        orchestrator = get_orchestrator()
        worker = orchestrator.model_router.select_worker()
        teacher = orchestrator.model_router.select_teacher()
        
        return HealthResponse(
            status="healthy",
            model_online=teacher.health_check() if teacher else False,
            model_offline=worker.health_check(),
            version="1.0.0",
        )

    # Code intelligence endpoints
    @app.post("/api/v1/code/analyze", response_model=AnalyzeCodeResponse)
    async def analyze_code(
        request: AnalyzeCodeRequest,
        _: bool = Depends(verify_api_key),
    ):
        """Analyze code for issues and improvements."""
        try:
            intelligence = get_code_intelligence()
            result = intelligence.analyze_code(
                code=request.code,
                language=request.language,
                file_path=request.file_path or "",
            )
            
            return AnalyzeCodeResponse(
                file_path=result.file_path,
                language=result.language,
                issues=result.issues,
                metrics=result.metrics,
                suggestions=result.suggestions,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/v1/code/review", response_model=ReviewCodeResponse)
    async def review_code(
        request: ReviewCodeRequest,
        _: bool = Depends(verify_api_key),
    ):
        """Review code and provide feedback."""
        try:
            intelligence = get_code_intelligence()
            result = intelligence.review_code(
                code=request.code,
                language=request.language,
                file_path=request.file_path or "",
                context_files=request.context_files,
            )
            
            return ReviewCodeResponse(
                file_path=result.file_path,
                comments=result.comments,
                overall_score=result.overall_score,
                summary=result.summary,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/v1/code/generate-tests", response_model=GenerateTestsResponse)
    async def generate_tests(
        request: GenerateTestsRequest,
        _: bool = Depends(verify_api_key),
    ):
        """Generate test cases for code."""
        try:
            intelligence = get_code_intelligence()
            result = intelligence.generate_tests(
                code=request.code,
                language=request.language,
                test_framework=request.test_framework,
            )
            
            return GenerateTestsResponse(
                test_code=result.test_code,
                test_cases=result.test_cases,
                coverage_targets=result.coverage_targets,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/v1/code/complete", response_model=CompleteCodeResponse)
    async def complete_code(
        request: CompleteCodeRequest,
        _: bool = Depends(verify_api_key),
    ):
        """Complete code at cursor position."""
        try:
            intelligence = get_code_intelligence()
            completion = intelligence.complete_code(
                code_prefix=request.code_prefix,
                code_suffix=request.code_suffix,
                language=request.language,
                file_path=request.file_path or "",
            )
            
            return CompleteCodeResponse(completion=completion)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/v1/code/scan-vulnerabilities", response_model=ScanVulnerabilitiesResponse)
    async def scan_vulnerabilities(
        request: ScanVulnerabilitiesRequest,
        _: bool = Depends(verify_api_key),
    ):
        """Scan code for security vulnerabilities."""
        try:
            intelligence = get_code_intelligence()
            vulnerabilities = intelligence.scan_vulnerabilities(
                code=request.code,
                language=request.language,
            )
            
            return ScanVulnerabilitiesResponse(vulnerabilities=vulnerabilities)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Generic query endpoint
    @app.post("/api/v1/query", response_model=QueryResponse)
    async def query(
        request: QueryRequest,
        _: bool = Depends(verify_api_key),
    ):
        """Process a generic query through AXON."""
        try:
            orchestrator = get_orchestrator()
            decision = orchestrator.execute_pipeline(
                raw_input=request.query,
                source="mobile_api",
                role="developer",
                subject_id="api_user",
            )
            
            return QueryResponse(
                response=decision.response or "",
                decision=decision.decision,
                risk_level=decision.risk_level,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # System info endpoint
    @app.get("/api/v1/info")
    async def system_info():
        """Get system information."""
        orchestrator = get_orchestrator()
        worker = orchestrator.model_router.select_worker()
        teacher = orchestrator.model_router.select_teacher()
        
        worker_info = worker.get_info() if hasattr(worker, "get_info") else {"name": worker.name}
        teacher_info = teacher.get_info() if teacher and hasattr(teacher, "get_info") else None
        
        return {
            "version": "1.0.0",
            "offline_model": worker_info,
            "online_model": teacher_info,
            "kill_switch_engaged": _kill_switch.is_global_engaged() if _kill_switch else False,
            "supported_languages": ["python", "javascript", "typescript", "java", "cpp", "go", "rust"],
        }

    return app


def start_mobile_api_server(host: str = "0.0.0.0", port: int = 8000):
    """
    Start the mobile API server.
    
    Args:
        host: Host to bind to (default: 0.0.0.0 for all interfaces)
        port: Port to bind to (default: 8000)
    """
    try:
        import uvicorn
    except ImportError:
        print("⚠️  uvicorn not installed. Install with: pip install uvicorn")
        return

    app = create_mobile_api_app()
    if app is None:
        print("❌ Failed to create API app")
        return

    print(f"🚀 Starting AXON Mobile API on {host}:{port}")
    print(f"📱 Access from mobile: http://{host}:{port}")
    print(f"📖 API docs: http://{host}:{port}/docs")
    print()
    
    uvicorn.run(app, host=host, port=port)
