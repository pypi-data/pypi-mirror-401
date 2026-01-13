"""FastAPI application for DataCheck dashboard.

Provides REST API endpoints for monitoring data quality.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import os

from datacheck import __version__
from datacheck.api.database import Database
from datacheck.api.models import (
    ValidationSummary,
    ValidationDetail,
    ValidationResult,
    RuleResult,
    TrendData,
    TopIssue,
    Alert,
    AlertCreate,
    ValidationCreate,
    RuleResultCreate,
    MetricCreate,
    HealthResponse,
    APIInfo,
    ValidationStatus,
)


def create_app(db_path: str = None) -> FastAPI:
    """Create FastAPI application.

    Args:
        db_path: Path to database file

    Returns:
        FastAPI application instance
    """
    # Database instance
    db_file = db_path or os.environ.get("DATACHECK_DB", "datacheck.db")
    db = Database(db_file)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Application lifespan handler."""
        # Startup
        db.initialize()
        yield
        # Shutdown
        db.close()

    app = FastAPI(
        title="DataCheck API",
        description="REST API for DataCheck data quality monitoring dashboard",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def get_db():
        """Dependency to get database instance."""
        return db

    # Root endpoint
    @app.get("/", response_model=APIInfo)
    async def root():
        """API root endpoint."""
        return APIInfo(
            name="DataCheck API",
            version=__version__,
            status="running",
            endpoints=[
                "/health",
                "/api/validations",
                "/api/validations/{id}",
                "/api/validations/summary",
                "/api/validations/trends",
                "/api/validations/top-issues",
                "/api/alerts",
            ],
        )

    # Health check
    @app.get("/health", response_model=HealthResponse)
    async def health_check(database: Database = Depends(get_db)):
        """Health check endpoint."""
        try:
            # Test database connection
            database.query("SELECT 1")
            db_status = "connected"
        except Exception:
            db_status = "disconnected"

        return HealthResponse(
            status="healthy" if db_status == "connected" else "degraded",
            version=__version__,
            database=db_status,
        )

    # Validation endpoints
    @app.get("/api/validations", response_model=list[ValidationResult])
    async def list_validations(
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        status: ValidationStatus | None = None,
        database: Database = Depends(get_db),
    ):
        """List recent validations."""
        try:
            validations = database.get_recent_validations(limit=limit + offset)

            # Apply offset
            validations = validations[offset:offset + limit]

            # Filter by status if provided
            if status:
                validations = [v for v in validations if v.get("status") == status.value]

            return [
                ValidationResult(
                    id=v["id"],
                    filename=v["filename"],
                    source=v.get("source"),
                    status=ValidationStatus(v["status"]),
                    pass_rate=v.get("pass_rate"),
                    quality_score=v.get("quality_score"),
                    total_rows=v.get("total_rows"),
                    total_columns=v.get("total_columns"),
                    rules_run=v.get("rules_run"),
                    rules_passed=v.get("rules_passed"),
                    rules_failed=v.get("rules_failed"),
                    timestamp=v["timestamp"],
                    duration_seconds=v.get("duration_seconds"),
                )
                for v in validations
            ]

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/validations/summary", response_model=ValidationSummary)
    async def get_validation_summary(
        hours: int = Query(24, ge=1, le=720),
        database: Database = Depends(get_db),
    ):
        """Get validation summary for last N hours."""
        try:
            since = datetime.utcnow() - timedelta(hours=hours)
            result = database.get_validation_summary(since=since)

            quality_label = _get_quality_label(result.get("avg_quality"))

            return ValidationSummary(
                total_checks=result.get("total_checks", 0) or 0,
                pass_rate=round(result.get("pass_rate", 0) or 0, 1),
                quality_score=quality_label,
                passed=result.get("passed", 0) or 0,
                failed=result.get("failed", 0) or 0,
                total_rows_checked=result.get("total_rows_checked", 0) or 0,
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/validations/trends", response_model=list[TrendData])
    async def get_validation_trends(
        hours: int = Query(24, ge=1, le=720),
        group_by: str = Query("hour", pattern="^(hour|day|week)$"),
        database: Database = Depends(get_db),
    ):
        """Get validation pass rate trends over time."""
        try:
            since = datetime.utcnow() - timedelta(hours=hours)
            results = database.get_trends(since=since, group_by=group_by)

            return [
                TrendData(
                    period=r["period"],
                    pass_rate=round(r["pass_rate"] or 0, 1),
                    count=r["count"],
                    avg_quality=r.get("avg_quality"),
                )
                for r in results
            ]

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/validations/top-issues", response_model=list[TopIssue])
    async def get_top_issues(
        limit: int = Query(10, ge=1, le=50),
        database: Database = Depends(get_db),
    ):
        """Get most common validation failures."""
        try:
            results = database.get_top_issues(limit=limit)

            return [
                TopIssue(
                    rule_name=r["rule_name"],
                    rule_type=r.get("rule_type"),
                    column_name=r.get("column_name"),
                    failure_count=r["failure_count"],
                    avg_failed_rows=r["avg_failed_rows"] or 0,
                )
                for r in results
            ]

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/validations/{validation_id}", response_model=ValidationDetail)
    async def get_validation_detail(
        validation_id: int,
        database: Database = Depends(get_db),
    ):
        """Get detailed validation results."""
        try:
            validation = database.get_validation(validation_id)

            if not validation:
                raise HTTPException(status_code=404, detail="Validation not found")

            rules = database.get_validation_rules(validation_id)

            return ValidationDetail(
                id=validation["id"],
                filename=validation["filename"],
                source=validation.get("source"),
                status=ValidationStatus(validation["status"]),
                pass_rate=validation.get("pass_rate"),
                quality_score=validation.get("quality_score"),
                total_rows=validation.get("total_rows"),
                total_columns=validation.get("total_columns"),
                rules_run=validation.get("rules_run"),
                rules_passed=validation.get("rules_passed"),
                rules_failed=validation.get("rules_failed"),
                timestamp=validation["timestamp"],
                duration_seconds=validation.get("duration_seconds"),
                rules=[
                    RuleResult(
                        id=r["id"],
                        rule_name=r["rule_name"],
                        rule_type=r.get("rule_type"),
                        column_name=r.get("column_name"),
                        status=ValidationStatus(r["status"]),
                        passed_rows=r.get("passed_rows", 0),
                        failed_rows=r.get("failed_rows", 0),
                        error_message=r.get("error_message"),
                    )
                    for r in rules
                ],
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/validations", response_model=ValidationResult)
    async def create_validation(
        validation: ValidationCreate,
        database: Database = Depends(get_db),
    ):
        """Create a new validation record."""
        try:
            validation_id = database.insert_validation(validation.model_dump())

            return ValidationResult(
                id=validation_id,
                filename=validation.filename,
                source=validation.source,
                status=validation.status,
                pass_rate=validation.pass_rate,
                quality_score=validation.quality_score,
                total_rows=validation.total_rows,
                total_columns=validation.total_columns,
                rules_run=validation.rules_run,
                rules_passed=validation.rules_passed,
                rules_failed=validation.rules_failed,
                timestamp=datetime.utcnow(),
                duration_seconds=validation.duration_seconds,
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/validations/{validation_id}/rules", response_model=RuleResult)
    async def create_rule_result(
        validation_id: int,
        rule: RuleResultCreate,
        database: Database = Depends(get_db),
    ):
        """Create a rule result for a validation."""
        try:
            # Verify validation exists
            validation = database.get_validation(validation_id)
            if not validation:
                raise HTTPException(status_code=404, detail="Validation not found")

            rule_data = rule.model_dump()
            rule_data["validation_id"] = validation_id
            rule_id = database.insert_rule_result(rule_data)

            return RuleResult(
                id=rule_id,
                rule_name=rule.rule_name,
                rule_type=rule.rule_type,
                column_name=rule.column_name,
                status=rule.status,
                passed_rows=rule.passed_rows,
                failed_rows=rule.failed_rows,
                error_message=rule.error_message,
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Alert endpoints
    @app.get("/api/alerts", response_model=list[Alert])
    async def list_alerts(
        hours: int = Query(24, ge=1, le=720),
        unacknowledged_only: bool = Query(False),
        limit: int = Query(50, ge=1, le=200),
        database: Database = Depends(get_db),
    ):
        """List alerts."""
        try:
            since = datetime.utcnow() - timedelta(hours=hours)
            results = database.get_alerts(
                since=since,
                unacknowledged_only=unacknowledged_only,
                limit=limit,
            )

            return [
                Alert(
                    id=r["id"],
                    validation_id=r.get("validation_id"),
                    severity=r["severity"],
                    title=r["title"],
                    message=r["message"],
                    source=r.get("source"),
                    timestamp=r["timestamp"],
                    acknowledged=bool(r.get("acknowledged")),
                    acknowledged_at=r.get("acknowledged_at"),
                )
                for r in results
            ]

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/alerts", response_model=Alert)
    async def create_alert(
        alert: AlertCreate,
        database: Database = Depends(get_db),
    ):
        """Create a new alert."""
        try:
            alert_id = database.insert_alert(alert.model_dump())

            return Alert(
                id=alert_id,
                validation_id=alert.validation_id,
                severity=alert.severity,
                title=alert.title,
                message=alert.message,
                source=alert.source,
                timestamp=datetime.utcnow(),
                acknowledged=False,
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/alerts/{alert_id}/acknowledge")
    async def acknowledge_alert(
        alert_id: int,
        database: Database = Depends(get_db),
    ):
        """Acknowledge an alert."""
        try:
            success = database.acknowledge_alert(alert_id)

            if not success:
                raise HTTPException(status_code=404, detail="Alert not found")

            return {"status": "acknowledged", "alert_id": alert_id}

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Metrics endpoints
    @app.post("/api/metrics")
    async def create_metric(
        metric: MetricCreate,
        database: Database = Depends(get_db),
    ):
        """Record a metric."""
        try:
            metric_id = database.insert_metric(
                name=metric.name,
                value=metric.value,
                source=metric.source,
            )

            return {"status": "created", "metric_id": metric_id}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app


def _get_quality_label(score: float | None) -> str:
    """Convert quality score to label."""
    if score is None:
        return "Unknown"
    elif score >= 95:
        return "Excellent"
    elif score >= 85:
        return "Good"
    elif score >= 70:
        return "Fair"
    else:
        return "Poor"


# Default app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
