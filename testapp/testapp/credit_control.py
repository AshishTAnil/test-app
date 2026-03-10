import frappe
from frappe import _

def validate_customer_unpaid_invoices(doc, method):
    if not doc.customer:
        return

    unpaid_invoices = frappe.db.count(
        "Sales Invoice",
        {
            "customer": doc.customer,
            "docstatus": 1,
            "status": ["in", ["Unpaid", "Overdue"]]
        }
    )

    if unpaid_invoices >= 3 and not doc.custom_one_time_approval:
        frappe.throw(
            _("Customer has {0} unpaid invoices. Please enable One Time Approval.")
            .format(unpaid_invoices)
        )


