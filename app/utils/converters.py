def usd_to_irr(usd_amount: float, rate: float) -> float:
    """Convert USD amount to IRR."""
    return usd_amount * rate


def irr_to_usd(irr_amount: float, rate: float) -> float:
    """Convert IRR amount to USD."""
    return irr_amount / rate if rate else 0
