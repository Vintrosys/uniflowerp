frappe.ui.form.on('Lead', {
    before_save: function(frm) {
        if(frm.is_new()){
            frappe.call({
                method: 'uniflowerp.uniflowerp.utils.duplicate_checker.update_lead_duplicates',
                args: {
                    lead: frm.doc
                },
                callback: (response) => {
                    if (response.message.refresh_form == "Y") {
                        frappe.msgprint(response.message.message);
                        frappe.validated = false;                 
                        frm.reload_doc();  
                    }
                    else { 
                        frappe.msgprint(response.message.message);
                    }                        
                }
            });
        }
    }
});

             