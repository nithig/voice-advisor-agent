from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import time

# --- INTERNAL DATABASE (Simulation) ---
# This mimics a NoSQL structure. In a real app, this would be your MongoDB.
MOCK_ORDER_DB = {
    "4120": {
        "status": "shipped",
        "eta": "tomorrow by 5 PM",
        "items": "Wireless Headphones"
    },
    "7850": {
        "status": "processing",
        "eta": "in 3 days",
        "items": "Gaming Monitor"
    },
    "3090": {
        "status": "delivered",
        "eta": "yesterday",
        "items": "USB-C Cable"
    }
}

class ValidateOrderStatusForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_order_status_form"

    def validate_order_id(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate if the user actually gave a valid-looking ID."""
        
        # Clean the input (remove spaces, make uppercase)
        cleaned_id = str(slot_value).strip()

        # Business Rule: IDs must be at least 3 chars long
        if len(cleaned_id) < 3:
            dispatcher.utter_message(text="That Order ID seems too short. Please say at least 3 digits.")
            return {"order_id": None} # Reject it

        # If user says something unrelated like "Cancel"
        if cleaned_id.lower() in ["cancel", "stop", "nevermind"]:
             dispatcher.utter_message(text="Okay, cancelling that request.")
             return {"order_id": None}

        # Accept the slot
        return {"order_id": cleaned_id}


class ActionCheckStatusAPI(Action):
    def name(self) -> Text:
        return "action_check_status_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_id = tracker.get_slot("order_id")
        
        # 1. Notify user (Simulate 'Thinking')
        dispatcher.utter_message(text=f"One moment, looking up order {order_id}...")
        time.sleep(1.0) 

        # 2. Query the Internal DB
        # We try to find the key in our dictionary
        order_data = MOCK_ORDER_DB.get(order_id)

        # 3. Handle Results
        if order_data:
            status = order_data['status']
            eta = order_data['eta']
            item = order_data['items']
            
            response_text = f"Found it. Your {item} is currently {status}. It is expected to arrive {eta}."
        else:
            # Not found
            response_text = f"I searched the system, but I could not find an order with ID {order_id}. Please check the number."

        dispatcher.utter_message(text=response_text)
        
        # 4. Clear slot so they can ask again
        return [SlotSet("order_id", None)]


class ActionEscalateAndHandoff(Action):
    def name(self) -> Text:
        return "action_escalate_and_handoff"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Connecting you to a human agent now. Please hold.")
        return [SlotSet("order_id", None)]