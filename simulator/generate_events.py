import requests
import json
import time
import os

API_URL = "http://localhost:8000/rfid/event"
EVENTS_FILE = "data/events.json"

def load_events():
    if not os.path.exists(EVENTS_FILE):
        print(f"Error: {EVENTS_FILE} not found.")
        return []
    
    with open(EVENTS_FILE, "r") as f:
        try:
            data = json.load(f)
            # Handle if the root is a dict with an "events" key (User's new structure)
            if isinstance(data, dict) and "events" in data:
                return data["events"]
            # Handle list of events
            if isinstance(data, list):
                return data
            # Handle single event object
            return [data]
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {EVENTS_FILE}: {e}")
            return []

def simulate_rfid_events():
    print(f"Loading events from {EVENTS_FILE}...")
    events = load_events()
    
    if not events:
        print("No events to simulate. Exiting.")
        return

    while True:
        for event in events:
            try:
                response = requests.post(API_URL, json=event)
                # Check for success
                response.raise_for_status()
                print(f"Sent: {event} → Response: {response.json()}")
            except Exception as e:
                print(f"Error sending event: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    print(f"Response content: {e.response.text}")
            
            time.sleep(2)

if __name__ == "__main__":
    simulate_rfid_events()
