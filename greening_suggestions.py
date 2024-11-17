def suggest_greening(temperature, humidity=None, rainfall=None):
    """Suggest greening actions based on temperature, humidity, rainfall."""
    
    try:
        temperature = float(temperature)
        if humidity is not None:
            humidity = float(humidity)
        if rainfall is not None:
            rainfall = float(rainfall)
    except (ValueError, TypeError):
        return f"Error: Unable to process input data."

    suggestion = []

    # Temperature-based suggestion
    if temperature > 30:
        suggestion.append("High heat: Recommend planting trees, vertical gardens, and installing green roofs.")
    elif temperature > 25:
        suggestion.append("Moderate heat: Suggest green walls, bushes, and additional green space.")
    elif temperature <= 25:
        suggestion.append("Low heat: Grass lawns, shrubs, and community gardens would work well.")
    
    # Humidity-based suggestion
    if humidity is not None:
        if humidity > 60:
            suggestion.append("High humidity: Consider moisture-loving plants like ferns and certain shrubs.")
        else:
            suggestion.append("Low humidity: Use drought-resistant plants and succulents.")

    # Rainfall-based suggestion
    if rainfall is not None:
        if rainfall < 500:
            suggestion.append("Low rainfall: Suggest xeriscaping with drought-resistant plants.")
        else:
            suggestion.append("High rainfall: Opt for plants that can handle wet conditions, such as native grasses.")

    return " ".join(suggestion) if suggestion else "Data insufficient for suggestion."
