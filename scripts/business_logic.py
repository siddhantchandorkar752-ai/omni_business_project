import json
from datetime import datetime

class PricingEngine:
    def __init__(self):
        self.base_price = 1000.0
        self.discounts = {
            "Grade_A_Perfect": 0.0,
            "Grade_B_Minor": 0.30,
            "Grade_C_Reject": 1.0
        }

    def calculate_price(self, detection_class):
        discount = self.discounts.get(detection_class, 0.0)
        final_price = self.base_price * (1 - discount)
        return final_price

    def generate_marketing_trigger(self, item_id, detection_class):
        final_price = self.calculate_price(detection_class)
        status = "Standard Sale"
        
        if detection_class == "Grade_B_Minor":
            status = "Flash Sale - 30% Off"
        elif detection_class == "Grade_C_Reject":
            status = "Recycle Pipeline - No Sale"

        payload = {
            "item_id": item_id,
            "quality_grade": detection_class,
            "original_price": self.base_price,
            "final_price": final_price,
            "marketing_action": status,
            "timestamp": datetime.now().isoformat()
        }
        return payload

engine = PricingEngine()
sample_trigger = engine.generate_marketing_trigger("ITEM_8472", "Grade_B_Minor")

print(json.dumps(sample_trigger, indent=4))
print("Business Logic and Dynamic Pricing Engine Initialized.")