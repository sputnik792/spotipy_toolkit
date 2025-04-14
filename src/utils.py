from datetime import datetime
import re

def parse_release_date(date_str):
    """Handle YYYY, YYYY-MM, or YYYY-MM-DD formats"""
    parts = date_str.split('-')
    if len(parts) == 1:
        return datetime.strptime(date_str + '-01-01', '%Y-%m-%d')
    elif len(parts) == 2:
        return datetime.strptime(date_str + '-01', '%Y-%m-%d')
    return datetime.strptime(date_str, '%Y-%m-%d')

def extract_artist_from_description(desc):
    """Extract @ArtistName from description"""
    match = re.search(r'#auto-update\s+@([^\n]+)', desc, re.IGNORECASE)
    return match.group(1).strip() if match else None
