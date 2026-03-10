import frappe
from frappe import _
from frappe.utils import getdate




def validate_work_order(doc, method=None):
    """
    Main Work Order validation entry point (before_submit).
    Add this in hooks.py
    """
    validate_bom_active(doc)
    validate_raw_material_stock(doc)


def validate_bom_active(doc):
    """Ensure selected BOM is Active."""
    if not doc.bom_no:
        return

    is_active = frappe.db.get_value("BOM", doc.bom_no, "is_active")

    if not is_active:
        frappe.throw(
            _("❌ BOM {0} is Inactive. Please activate it before submitting.")
            .format(doc.bom_no)
        )


def validate_raw_material_stock(doc):
    """Check sufficient Actual Qty in source warehouses."""
    for item in doc.required_items:

        if not item.source_warehouse:
            continue

        available_qty = frappe.db.get_value(
            "Bin",
            {
                "item_code": item.item_code,
                "warehouse": item.source_warehouse
            },
            "actual_qty"
        ) or 0

        if available_qty < item.required_qty:
            frappe.throw(
                _("❌ Insufficient Stock for Item: {0}\n\n"
                  "Required: {1}\n"
                  "Available: {2}\n"
                  "Warehouse: {3}")
                .format(
                    item.item_code,
                    item.required_qty,
                    available_qty,
                    item.source_warehouse
                )
            )




def prevent_overproduction(doc, method=None):
    """
    Prevent manufacturing more than Work Order planned qty.
    """
    if doc.stock_entry_type != "Manufacture" or not doc.work_order:
        return

    planned_qty, produced_qty = frappe.db.get_value(
        "Work Order",
        doc.work_order,
        ["qty", "produced_qty"]
    )

    current_fg_qty = doc.fg_completed_qty or 0
    total_after_submit = (produced_qty or 0) + current_fg_qty

    if total_after_submit > (planned_qty or 0):
        frappe.throw(
            _("❌ Overproduction Not Allowed!\n\n"
              "Work Order: {0}\n"
              "Planned Qty: {1}\n"
              "Already Produced: {2}\n"
              "Trying to Produce: {3}")
            .format(
                doc.work_order,
                planned_qty,
                produced_qty or 0,
                current_fg_qty
            )
        )


def prevent_backdated_manufacture(doc, method=None):
    """
    Prevent Stock Entry posting date earlier than Work Order transaction date.
    (ERPNext v15 compatible)
    """
    if doc.stock_entry_type != "Manufacture" or not doc.work_order:
        return

    work_order_date = frappe.db.get_value(
    "Work Order",
    doc.work_order,
    "planned_start_date"
    )

    if not work_order_date:
        return

    if getdate(doc.posting_date) < getdate(work_order_date):
        frappe.throw(
            _("❌ Backdated Manufacture Not Allowed.\n\n"
              "Work Order Date: {0}\n"
              "Stock Entry Date: {1}")
            .format(work_order_date, doc.posting_date)
        )