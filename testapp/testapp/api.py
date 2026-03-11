import frappe
import json

@frappe.whitelist()
def get_previous_supplier_rates(items, suppliers):

    # convert string to list if needed
    if isinstance(items, str):
        items = json.loads(items)

    if isinstance(suppliers, str):
        suppliers = json.loads(suppliers)

    if not items or not suppliers:
        return []

    data = frappe.db.sql("""
        SELECT
            pi.supplier,
            pii.item_code,
            pii.qty,
            pii.rate,
            pi.posting_date
        FROM `tabPurchase Invoice Item` pii
        INNER JOIN `tabPurchase Invoice` pi
            ON pi.name = pii.parent
        WHERE
            pii.item_code IN %s
            AND pi.supplier IN %s
            AND pi.docstatus = 1
        ORDER BY
            pii.item_code ASC,
            pii.rate ASC
    """, (tuple(items), tuple(suppliers)), as_dict=True)

    return data