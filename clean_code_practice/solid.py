from abc import ABC, abstractmethod

# Interfaces
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class RefundProcessor(ABC):
    @abstractmethod
    def refund_payment(self, amount):
        pass


# Payment Implementations
class CreditCardPayment(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing credit card payment of {amount}")

class DebitCardPayment(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing debit card payment of {amount}")


# Refund Implementations
class CreditCardRefund(RefundProcessor):
    def refund_payment(self, amount):
        print(f"Refunding credit card payment of {amount}")


# Services
class PaymentService:
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor

    def process_payment(self, amount):
        self.processor.process_payment(amount)


class RefundService:
    def __init__(self, refunder: RefundProcessor):
        self.refunder = refunder

    def refund_payment(self, amount):
        self.refunder.refund_payment(amount)


def main():
    credit_payment = CreditCardPayment()
    debit_payment = DebitCardPayment()
    credit_refund = CreditCardRefund()

    payment_service = PaymentService(credit_payment)
    payment_service.process_payment(100)

    refund_service = RefundService(credit_refund)
    refund_service.refund_payment(100)


if __name__ == "__main__":
    main()
