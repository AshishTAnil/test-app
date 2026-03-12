frappe.ui.form.on('Request for Quotation', {

    refresh: function(frm) {

        frm.add_custom_button("Supplier Price Comparison", function() {

            if (!frm.doc.items.length) {
                frappe.msgprint("Please add items first");
                return;
            }

            
            let items = [];
            frm.doc.items.forEach(row => {
                items.push(row.item_code);
            });

            
            let suppliers = [];
            frm.doc.suppliers.forEach(row => {
                suppliers.push(row.supplier);
            });

            frappe.call({
                method: "testapp.testapp.api.get_previous_supplier_rates",
                args: {
                    items: items,
                    suppliers: suppliers
                },

                callback: function(r) {

                    let data = r.message;

                    if (!data || data.length === 0) {
                        frappe.msgprint("No previous supplier purchase history found");
                        return;
                    }

                    // group by item
                    let grouped = {};

                    data.forEach(row => {

                        if (!grouped[row.item_code]) {
                            grouped[row.item_code] = [];
                        }

                        grouped[row.item_code].push(row);
                    });

                    let html = `<table class="table table-bordered">
                        <tr>
                            <th>Item</th>
                            <th>Supplier</th>
                            <th>Qty</th>
                            <th>Rate</th>
                            <th>Date</th>
                            <th>Rank</th>
                        </tr>`;

                    for (let item in grouped) {

                        let rows = grouped[item];

                        // sort by rate
                        rows.sort((a,b)=>a.rate-b.rate);

                        rows.forEach((row,index)=>{

                            let rank = index === 0 ? "🟢 Best" : index + 1;

                            html += `<tr>
                                <td>${row.item_code}</td>
                                <td>${row.supplier}</td>
                                <td>${row.qty}</td>
                                <td>${row.rate}</td>
                                <td>${row.posting_date}</td>
                                <td>${rank}</td>
                            </tr>`;
                        });
                    }

                    html += "</table>";

                    frappe.msgprint({
                        title: "Supplier Price Comparison",
                        message: html,
                        wide: true
                    });

                }

            });

        });

    }

});