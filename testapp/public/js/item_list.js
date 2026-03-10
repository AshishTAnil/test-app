// frappe.listview_settings['Item'] = {
//     onload: function(listview) {

//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Bin",
//                 fields: ["item_code", "actual_qty"],
//                 filters: {
//                     "actual_qty": ["<", 10]
//                 },
//                 limit_page_length: 100
//             },
//             callback: function(r) {
//                 if (r.message && r.message.length > 0) {

//                     let items = [...new Set(r.message.map(d => d.item_code))];

//                     frappe.msgprint({
//                         title: __("Low Stock Alert"),
//                         message: __("The following items are below 10 quantity:<br><br><b>" + items.join("<br>") + "</b>"),
//                         indicator: "red"
//                     });
//                 }
//             }
//         });

//     }
// };

