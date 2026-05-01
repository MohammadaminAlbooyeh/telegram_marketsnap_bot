def validate_price(value: str) -> float:
    """Validate and parse price string."""
    try:
        return float(value)
    except (ValueError, TypeError):
        raise ValueError("Invalid price value")


def validate_alert_condition(condition: str) -> str:
    """Validate alert condition."""
    condition = condition.lower()
    if condition not in ("above", "below"):
        raise ValueError("Condition must be 'above' or 'below'")
    return condition
