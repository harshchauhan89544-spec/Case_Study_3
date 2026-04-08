#Harsh Chauhan 
#202501100700076
from abc import ABC, abstractmethod

class Payment(ABC):
    def __init__(self, user_name):
        self.user_name = user_name
        self.original_amount = 0
        self.final_amount = 0
        self.breakdown = []

    @abstractmethod
    def pay(self, amount):
        pass

    def generate_receipt(self):
        print(f"\n--- Payment Receipt ---")
        print(f"User: {self.user_name}")
        print(f"Original Amount: ₹{self.original_amount:.2f}")
        
        if self.breakdown:
            print("Breakdown:")
            for item, value in self.breakdown:
                if value < 0:
                    print(f"  {item}: -₹{abs(value):.2f}")
                else:
                    print(f"  {item}: +₹{value:.2f}")
                    
        print(f"Final Amount Paid: ₹{self.final_amount:.2f}")
        print(f"-----------------------\n")

class CreditCardPayment(Payment):
    def pay(self, amount):
        self.original_amount = amount
        gateway_fee = amount * 0.02
        gst = gateway_fee * 0.18
        self.final_amount = amount + gateway_fee + gst
        
        self.breakdown = [
            ("Gateway Fee (2%)", gateway_fee),
            ("GST on Gateway Fee (18%)", gst)
        ]
        self.generate_receipt()

class UPIPayment(Payment):
    def pay(self, amount):
        self.original_amount = amount
        cashback = 50 if amount > 1000 else 0
        self.final_amount = amount - cashback
        
        self.breakdown = []
        if cashback > 0:
            self.breakdown.append(("Cashback Applied", -cashback))
            
        self.generate_receipt()

class PayPalPayment(Payment):
    def pay(self, amount):
        self.original_amount = amount
        intl_fee = amount * 0.03
        conversion_fee = 20
        self.final_amount = amount + intl_fee + conversion_fee
        
        self.breakdown = [
            ("International Transaction Fee (3%)", intl_fee),
            ("Currency Conversion Fee (Fixed)", conversion_fee)
        ]
        self.generate_receipt()

class WalletPayment(Payment):
    def __init__(self, user_name, balance):
        super().__init__(user_name)
        self.balance = balance

    def pay(self, amount):
        self.original_amount = amount
        if amount > self.balance:
            print(f"\nTransaction Failed for {self.user_name}: Insufficient wallet balance.")
            print(f"Current Balance: ₹{self.balance:.2f} | Required: ₹{amount:.2f}\n")
        else:
            self.balance -= amount
            self.final_amount = amount
            self.breakdown = [] 
            self.generate_receipt()
            print(f"Remaining Wallet Balance: ₹{self.balance:.2f}\n")

def process_payment(payment_obj, amount):
    payment_obj.pay(amount)

if __name__ == "__main__":
    user_name = input("Enter user name: ")
    
    print("\nAvailable Payment Methods:")
    print("1. Credit Card")
    print("2. UPI")
    print("3. PayPal")
    print("4. Digital Wallet")
    
    choice = input("Select a payment method (1-4): ")
    
    try:
        amount = float(input("Enter the payment amount: ₹"))
    except ValueError:
        print("Invalid amount entered. Exiting.")
        exit()

    if choice == '1':
        selected_payment = CreditCardPayment(user_name)
    elif choice == '2':
        selected_payment = UPIPayment(user_name)
    elif choice == '3':
        selected_payment = PayPalPayment(user_name)
    elif choice == '4':
        selected_payment = WalletPayment(user_name, 1000) 
    else:
        print("Invalid choice selected. Exiting.")
        exit()

    process_payment(selected_payment, amount)