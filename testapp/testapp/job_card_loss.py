import frappe
from frappe.utils import nowdate

def create_process_loss_entry(doc, method):

    if not doc.custom_process_loss_items:
        return

    items_to_issue = []

    for row in doc.custom_process_loss_items:
        if not row.loss_qty or row.loss_qty <= 0:
            continue

        if row.loss_qty > row.planned_qty:
            frappe.throw(
                f"Loss Qty cannot be greater than Planned Qty for item {row.item_code}"
            )

        items_to_issue.append({
            "item_code": row.item_code,
            "qty": row.loss_qty,
            "s_warehouse": doc.wip_warehouse
        })

    if not items_to_issue:
        return

    se = frappe.new_doc("Stock Entry")
    se.stock_entry_type = "Material Issue"
    se.company = doc.company
    se.posting_date = nowdate()

    for item in items_to_issue:
        se.append("items", item)

    se.insert()
    se.submit()

    frappe.msgprint(f"Material Issue {se.name} created for Process Loss.")