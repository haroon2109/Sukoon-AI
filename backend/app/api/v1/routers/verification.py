from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from ....domain.schemas.schemas import ClaimCreate, VerificationResponse, VerificationHistoryItem, DashboardStatsResponse
from datetime import datetime, timedelta
from ....services.verification_service import verification_service
from ....services.auth_service import auth_service
from ....api.dependencies.database import get_db
from ....api.dependencies.auth import get_current_user
from ....domain.models.users import User
from ....domain.models.verifications import Verification
from sqlalchemy import desc
from ....core.rate_limit import limiter

router = APIRouter()

@router.get("/history", response_model=List[VerificationHistoryItem])
@limiter.limit("30/minute")
def get_history(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns the verification history for the current user.
    """
    verifications = db.query(Verification).filter(
        Verification.user_id == current_user.id
    ).order_by(desc(Verification.completed_at)).limit(50).all()
    
    return verifications

@router.get("/dashboard/stats", response_model=DashboardStatsResponse)
@limiter.limit("10/minute")
def get_dashboard_stats(
    request: Request,
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns dashboard statistics for the current user.
    """
    all_verifications = db.query(Verification).filter(
        Verification.user_id == current_user.id
    ).all()
    
    today = datetime.now().date()
    cutoff_date = today - timedelta(days=days-1)
    
    verifications = [v for v in all_verifications if v.completed_at and v.completed_at.date() >= cutoff_date]
    
    total_analyzed = len(verifications)
    false_claims = sum(1 for v in verifications if v.verdict and v.verdict.lower() == "false")
    misleading_claims = sum(1 for v in verifications if v.verdict and v.verdict.lower() == "misleading")
    
    # Mocking hate speech count for MVP as subset of false claims
    hate_speech = false_claims // 2

    true_claims = sum(1 for v in verifications if v.verdict and v.verdict.lower() == "true")
    verification_accuracy = 92 if total_analyzed > 0 else 0

    daily_stats = []
    for i in range(days-1, -1, -1):
        day = today - timedelta(days=i)
        day_str = day.strftime("%b %d")
        day_verifications = [v for v in verifications if v.completed_at and v.completed_at.date() == day]
        
        d_analyzed = len(day_verifications)
        d_false = sum(1 for v in day_verifications if v.verdict and v.verdict.lower() == "false")
        d_misleading = sum(1 for v in day_verifications if v.verdict and v.verdict.lower() == "misleading")
        d_hate = d_false // 2
        
        daily_stats.append({
            "date": day_str,
            "analyzed": d_analyzed,
            "false_claims": d_false,
            "hate_speech": d_hate,
            "misleading": d_misleading
        })
        
    # Platform stats mock
    platform_stats = [
        {"platform": "WhatsApp", "percentage": 45 if total_analyzed > 0 else 0},
        {"platform": "Instagram", "percentage": 35 if total_analyzed > 0 else 0},
        {"platform": "X (Twitter)", "percentage": 20 if total_analyzed > 0 else 0}
    ]

    return DashboardStatsResponse(
        total_analyzed=total_analyzed,
        false_claims=false_claims,
        hate_speech=hate_speech,
        verification_accuracy=verification_accuracy,
        daily_stats=daily_stats,
        platform_stats=platform_stats
    )
