import re
from datetime import datetime, timedelta

def clean_html(text):
    """
    Clean HTML tags from text and remove extra whitespace.
    """
    cleaned_text = re.sub('<.*?>', '', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()

def parse_custom_date(date_string):
    """
    Parse custom date format and adjust for Martinique timezone (UTC-4).

    Args:
    date_string (str): A string representing a date in the format "Day, DD Mon YYYY HH:MM:SS +/-HHMM".

    Returns:
    str: A string representing the parsed and adjusted date-time, or None if parsing fails.
    """
    if not date_string:
        return None
    
    pattern = r"([A-Za-z]{3}),\s(\d{1,2})\s([A-Za-z]{3})\s(\d{4})\s(\d{2}):(\d{2}):(\d{2})\s([+-]\d{4})"
    match = re.match(pattern, date_string)
    
    if not match:
        return None
    
    day_of_week, day, month, year, hour, minute, second, offset = match.groups()
    
    # Convert month abbreviation to number
    month_num = datetime.strptime(month, '%b').month
    
    # Parse the original datetime
    original_dt = datetime(int(year), month_num, int(day), int(hour), int(minute), int(second))
    
    # Calculate the offset
    offset_hours = int(offset[1:3])
    offset_minutes = int(offset[3:])
    offset_delta = timedelta(hours=offset_hours, minutes=offset_minutes)
    if offset[0] == '-':
        offset_delta = -offset_delta
    
    # Adjust to Martinique time (UTC-4)
    martinique_offset = timedelta(hours=-4)
    adjusted_dt = original_dt - offset_delta + martinique_offset
    
    # Format the result
    return adjusted_dt.strftime('%Y-%m-%d-%H-%M-%S')

def extract_full_name(sender):
    """
    Extract and format the full name from an email sender string.
    """
    full_name = re.match(r'^[^@]+', sender)
    if full_name:
        full_name = full_name.group(0).replace('.', ' ').title()
        return full_name
    return None

def clean_subject(subject):
    """
    Clean and decode email subject lines.
    """
    subject = re.sub(r'=\?iso-8859-1\?Q\?', ' ', subject)
    subject = subject.replace('_', ' ')
    subject = subject.replace('=E9', 'é').replace('C3A9', 'é').replace('C3A0', 'à')
    subject = re.sub(r'[?=]', '', subject)
    subject = re.sub(r'\r\n', ' ', subject)
    subject = re.sub(r'\s+', ' ', subject)
    return subject.strip()

def extract_name(full_name):
    """
    Extract first name and last name from a full name string.
    """
    parts = full_name.split()
    if len(parts) >= 2:
        return {'prenom': parts[0], 'nom': ' '.join(parts[1:])}
    else:
        return {'prenom': full_name, 'nom': None}

def extract_timezone(date_string):
    """
    Extract timezone information from a date string.
    """
    tz = re.search(r'[+-]\d{4}$', date_string)
    return tz.group(0) if tz else "Unknown"