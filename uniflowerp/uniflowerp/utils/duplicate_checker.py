import frappe
from frappe.model.document import Document

@frappe.whitelist()
def check_for_duplicate_lead(lead):
    frappe.msgprint("Inside dup check py")
    lead = frappe.parse_json(lead)
    lead_name = lead.get('name')
    email_id = lead.get('email_id')
    phone = lead.get('custom_primary_phone')

    # Check for existing leads with the same email or phone number
    existing_leads = frappe.get_all('Lead', filters=[
        ['email_id', '=', email_id],
        ['custom_primary_phone', '=', phone]
    ], fields=['name', 'email_id', 'custom_primary_phone', 'source', 'custom_source_details']) # add  'creation_date' later

    if not existing_leads:
        existing_leads = frappe.get_all('Lead', filters=[
            ['custom_primary_phone', '=', phone]
        ], fields=['name', 'email_id', 'custom_primary_phone', 'source', 'custom_source_details']) # add  'creation_date' later

    if existing_leads:
        for existing_lead in existing_leads:
            # Fetch the lead document
            lead_doc = frappe.get_doc('Lead', existing_lead.name)

            # Update the Lead Duplicate Details child table
            lead_duplicate_detail = lead_doc.append('custom_lead_duplicate_details', {})
            lead_duplicate_detail.name1 = lead_name
            lead_duplicate_detail.phone_no = phone
            lead_duplicate_detail.email = email_id
            lead_duplicate_detail.source = lead.get('source')
            lead_duplicate_detail.source_detail = lead.get('source_detail')
            # lead_duplicate_detail.created_date_time = lead.get('creation')

            if existing_lead.email_id != email_id:
                lead_duplicate_detail.secondary_email = email_id

            lead_doc.save()
            return {"message": "Lead updated with duplicate details."}

    return {"message": "No matching lead found."}
