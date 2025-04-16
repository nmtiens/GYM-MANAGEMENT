from datetime import datetime, timedelta
from threading import Thread
import time
from database import the_hoi_vien_collection
import logging

def decrease_remaining_days():
    while True:
        try:
            # Calculate time until next midnight (12 AM)
            now = datetime.now()
            tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            seconds_until_midnight = (tomorrow - now).total_seconds()
            
            # Sleep until midnight
            time.sleep(seconds_until_midnight)
            
            # Decrease SoNgayConLai by 1 for all users
            the_hoi_vien_collection.update_many(
                {},  # Update all users regardless of current SoNgayConLai value
                {"$inc": {"SoNgayConLai": -1}}
            )
            logging.info(f"Decreased SoNgayConLai by 1 for all users at {datetime.now()}")
        except Exception as e:
            logging.error(f"Error updating SoNgayConLai: {str(e)}")
            # If an error occurs, wait a bit before retrying
            time.sleep(60)

def start_reset_thread():
    decrease_thread = Thread(target=decrease_remaining_days, daemon=True)
    decrease_thread.start()