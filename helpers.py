from decimal import Decimal

def calculate_delta(base, current):
    if not base or not current: return None
    return ((current - base) / base) * Decimal(100)