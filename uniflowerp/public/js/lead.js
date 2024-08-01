frappe.ui.form.on('Lead', {
    after_save(frm) {
        frappe.call({
            method: "uniflowerp.api.check_lead_duplicated",
            args: {
                docname: frm.doc.name,
                custom_primary_phone: frm.doc?.custom_primary_phone,
            },
            freeze: true,
            freeze_message: "Checking Lead Duplicacy...",
            callback: function (check_response) {
                // DEFINE VARIABLES
                const is_duplicate = check_response.message.is_duplicate;
                const parent_lead = check_response.message.parent_lead;

                if (is_duplicate) {
                    // RELOAD THE CURRENT DOC
                    frm.reload_doc();

                    // SET HISTORY TO THE LEAD LIST VIEW
                    frappe.set_route("list", "Lead");

                    // SET ROUTE TO THE PARENT DOC
                    frappe.set_route("form", "Lead", parent_lead);

                    if (frm.doc.email_id) {
                        // // WELCOME EMAIL
                        // const welcome_email_html =  `<h1>
                        //                                 Hello ${frm.doc.company_name},
                        //                             </h1>
                        //                             <p>
                        //                                 The New Lead is Created for Company: ${frm.doc.company}.
                        //                             </p>`
                        // // WELCOME EMAIL
                        // frappe.call({
                        //     method:"resend_integration.api.send_resend_emails",
                        //     args:{
                        //         //  "Get discount!",
                        //         subject:"Welcome!",
                        //         from_email:"marketing@uniflowerp.in",
                        //         to_emails:frm.doc.email_id,
                        //         email_html:welcome_email_html,
                        //     },
                        //     callback:function(res){
                        //         console.log(res);
                        //     }
                        // });
                    }


                    if (frm.doc.lead_owner) {
                        // LEAD OWNER EMAIL HTML
                        // const lead_owner_email_html =   `<h1>
                        //                                     Hello ${frm.doc.lead_owner},
                        //                                 </h1>
                        //                                 <p>
                        //                                     The New Duplicate Lead is Created for ${frm.doc.company}.
                        //                                 </p>
                        //                                 <p>
                        //                                     Here is the link of the parent lead <a href=${window.location.origin + "/app/lead/"+parent_lead} >${parent_lead}</a>.
                        //                                 </p>`
                        // // LEAD OWNER EMAIL
                        // frappe.call({
                        //     method:"resend_integration.api.send_resend_emails",
                        //     args:{
                        //         //  "Get discount!",
                        //         subject:"New Lead!",
                        //         from_email:"marketing@uniflowerp.in",
                        //         to_emails:frm.doc.lead_owner,
                        //         email_html:lead_owner_email_html,
                        //     },
                        //     callback:function(res){
                        //         console.log(res);
                        //     }
                        // });
                    }
                }

            }
        });
    }
});