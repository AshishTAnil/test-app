frappe.ui.form.on('Material Request', {
    refresh: function(frm) {
        set_priority_indicator(frm);
    }
});

frappe.ui.form.on('Material Request Item', {

    custom_priority: function(frm) {
        set_priority_indicator(frm);
    },

    items_add: function(frm) {
        set_priority_indicator(frm);
    }

});

function set_priority_indicator(frm){

    setTimeout(function(){

        frm.fields_dict.items.grid.grid_rows.forEach(function(row){

            let priority = row.doc.custom_priority;

            let color = "";

            if(priority === "Immediate"){
                color = "red";
            }
            else if(priority === "High"){
                color = "orange";
            }
            else if(priority === "Medium"){
                color = "gold";
            }
            else if(priority === "Low"){
                color = "green";
            }

            let cell = $(row.row).find('[data-fieldname="custom_priority"] .grid-static-col');

            if(cell.length && color){

                cell.find(".priority-dot").remove();

                // 2. Added vertical-align: middle; and margin-top: -2px; to center it with the text
                cell.prepend(
                    `<span class="priority-dot"
                        style="
                        height: 10px;
                        width: 10px;
                        background: ${color};
                        border-radius: 50%;
                        display: inline-block;
                        margin-right: 6px;
                        vertical-align: middle;
                        margin-top: -2px;">
                    </span>`
                );
            }

        });

    },200);

}