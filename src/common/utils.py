"""
Common utility functions for the satellite tracking system.
Add helper functions that can be reused across the Pi and server components.
"""

def log_message(message, logfile="../../logs/system.log"):
    """
    Simple logger that appends messages to a log file.
    """
    from datetime import datetime
    with open(logfile, "a") as f:
        f.write(f"{datetime.now()}: {message}\n")
