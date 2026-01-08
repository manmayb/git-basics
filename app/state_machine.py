VALID_TRANSITIONS = {
    "UNKNOWN": ["INWARD"],
    "CREATED": ["INWARD"],
    "INWARD": ["TRANSFER", "SOLD"],
    "TRANSFER": ["INWARD"],
    "SOLD": ["RETURNED"],
    "RETURNED": ["INWARD"],
    "SCRAPPED": []
}

class StateMachine:
    def transition(self, current_state: str, event_type: str) -> str:
        # If the state is UNKNOWN, we allow INWARD
        if current_state not in VALID_TRANSITIONS:
            if event_type == "INWARD":
                return "INWARD"
            return current_state
            
        allowed_next = VALID_TRANSITIONS.get(current_state, [])
        if event_type in allowed_next:
            return event_type
            
        return current_state

def is_valid_transition(current_state: str, new_event: str) -> bool:
    state_machine = StateMachine()
    return state_machine.transition(current_state, new_event) != current_state
