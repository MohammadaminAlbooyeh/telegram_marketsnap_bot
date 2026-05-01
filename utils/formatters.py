def format_price(price: float, currency: str = "USD") -> str:
    """Format price with currency symbol."""
    if currency == "IRR":
        return f"{price:,.0f} IRR"
    return f"${price:,.2f}"


def format_percentage(value: float) -> str:
    """Format percentage with sign."""
    return f"{value:+.2f}%"
