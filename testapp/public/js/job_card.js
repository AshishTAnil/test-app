// frappe.ui.form.on("Job Card", {

//     process_loss: function(frm) {

//         if (!frm.doc.process_loss || !frm.doc.work_order) {
//             return;
//         }

//         frappe.call({
//             method: "frappe.client.get",
//             args: {
//                 doctype: "Work Order",
//                 name: frm.doc.work_order
//             },
//             callback: function(r) {

//                 if (!r.message) return;

//                 frm.clear_table("process_loss_items");

//                 (r.message.required_items || []).forEach(function(item) {

//                     let row = frm.add_child("process_loss_items");
//                     row.item_code = item.item_code;
//                     row.planned_qty = item.required_qty;
//                     row.loss_qty = 0;
//                 });

//                 frm.refresh_field("process_loss_items");
//             }
//         });
//     }

// });