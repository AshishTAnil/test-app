import frappe
from frappe.utils import nowdate, flt



def create_entries_from_work_order(work_order, source_warehouse=None, posting_date=None):

    try:

        if not work_order.custom_process_loss_items:
            return

        loss_items = []
        restore_items = []

       
        for row in work_order.custom_process_loss_items:

            if not row.item_code:
                continue

            stock_uom = frappe.get_value("Item", row.item_code, "stock_uom")

           
            if flt(row.loss_qty) > 0:

                warehouse = source_warehouse or work_order.wip_warehouse

                if not warehouse:
                    frappe.throw("WIP Warehouse is not set in Work Order.")

                loss_items.append({
                    "item_code": row.item_code,
                    "qty": flt(row.loss_qty),
                    "uom": stock_uom,
                    "s_warehouse": warehouse
                })

           
            if flt(row.restore_qty) > 0:

                if not work_order.source_warehouse:
                    frappe.throw("Source Warehouse is not set in Work Order.")

                if not work_order.wip_warehouse:
                    frappe.throw("WIP Warehouse is not set in Work Order.")

                restore_items.append({
                    "item_code": row.item_code,
                    "qty": flt(row.restore_qty),
                    "uom": stock_uom,
                    "s_warehouse": work_order.source_warehouse,
                    "t_warehouse": work_order.wip_warehouse
                })

        
        if loss_items:

            existing_loss = frappe.get_all(
                "Stock Entry",
                filters={
                    "work_order": work_order.name,
                    "stock_entry_type": "Material Issue",
                    "docstatus": 1
                }
            )

            if not existing_loss:

                loss_entry = frappe.new_doc("Stock Entry")
                loss_entry.stock_entry_type = "Material Issue"
                loss_entry.company = work_order.company
                loss_entry.posting_date = posting_date or nowdate()
                loss_entry.work_order = work_order.name

                for item in loss_items:
                    loss_entry.append("items", item)

                loss_entry.insert(ignore_permissions=True)
                loss_entry.submit()

                frappe.msgprint(f"Material Issue {loss_entry.name} created successfully.")

        
        if restore_items:

            restore_entry = frappe.new_doc("Stock Entry")
            restore_entry.stock_entry_type = "Material Transfer for Manufacture"
            restore_entry.company = work_order.company
            restore_entry.posting_date = posting_date or nowdate()
            restore_entry.work_order = work_order.name

            for item in restore_items:
                restore_entry.append("items", item)

            restore_entry.insert(ignore_permissions=True)
            restore_entry.submit()

            frappe.msgprint(f"Material Transfer for Manufacture{restore_entry.name} created successfully.")

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Process Loss Entry Creation Failed")




def handle_process_loss(doc, method):

    if doc.docstatus != 1:
        return

    create_entries_from_work_order(doc)



def create_loss_on_manufacture(doc, method):

    if doc.stock_entry_type != "Manufacture":
        return

    if not doc.work_order:
        return

    work_order = frappe.get_doc("Work Order", doc.work_order)

    
    source_warehouse = None

    for item in doc.items:
        if item.s_warehouse:
            source_warehouse = item.s_warehouse
            break

    if not source_warehouse:
        frappe.throw("Source Warehouse not found in Manufacture Entry.")

    create_entries_from_work_order(
        work_order=work_order,
        source_warehouse=source_warehouse,
        posting_date=doc.posting_date
    )