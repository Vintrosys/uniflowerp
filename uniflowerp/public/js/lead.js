frappe.ui.form.on('Lead', {
    after_save(frm) {
        //? CHECK FOR THE DUPLICATE LEADS 
        frappe.call({
            method: "uniflowerp.api.check_lead_duplicated",
            args: {
                docname: frm.doc.name,
                custom_primary_phone: frm.doc?.custom_primary_phone,
            },
            freeze: true,
            freeze_message: "Checking Lead Duplicacy...",
            callback: function (check_response) {
                //? DEFINE VARIABLES
                const is_duplicate = check_response.message.is_duplicate;
                const parent_lead = check_response.message.parent_lead;

                if (is_duplicate) {
                    //? RELOAD THE CURRENT DOC
                    frm.reload_doc();

                    //? SET ROUTE TO THE PARENT DOC
                    frappe.set_route("form", "Lead", parent_lead);
                }

            }
        });
    }
});