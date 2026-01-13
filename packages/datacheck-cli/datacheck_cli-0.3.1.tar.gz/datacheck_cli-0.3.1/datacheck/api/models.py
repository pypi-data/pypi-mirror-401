"""Pydantic models for DataCheck API.

Defines request/response schemas for the REST API.
"""

from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime
from enum import Enum


class ValidationStatus(str, Enum):
    """Validation status enum."""

    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    UNKNOWN = "unknown"


class AlertSeverity(str, Enum):
    """Alert severity enum."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class RuleResult(BaseModel):
    """Result of a single validation rule."""

    id: int
    rule_name: str
    rule_type: str | None = None
    column_name: str | None = None
    status: ValidationStatus
    passed_rows: int = 0
    failed_rows: int = 0
    error_message: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class ValidationResult(BaseModel):
    """Complete validation result."""

    id: int
    filename: str
    source: str | None = None
    status: ValidationStatus
    pass_rate: float | None = None
    quality_score: float | None = None
    total_rows: int | None = None
    total_columns: int | None = None
    rules_run: int | None = None
    rules_passed: int | None = None
    rules_failed: int | None = None
    timestamp: datetime
    duration_seconds: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ValidationDetail(BaseModel):
    """Detailed validation result with rules."""

    id: int
    filename: str
    source: str | None = None
    status: ValidationStatus
    pass_rate: float | None = None
    quality_score: float | None = None
    total_rows: int | None = None
    total_columns: int | None = None
    rules_run: int | None = None
    rules_passed: int | None = None
    rules_failed: int | None = None
    timestamp: datetime
    duration_seconds: float | None = None
    rules: list[RuleResult] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ValidationSummary(BaseModel):
    """Summary of validation statistics."""

    total_checks: int = 0
    pass_rate: float = 0.0
    quality_score: str = "Unknown"
    passed: int = 0
    failed: int = 0
    total_rows_checked: int = 0


class TrendData(BaseModel):
    """Trend data point."""

    period: str
    pass_rate: float
    count: int
    avg_quality: float | None = None


class TopIssue(BaseModel):
    """Common validation issue."""

    rule_name: str
    rule_type: str | None = None
    column_name: str | None = None
    failure_count: int
    avg_failed_rows: float


class Alert(BaseModel):
    """Alert record."""

    id: int
    validation_id: int | None = None
    severity: AlertSeverity
    title: str
    message: str
    source: str | None = None
    timestamp: datetime
    acknowledged: bool = False
    acknowledged_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AlertCreate(BaseModel):
    """Schema for creating an alert."""

    validation_id: int | None = None
    severity: AlertSeverity = AlertSeverity.INFO
    title: str
    message: str
    source: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ValidationCreate(BaseModel):
    """Schema for creating a validation record."""

    filename: str
    source: str | None = None
    status: ValidationStatus
    pass_rate: float | None = None
    quality_score: float | None = None
    total_rows: int | None = None
    total_columns: int | None = None
    rules_run: int | None = None
    rules_passed: int | None = None
    rules_failed: int | None = None
    duration_seconds: float | None = None
    config_hash: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class RuleResultCreate(BaseModel):
    """Schema for creating a rule result."""

    validation_id: int
    rule_name: str
    rule_type: str | None = None
    column_name: str | None = None
    status: ValidationStatus
    passed_rows: int = 0
    failed_rows: int = 0
    error_message: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class MetricCreate(BaseModel):
    """Schema for creating a metric."""

    name: str
    value: float
    source: str | None = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    database: str


class APIInfo(BaseModel):
    """API information response."""

    name: str
    version: str
    status: str
    endpoints: list[str]
