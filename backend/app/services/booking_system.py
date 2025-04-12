def process_booking(prompt: str, confirmation: str = None) -> str:
    """
    Process booking requests.

    Parameters:
        prompt (str): The original user prompt.
        confirmation (str, optional): The user's confirmation response. 
                                      If None, the function returns a confirmation question.

    Returns:
        str: The response message after processing the booking.
    """
    # If no confirmation is provided, assume this is the first step.
    if confirmation is None:
        return "Do you want to confirm this booking? Options: yes or no."
    else:
        # Process the confirmation response.
        if confirmation.lower() == "yes":
            return "Booking confirmed."
        elif confirmation.lower() == "no":
            return "Booking cancelled."
        else:
            return "Invalid response. Please reply with 'yes' or 'no'."