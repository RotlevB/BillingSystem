from datetime import date, timedelta

def calculate_due_date(week):
    current_date = date.today()
    other_date = current_date + timedelta(weeks=week)
    return other_date

# BillingSystem class
class BillingSystem:
    def __init__(self):
        self.active_customers = []
        self.awaiting_customers = []
        self.inactive_customers = []
        self.processor_api = ProcessorAPI()

    def perform_advance(self, dst_bank_account, amount):
        if(amount <= 0):
            return 0
        # Create a new customer
        customer = Customer(dst_bank_account, amount)
        self.awaiting_customers.append(customer)

        # Perform initial credit transaction
        transaction_id = self.processor_api.perform_transaction(
            "billing_system_account", dst_bank_account, amount, "credit"
        )
        customer.add_transaction(transaction_id)

        

    #do once a day, after status update
    def process_repayments(self):
        for customer in self.active_customers:
            if customer.has_scheduled_repayments():
                next_repayment = customer.get_next_repayment()
                due_date = next_repayment["due_date"]
                amount = next_repayment["amount"]
                if(due_date == date.today()):
                    # Perform debit transaction
                    transaction_id = self.processor_api.perform_transaction(
                        customer.dst_bank_account, "billing_system_account", amount, "debit"
                    )

                    if transaction_id is not None:
                        customer.add_transaction(transaction_id)
                        customer.complete_repayment()
                    else:
                        customer.move_repayment_to_end()
                    if(not(customer.has_scheduled_repayments()) and customer.amount_owed() > 0):
                        customer.schedule_repayment(calculate_due_date(1), amount)
            else:
                if(customer.amount_owed() > 0):
                    customer.schedule_repayment(calculate_due_date(1), amount)


    
    #checks report for updates
    def status_update(self):
        report = self.processor_api.download_report()
        report_map = {}
        for transaction in report:
            split_result = transaction_string.split(", ")
            transaction_id = int(split_result[0])
            status = split_result[1]
            report_map[transaction_id] = status

        for customer in self.active_customers:
            transaction_ids = customer.get_transaction_ids()
            for transaction in transaction_ids:    
                if transaction in report_map:
                    customer.update_transaction_status(transaction, report_map[transaction])
                    amount_owed = customer.amount_owed()
                    if(amount_owed < 0):
                        transaction_id = self.processor_api.perform_transaction(
                            "billing_system_account", dst_bank_account, amount, "credit"
                        )
                        if transaction_id is not None:
                            customer.add_refund(transaction_id)

            if(len(customer.get_transaction_ids()) == 0):
                amount_owed = customer.amount_owed() 
                if (amount_owed < 0):
                    transaction_id = self.processor_api.perform_transaction(
                            "billing_system_account", dst_bank_account, amount, "credit"
                        )
                    if transaction_id is not None:
                        customer.add_refund(transaction_id)
                else:
                    if(amount_owed == 0):
                        self.active_customers.remove(customer)
                        self.inactive_customers.append(customer)
                        customer.reset_payment_plan()
                    else:
                        if not(customer.has_scheduled_repayments()):
                            customer.reset_payment_plan()
                    
                
        
        for customer in self.awaiting_customers:
            transaction_ids = customer.get_transaction_ids()
            if transaction_ids[0] in report_map:
                self.awaiting_customers.remove(customer)
                if(report_map[transaction_ids[0]] == "success"):
                    customer.activate()
                    self.active_customers.append(customer)
                else:
                    self.inactive_customers.append(customer)
                

# Customer class
class Customer:
    def __init__(self, dst_bank_account, advance_amount, first_transaction):
        self.dst_bank_account = dst_bank_account
        self.advance_amount = advance_amount
        self.first_transaction = first_transaction
        self.status = "waiting"
        self.amount_payed = 0
        self.refunded = 0
        self.refunds = []
        self.repayments = []
        self.awaiting_transactions = []
        self.done_transactions = {}


    def reset_payment_plan(self):
        self.repayments = []
        payment_num = self.amount_owed() * 12 / self.advance_amount
        if payment_num > 0:
            for week in range(1, payment_num + 1):
                due_date = calculate_due_date(week)
                customer.schedule_repayment(due_date, repayment_amount)
    def amount_owed(self):
        return self.advance_amount + self.amount_payed - self.refunded

    def add_transaction(self, transaction_id):
        self.awaiting_transactions.append(transaction_id)
    
    def add_refund(self, transaction_id):
        self.refunds.append(transaction_id)

    def schedule_repayment(self, due_date, amount):
        self.repayments.append({"due_date": due_date, "amount": amount})

    def has_scheduled_repayments(self):
        return len(self.repayments) > 0

    def get_next_repayment(self):
        return self.repayments[0]

    def complete_repayment(self):
        self.repayments.pop(0)

    def move_repayment_to_end(self):
        failed_repayment = self.repayments.pop(0)
        self.repayments.append(failed_repayment)

    def get_transaction_ids(self):
        return self.awaiting_transactions + self.refunds
    
    def activate(self):
        self.update_transaction_status(self.first_transaction, "success")
        self.status = "active"
        # Schedule weekly debit transactions
        repayment_amount = self.advance_amount / 12
        for week in range(1, 13):
            due_date = calculate_due_date(week)
            customer.schedule_repayment(due_date, repayment_amount)
    


    def update_transaction_status(self, transaction_id, status):
        if transaction_id in self.done_transactions or transaction_id not in self.awaiting_transactions:
            if transaction_id in self.refunds and status == success:
                self.refunded += self.advance_amount / 12
                return 1
            return 0
        if(not(self.status == "waiting") and status == success):
            self.amount_payed += self.advance_amount / 12
        self.awaiting_transactions.remove(transaction_id)
        self.done_transactions[transaction_id] = status
        return 1
        

# ProcessorAPI class
class ProcessorAPI:
    def perform_transaction(self, src_bank_account, dst_bank_account, amount, direction):
        # Perform the transaction using the "processor" API
        # Return the transaction ID


    def download_report(self):
        # Download the transaction report using the "processor" API
        # Return the report as a dictionary {transaction_id: status}

