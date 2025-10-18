"""
Biofield validation endpoints for CSN Server
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import structlog
import numpy as np
from datetime import datetime

from csn_server.config import settings

logger = structlog.get_logger()
router = APIRouter()


class HRVData(BaseModel):
    """HRV data model"""
    rr_intervals: List[float] = Field(..., description="R-R intervals in milliseconds")
    sample_rate: int = Field(default=1000, description="Sample rate in Hz")
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class BiofieldValidationRequest(BaseModel):
    """Biofield validation request"""
    hrv_data: HRVData
    validation_type: str = Field(default="comprehensive", description="Type of validation")
    parameters: Optional[Dict[str, Any]] = None


class ValidationResult(BaseModel):
    """Validation result model"""
    is_valid: bool
    confidence_score: float
    validation_metrics: Dict[str, Any]
    recommendations: List[str]
    timestamp: datetime


class HRVAnalysis(BaseModel):
    """HRV analysis results"""
    time_domain: Dict[str, float]
    frequency_domain: Dict[str, float]
    nonlinear: Dict[str, float]
    quality_metrics: Dict[str, Any]


# Mock HRV analysis functions (replace with actual pyhrv implementation)
def calculate_time_domain_metrics(rr_intervals: List[float]) -> Dict[str, float]:
    """Calculate time domain HRV metrics"""
    rr_array = np.array(rr_intervals)
    
    # Basic statistics
    mean_rr = np.mean(rr_array)
    std_rr = np.std(rr_array)
    
    # RMSSD (Root Mean Square of Successive Differences)
    rmssd = np.sqrt(np.mean(np.diff(rr_array) ** 2))
    
    # pNN50 (Percentage of successive RR intervals that differ by more than 50ms)
    nn50 = np.sum(np.abs(np.diff(rr_array)) > 50)
    pnn50 = (nn50 / len(rr_array)) * 100 if len(rr_array) > 0 else 0
    
    return {
        "mean_rr": float(mean_rr),
        "std_rr": float(std_rr),
        "rmssd": float(rmssd),
        "pnn50": float(pnn50),
        "nn50": int(nn50)
    }


def calculate_frequency_domain_metrics(rr_intervals: List[float], sample_rate: int) -> Dict[str, float]:
    """Calculate frequency domain HRV metrics"""
    # This is a simplified implementation
    # In a real implementation, you would use proper FFT and power spectral density analysis
    
    rr_array = np.array(rr_intervals)
    
    # Mock frequency domain calculations
    # In reality, you would:
    # 1. Interpolate RR intervals to regular time series
    # 2. Apply FFT
    # 3. Calculate power in different frequency bands
    
    total_power = np.var(rr_array) * 1000  # Mock total power
    
    # Mock frequency band powers (these should be calculated from actual FFT)
    vlf_power = total_power * 0.1  # Very Low Frequency (0.003-0.04 Hz)
    lf_power = total_power * 0.3   # Low Frequency (0.04-0.15 Hz)
    hf_power = total_power * 0.4   # High Frequency (0.15-0.4 Hz)
    vhf_power = total_power * 0.2  # Very High Frequency (0.4-0.5 Hz)
    
    # LF/HF ratio
    lf_hf_ratio = lf_power / hf_power if hf_power > 0 else 0
    
    return {
        "total_power": float(total_power),
        "vlf_power": float(vlf_power),
        "lf_power": float(lf_power),
        "hf_power": float(hf_power),
        "vhf_power": float(vhf_power),
        "lf_hf_ratio": float(lf_hf_ratio)
    }


def calculate_nonlinear_metrics(rr_intervals: List[float]) -> Dict[str, float]:
    """Calculate nonlinear HRV metrics"""
    # This is a simplified implementation
    # In a real implementation, you would calculate:
    # - SD1, SD2 (Poincaré plot)
    # - Approximate entropy
    # - Sample entropy
    # - DFA (Detrended Fluctuation Analysis)
    
    rr_array = np.array(rr_intervals)
    
    # Mock nonlinear metrics
    sd1 = np.std(rr_array) * 0.5  # Mock SD1
    sd2 = np.std(rr_array) * 1.5  # Mock SD2
    
    return {
        "sd1": float(sd1),
        "sd2": float(sd2),
        "sd1_sd2_ratio": float(sd1 / sd2) if sd2 > 0 else 0
    }


def assess_data_quality(rr_intervals: List[float], sample_rate: int) -> Dict[str, Any]:
    """Assess the quality of HRV data"""
    rr_array = np.array(rr_intervals)
    
    # Basic quality checks
    min_segment_length = settings.hrv_min_segment_length
    max_segment_length = settings.hrv_max_segment_length
    
    segment_length = len(rr_array)
    duration_minutes = segment_length / (sample_rate / 1000) / 60
    
    # Check for reasonable RR intervals (200-2000ms)
    valid_intervals = np.sum((rr_array >= 200) & (rr_array <= 2000))
    quality_percentage = (valid_intervals / len(rr_array)) * 100 if len(rr_array) > 0 else 0
    
    # Check for artifacts (sudden large changes)
    rr_diff = np.abs(np.diff(rr_array))
    artifact_threshold = 200  # ms
    artifacts = np.sum(rr_diff > artifact_threshold)
    artifact_percentage = (artifacts / len(rr_diff)) * 100 if len(rr_diff) > 0 else 0
    
    return {
        "segment_length": segment_length,
        "duration_minutes": float(duration_minutes),
        "quality_percentage": float(quality_percentage),
        "artifact_percentage": float(artifact_percentage),
        "is_sufficient_length": segment_length >= min_segment_length,
        "is_within_limits": segment_length <= max_segment_length,
        "quality_score": float(quality_percentage - artifact_percentage)
    }


def validate_biofield_data(hrv_data: HRVData, validation_type: str = "comprehensive") -> ValidationResult:
    """Validate biofield data using HRV analysis"""
    try:
        rr_intervals = hrv_data.rr_intervals
        sample_rate = hrv_data.sample_rate
        
        # Assess data quality
        quality_metrics = assess_data_quality(rr_intervals, sample_rate)
        
        # Calculate HRV metrics
        time_domain = calculate_time_domain_metrics(rr_intervals)
        frequency_domain = calculate_frequency_domain_metrics(rr_intervals, sample_rate)
        nonlinear = calculate_nonlinear_metrics(rr_intervals)
        
        # Determine validation result
        is_valid = True
        confidence_score = 0.0
        recommendations = []
        
        # Quality checks
        if quality_metrics["quality_percentage"] < 80:
            is_valid = False
            recommendations.append("Data quality is below 80%. Consider re-recording.")
        
        if quality_metrics["artifact_percentage"] > 10:
            is_valid = False
            recommendations.append("High artifact percentage detected. Clean data before analysis.")
        
        if not quality_metrics["is_sufficient_length"]:
            is_valid = False
            recommendations.append(f"Segment length ({quality_metrics['segment_length']}) is below minimum ({settings.hrv_min_segment_length}).")
        
        # HRV metric validation
        if time_domain["rmssd"] < 10:
            recommendations.append("Low RMSSD detected. This may indicate reduced parasympathetic activity.")
        
        if frequency_domain["lf_hf_ratio"] > 2.0:
            recommendations.append("High LF/HF ratio detected. This may indicate sympathetic dominance.")
        
        # Calculate confidence score
        quality_score = quality_metrics["quality_score"]
        hrv_score = min(100, max(0, (time_domain["rmssd"] / 100) * 50 + (frequency_domain["hf_power"] / 1000) * 50))
        confidence_score = (quality_score + hrv_score) / 2
        
        # Additional validation based on type
        if validation_type == "comprehensive":
            # Additional checks for comprehensive validation
            if frequency_domain["total_power"] < 100:
                recommendations.append("Low total power detected. Consider longer recording period.")
        
        elif validation_type == "basic":
            # Simplified validation for basic checks
            confidence_score = quality_score
        
        return ValidationResult(
            is_valid=is_valid,
            confidence_score=confidence_score,
            validation_metrics={
                "time_domain": time_domain,
                "frequency_domain": frequency_domain,
                "nonlinear": nonlinear,
                "quality": quality_metrics
            },
            recommendations=recommendations,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Biofield validation failed", error=str(e))
        return ValidationResult(
            is_valid=False,
            confidence_score=0.0,
            validation_metrics={},
            recommendations=[f"Validation error: {str(e)}"],
            timestamp=datetime.now()
        )


@router.post("/validate")
async def validate_biofield(request: BiofieldValidationRequest) -> Dict[str, Any]:
    """Validate biofield data using HRV analysis"""
    try:
        if not settings.hrv_validation_enabled:
            raise HTTPException(status_code=503, detail="HRV validation is disabled")
        
        # Validate input data
        if not request.hrv_data.rr_intervals:
            raise HTTPException(status_code=400, detail="RR intervals data is required")
        
        if len(request.hrv_data.rr_intervals) < settings.hrv_min_segment_length:
            raise HTTPException(
                status_code=400, 
                detail=f"RR intervals data must have at least {settings.hrv_min_segment_length} samples"
            )
        
        # Perform validation
        result = validate_biofield_data(request.hrv_data, request.validation_type)
        
        logger.info("Biofield validation completed", 
                   is_valid=result.is_valid,
                   confidence_score=result.confidence_score,
                   validation_type=request.validation_type)
        
        return {
            "validation_result": result.dict(),
            "hrv_data_info": {
                "sample_count": len(request.hrv_data.rr_intervals),
                "sample_rate": request.hrv_data.sample_rate,
                "duration_minutes": len(request.hrv_data.rr_intervals) / (request.hrv_data.sample_rate / 1000) / 60
            }
        }
        
    except Exception as e:
        logger.error("Biofield validation request failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@router.post("/analyze")
async def analyze_hrv(hrv_data: HRVData) -> Dict[str, Any]:
    """Perform comprehensive HRV analysis"""
    try:
        if not settings.hrv_validation_enabled:
            raise HTTPException(status_code=503, detail="HRV analysis is disabled")
        
        # Validate input
        if not hrv_data.rr_intervals:
            raise HTTPException(status_code=400, detail="RR intervals data is required")
        
        # Calculate all metrics
        time_domain = calculate_time_domain_metrics(hrv_data.rr_intervals)
        frequency_domain = calculate_frequency_domain_metrics(hrv_data.rr_intervals, hrv_data.sample_rate)
        nonlinear = calculate_nonlinear_metrics(hrv_data.rr_intervals)
        quality_metrics = assess_data_quality(hrv_data.rr_intervals, hrv_data.sample_rate)
        
        analysis = HRVAnalysis(
            time_domain=time_domain,
            frequency_domain=frequency_domain,
            nonlinear=nonlinear,
            quality_metrics=quality_metrics
        )
        
        logger.info("HRV analysis completed", 
                   sample_count=len(hrv_data.rr_intervals),
                   quality_score=quality_metrics["quality_score"])
        
        return {
            "analysis": analysis.dict(),
            "metadata": {
                "sample_count": len(hrv_data.rr_intervals),
                "sample_rate": hrv_data.sample_rate,
                "timestamp": hrv_data.timestamp.isoformat() if hrv_data.timestamp else None
            }
        }
        
    except Exception as e:
        logger.error("HRV analysis failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/metrics")
async def get_hrv_metrics() -> Dict[str, Any]:
    """Get available HRV metrics and their descriptions"""
    return {
        "time_domain_metrics": {
            "mean_rr": "Mean R-R interval (ms)",
            "std_rr": "Standard deviation of R-R intervals (ms)",
            "rmssd": "Root Mean Square of Successive Differences (ms)",
            "pnn50": "Percentage of successive RR intervals that differ by more than 50ms (%)",
            "nn50": "Number of successive RR intervals that differ by more than 50ms"
        },
        "frequency_domain_metrics": {
            "total_power": "Total power (ms²)",
            "vlf_power": "Very Low Frequency power (0.003-0.04 Hz) (ms²)",
            "lf_power": "Low Frequency power (0.04-0.15 Hz) (ms²)",
            "hf_power": "High Frequency power (0.15-0.4 Hz) (ms²)",
            "vhf_power": "Very High Frequency power (0.4-0.5 Hz) (ms²)",
            "lf_hf_ratio": "Low Frequency to High Frequency ratio"
        },
        "nonlinear_metrics": {
            "sd1": "SD1 (Poincaré plot short-term variability) (ms)",
            "sd2": "SD2 (Poincaré plot long-term variability) (ms)",
            "sd1_sd2_ratio": "SD1/SD2 ratio"
        },
        "quality_metrics": {
            "quality_percentage": "Percentage of valid RR intervals (%)",
            "artifact_percentage": "Percentage of artifacts detected (%)",
            "quality_score": "Overall quality score (0-100)"
        }
    }


@router.get("/config")
async def get_hrv_config() -> Dict[str, Any]:
    """Get HRV validation configuration"""
    return {
        "enabled": settings.hrv_validation_enabled,
        "sample_rate": settings.hrv_sample_rate,
        "min_segment_length": settings.hrv_min_segment_length,
        "max_segment_length": settings.hrv_max_segment_length,
        "frequency_bands": settings.hrv_frequency_bands
    }


@router.get("/status")
async def biofield_validation_status() -> Dict[str, Any]:
    """Get biofield validation service status"""
    try:
        return {
            "status": "running" if settings.hrv_validation_enabled else "disabled",
            "enabled": settings.hrv_validation_enabled,
            "sample_rate": settings.hrv_sample_rate,
            "min_segment_length": settings.hrv_min_segment_length,
            "max_segment_length": settings.hrv_max_segment_length,
            "frequency_bands": settings.hrv_frequency_bands
        }
    except Exception as e:
        logger.error("Biofield validation status check failed", error=str(e))
        return {
            "status": "error",
            "error": str(e)
        } 