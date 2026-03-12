app_name = "testapp"
app_title = "testapp"
app_publisher = "Ashish TA"
app_description = "customisation"
app_email = "ashish@gmail.com"
app_license = "mit"

# -----------------------------------------------------------
# Client Scripts (Load JS from App)
# -----------------------------------------------------------
# Client Scripts (Load JS from App)

doctype_js = {
    "Request for Quotation": "public/js/rfq_supplier_rates.js",
    "Material Request": "public/js/material_request_priority.js"
}
# -----------------------------------------------------------
# Document Events
# -----------------------------------------------------------
doc_events = {

    "Sales Invoice": {
        "before_submit": "testapp.testapp.credit_control.validate_customer_unpaid_invoices"
    },

    "Purchase Order": {
        "before_submit": "testapp.testapp.buying_validations.block_po_if_supplier_has_3_unpaid"
    },

    "Work Order": {
        "on_submit": "testapp.testapp.process_loss.handle_process_loss"
    },

    "Stock Entry": {
        "before_submit": [
            "testapp.testapp.manufacturing_validation.prevent_overproduction",
            "testapp.testapp.manufacturing_validation.prevent_backdated_manufacture"
        ],
        "on_submit": "testapp.testapp.process_loss.create_loss_on_manufacture"
    },

    "Job Card": {
        "on_submit": "testapp.testapp.job_card_loss.create_process_loss_entry"
    }
}

# -----------------------------------------------------------
# Optional Overrides
# -----------------------------------------------------------
# override_doctype_dashboards = {
#     "Work Order": "testapp.work_order_dashboard.get_data"
# }

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            ["fieldname", "=", "custom_priority"]
        ]
    }
]