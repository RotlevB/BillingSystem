# Billing System
This Python module BillingSystem.py implements a billing system that handles advanced payments and repayment processing using the provided ProcessorAPI class. The billing system allows performing advances, scheduling repayments, and tracking the status of transactions. It utilizes the Customer class to manage customer-related information and the ProcessorAPI class to interact with the external payment processor.

**Dependencies**

datetime: The module used to handle date and time operations.

**Classes**

BillingSystem

This class represents the billing system and manages the customers and their transactions.

Methods:

__init__(self): Initializes the BillingSystem object with empty customer lists and a ProcessorAPI object.

perform_advance(self, dst_bank_account, amount): Performs an advance payment for a customer, initiating a credit transaction and adding the customer to the awaiting customers list.

process_repayments(self): Processes the scheduled repayments for active customers, performing debit transactions, updating transaction statuses, and managing the payment plan.

status_update(self): Updates the transaction statuses based on the downloaded report, manages customer statuses, and handles refunds.

Customer

This class represents a customer and their payment information.

Methods:

__init__(self, dst_bank_account, advance_amount, first_transaction): Initializes the Customer object with destination bank account, advance amount, and first transaction ID.

reset_payment_plan(self): Resets the payment plan for the customer, scheduling new repayments based on the remaining amount owed.

amount_owed(self): Calculates and returns the amount owed by the customer.

add_transaction(self, transaction_id): Adds a transaction ID to the awaiting transactions list.

add_refund(self, transaction_id): Adds a refund transaction ID to the refunds list.

schedule_repayment(self, due_date, amount): Schedules a repayment with the provided due date and amount.

has_scheduled_repayments(self): Checks if the customer has scheduled repayments.

get_next_repayment(self): Returns the details of the next scheduled repayment.

complete_repayment(self): Marks the next repayment as complete.

move_repayment_to_end(self): Moves the failed repayment to the end of the repayment plan.

get_transaction_ids(self): Returns a list of transaction IDs for both awaiting transactions and refunds.

activate(self): Activates the customer, updates the first transaction status, sets the status to "active," and schedules weekly debit transactions.

update_transaction_status(self, transaction_id, status): Updates the status of a transaction and handles refunds or completing repayments.

ProcessorAPI

This class interacts with the external payment processor API for performing transactions and downloading reports.

Methods:

perform_transaction(self, src_bank_account, dst_bank_account, amount, direction): Performs a transaction using the "processor" API and returns the transaction ID.

download_report(self): Downloads the transaction report using the "processor" API and returns the report




