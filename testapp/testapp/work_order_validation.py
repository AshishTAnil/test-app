import frappe

def check_low_stock(doc, method):
    
    low_stock_items = []

    for item in doc.required_items:
        actual_qty = frappe.db.get_value(
            "Bin",
            {
                "item_code": item.item_code,
                "warehouse": item.source_warehouse
            },
            "actual_qty"
        ) or 0

        if actual_qty < 10:
            low_stock_items.append(
                f"{item.item_code} (Available: {actual_qty})"
            )

    if low_stock_items:
        frappe.throw(
            "Low Stock Alert! The following items have stock less than 10:<br><br>"
            + "<br>".join(low_stock_items)
        )