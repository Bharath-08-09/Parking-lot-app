from datetime import datetime
from app.core.config import settings

class BillingService:
    def calculate_fee(self, entry_time: datetime, exit_time: datetime) -> float:
        duration_seconds = (exit_time - entry_time).total_seconds()
        hours = max(1, int(duration_seconds // 3600) + (1 if duration_seconds % 3600 else 0))
        fee = hours * settings.DEFAULT_PARKING_RATE_PER_HOUR
        return round(fee, 2)

billing_service = BillingService()