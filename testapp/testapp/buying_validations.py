import frappe

def block_po_if_supplier_has_3_unpaid(doc, method=None):
    if not doc.supplier:
        return

    unpaid_count = frappe.db.count("Purchase Invoice", {
        "supplier": doc.supplier,
        "docstatus": 1,
        "outstanding_amount": (">", 0)
    })

    if unpaid_count >= 3:
        frappe.throw(
            f"Supplier {doc.supplier} has {unpaid_count} unpaid Purchase Invoices. "
            "Cannot submit new Purchase Order until payment is made."
        )