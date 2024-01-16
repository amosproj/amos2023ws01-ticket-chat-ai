from enum import Enum


class Category(str, Enum):
    technical_issues = "Technical Issues"
    billing_payment = "Billing & Payment"
    product_inquiries = "Product Inquiries"
    account_management = "Account Management"
    policy_questions = "Policy Questions"
    complaints_feedback = "Complaints & Feedback"
