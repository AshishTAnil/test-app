# import frappe

# @frappe.whitelist()
# def get_low_stock_items():

#     threshold = frappe.db.get_single_value(
#         "Stock Alert Settings",
#         "low_stock_threshold"
#     ) or 10

#     low_stock = frappe.db.sql("""
#         SELECT 
#             item_code,
#             warehouse,
#             actual_qty
#         FROM `tabBin`
#         WHERE actual_qty < %s
#         ORDER BY actual_qty ASC
#         LIMIT 20
#     """, threshold, as_dict=True)

#     return {
#         "items": low_stock,
#         "threshold": threshold
#     }
