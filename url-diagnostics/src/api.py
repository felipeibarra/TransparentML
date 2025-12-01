"""
URL Diagnostics API
===================
FastAPI application for URL health analysis and diagnostics.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Dict, List
import asyncio
import json
import uuid
from datetime import datetime
import logging
import os

from url_scraper import URLScraper
from ml_analyzer import URLHealthAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TransparentML URL Diagnostics",
    description="Comprehensive URL health analysis using Machine Learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
scraper = URLScraper()
analyzer = URLHealthAnalyzer()

# In-memory storage for analysis results (use Redis in production)
analysis_cache: Dict[str, Dict] = {}
analysis_logs: Dict[str, List[str]] = {}

# Mount static files
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


# Pydantic models
class URLAnalysisRequest(BaseModel):
    """Request model for URL analysis."""
    url: str = Field(..., description="URL to analyze", example="https://www.google.com")
    analysis_type: str = Field(default="comprehensive", description="Type of analysis: quick, comprehensive, security")
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.example.com",
                "analysis_type": "comprehensive"
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    timestamp: str
    version: str


class AnalysisStatusResponse(BaseModel):
    """Analysis status response."""
    analysis_id: str
    status: str
    progress: int
    message: str


# Routes
@app.get("/dashboard")
async def dashboard():
    """Serve the main dashboard HTML."""
    dashboard_path = os.path.join(static_path, "dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    raise HTTPException(status_code=404, detail="Dashboard not found")


@app.get("/", response_model=Dict)
async def root():
    """Root endpoint - redirects to dashboard."""
    # Check if dashboard exists
    dashboard_path = os.path.join(static_path, "dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    
    # Fallback to API info
    return {
        "service": "TransparentML URL Diagnostics",
        "version": "1.0.0",
        "description": "ML-powered URL health analysis",
        "endpoints": {
            "dashboard": "/dashboard",
            "health": "/health",
            "analyze": "/api/v1/analyze",
            "status": "/api/v1/status/{analysis_id}",
            "results": "/api/v1/results/{analysis_id}",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        service="url-diagnostics",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.post("/api/v1/analyze")
async def analyze_url(request: URLAnalysisRequest, background_tasks: BackgroundTasks):
    """
    Start URL analysis (async).
    
    Returns immediately with analysis_id for tracking progress.
    """
    analysis_id = str(uuid.uuid4())
    
    logger.info(f"Starting analysis {analysis_id} for URL: {request.url}")
    
    # Initialize analysis state
    analysis_cache[analysis_id] = {
        "status": "started",
        "progress": 0,
        "url": request.url,
        "started_at": datetime.now().isoformat()
    }
    analysis_logs[analysis_id] = []
    
    # Start background task
    background_tasks.add_task(
        perform_analysis,
        analysis_id,
        request.url,
        request.analysis_type
    )
    
    return {
        "analysis_id": analysis_id,
        "status": "started",
        "message": "Analysis started. Use /api/v1/status/{analysis_id} to track progress.",
        "url": request.url
    }


@app.post("/api/v1/analyze/sync")
async def analyze_url_sync(request: URLAnalysisRequest):
    """
    Synchronous URL analysis (waits for completion).
    
    Use this for immediate results, but may timeout for slow URLs.
    """
    logger.info(f"Starting synchronous analysis for URL: {request.url}")
    
    try:
        # Step 1: Scrape URL
        log_message(None, "🔍 Fetching URL metrics...")
        metrics = scraper.analyze_url(request.url)
        
        if not metrics.get('success'):
            raise HTTPException(
                status_code=400,
                detail=f"Failed to analyze URL: {metrics.get('error')}"
            )
        
        # Step 2: Extract features
        log_message(None, "🧬 Extracting features for ML analysis...")
        features = scraper.extract_features_for_ml(metrics)
        
        # Step 3: ML Analysis
        log_message(None, "🤖 Running ML analysis...")
        ml_results = analyzer.analyze(features)
        
        # Step 4: Combine results
        result = {
            "url": request.url,
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "load_time": metrics.get('load_time_seconds'),
                "response_size_kb": metrics.get('response_size_kb'),
                "status_code": metrics.get('status_code'),
                "ssl_enabled": metrics.get('ssl_enabled'),
                "mobile_friendly": metrics.get('mobile_friendly'),
            },
            "health_score": ml_results['health_score'],
            "grade": ml_results['grade'],
            "anomalies": ml_results['anomalies'],
            "recommendations": ml_results['recommendations'],
            "feature_analysis": ml_results['feature_analysis']
        }
        
        log_message(None, f"✅ Analysis complete! Score: {ml_results['health_score']}/100")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in synchronous analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/status/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    """Get the status of an ongoing analysis."""
    if analysis_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis ID not found")
    
    return analysis_cache[analysis_id]


@app.get("/api/v1/results/{analysis_id}")
async def get_analysis_results(analysis_id: str):
    """Get the complete results of a finished analysis."""
    if analysis_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis ID not found")
    
    analysis = analysis_cache[analysis_id]
    
    if analysis['status'] != 'completed':
        return {
            "status": analysis['status'],
            "message": "Analysis not yet completed",
            "progress": analysis.get('progress', 0)
        }
    
    return analysis.get('results', {})


@app.get("/api/v1/logs/{analysis_id}")
async def get_analysis_logs(analysis_id: str):
    """Get real-time logs for an analysis (Server-Sent Events)."""
    if analysis_id not in analysis_logs:
        raise HTTPException(status_code=404, detail="Analysis ID not found")
    
    async def event_generator():
        """Generate SSE events for logs."""
        sent_count = 0
        max_wait = 60  # Maximum wait time in seconds
        waited = 0
        
        while waited < max_wait:
            logs = analysis_logs.get(analysis_id, [])
            
            # Send new logs
            while sent_count < len(logs):
                log_entry = logs[sent_count]
                yield f"data: {json.dumps({'log': log_entry, 'index': sent_count})}\n\n"
                sent_count += 1
            
            # Check if analysis is complete
            if analysis_id in analysis_cache:
                status = analysis_cache[analysis_id].get('status')
                if status in ['completed', 'failed']:
                    yield f"data: {json.dumps({'status': status, 'done': True})}\n\n"
                    break
            
            await asyncio.sleep(0.5)
            waited += 0.5
        
        yield "data: {\"done\": true}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


# Background task functions
async def perform_analysis(analysis_id: str, url: str, analysis_type: str):
    """Perform the actual URL analysis in the background."""
    try:
        log_message(analysis_id, f"🚀 Starting {analysis_type} analysis for: {url}")
        analysis_cache[analysis_id]['progress'] = 10
        
        # Step 1: Scrape URL
        log_message(analysis_id, "🔍 Fetching URL metrics...")
        await asyncio.sleep(0.5)  # Simulate some delay
        metrics = scraper.analyze_url(url)
        analysis_cache[analysis_id]['progress'] = 40
        
        if not metrics.get('success'):
            log_message(analysis_id, f"❌ Failed to fetch URL: {metrics.get('error')}")
            analysis_cache[analysis_id]['status'] = 'failed'
            analysis_cache[analysis_id]['error'] = metrics.get('error')
            return
        
        log_message(analysis_id, f"✓ URL fetched successfully (Status: {metrics.get('status_code')})")
        
        # Step 2: Extract features
        log_message(analysis_id, "🧬 Extracting features for ML analysis...")
        await asyncio.sleep(0.3)
        features = scraper.extract_features_for_ml(metrics)
        analysis_cache[analysis_id]['progress'] = 60
        log_message(analysis_id, f"✓ Extracted {len(features)} features")
        
        # Step 3: ML Analysis
        log_message(analysis_id, "🤖 Running ML analysis (Linear Regression + PCA)...")
        await asyncio.sleep(0.3)
        ml_results = analyzer.analyze(features)
        analysis_cache[analysis_id]['progress'] = 80
        log_message(analysis_id, f"✓ Health Score: {ml_results['health_score']}/100 (Grade: {ml_results['grade']})")
        
        # Step 4: Generate recommendations
        log_message(analysis_id, "📋 Generating recommendations...")
        await asyncio.sleep(0.2)
        analysis_cache[analysis_id]['progress'] = 95
        log_message(analysis_id, f"✓ Found {len(ml_results['recommendations'])} recommendations")
        
        # Combine results
        result = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "load_time": metrics.get('load_time_seconds'),
                "response_size_kb": metrics.get('response_size_kb'),
                "status_code": metrics.get('status_code'),
                "ssl_enabled": metrics.get('ssl_enabled'),
                "ssl_days_until_expiry": metrics.get('ssl_days_until_expiry'),
                "mobile_friendly": metrics.get('mobile_friendly'),
                "has_meta_description": metrics.get('has_meta_description'),
                "images_count": metrics.get('images_count'),
                "scripts_count": metrics.get('scripts_count'),
                "compression_enabled": metrics.get('compression_enabled'),
            },
            "health_score": ml_results['health_score'],
            "grade": ml_results['grade'],
            "anomalies": ml_results['anomalies'],
            "recommendations": ml_results['recommendations'],
            "feature_analysis": ml_results['feature_analysis'],
            "raw_metrics": metrics
        }
        
        # Update cache
        analysis_cache[analysis_id].update({
            'status': 'completed',
            'progress': 100,
            'results': result,
            'completed_at': datetime.now().isoformat()
        })
        
        log_message(analysis_id, "✅ Analysis completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in analysis {analysis_id}: {str(e)}")
        log_message(analysis_id, f"❌ Error: {str(e)}")
        analysis_cache[analysis_id].update({
            'status': 'failed',
            'error': str(e)
        })


def log_message(analysis_id: Optional[str], message: str):
    """Add a log message for an analysis."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    
    logger.info(log_entry)
    
    if analysis_id and analysis_id in analysis_logs:
        analysis_logs[analysis_id].append(log_entry)


# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
