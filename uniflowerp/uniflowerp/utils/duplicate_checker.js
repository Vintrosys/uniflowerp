frappe.ui.form.on('Lead', {
    before_save: function(frm) {
        if (frm.doc.email_id || frm.doc.custom_primary_phone) {
            frappe.msgprint("Inside duplicate check js")
            console.log("Inside duplicate check js")
            frappe.call({
                method: 'uniflowerp.uniflowerp.custom.duplicate_checker.check_for_duplicate_lead',
                args: {
                    lead: frm.doc
                },
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint(response.message);
                    }
                    frm.save(); // Save the form after the callback
                }
            });
            frappe.validated = false; // Prevent default save to handle it manually in the callback
        }
    }
});
