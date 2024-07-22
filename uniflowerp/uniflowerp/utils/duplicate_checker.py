import frappe
from frappe.model.document import Document
from datetime import date, datetime
from frappe.utils import nowdate, now_datetime


@frappe.whitelist()
def update_lead_duplicates(lead):	
    
    cur_lead = frappe.parse_json(lead)

    if frappe.flags.in_update_lead_duplicates:
        return

    # Set the flag to prevent recursion
    frappe.flags.in_update_lead_duplicates = True

    lead_list = frappe.db.get_list("Lead", {'custom_primary_phone': cur_lead.custom_primary_phone, "name": ["!=", cur_lead.name] }, 
        ['name', "company_name", "email_id", "custom_primary_phone", "source", "custom_source_details",
        "creation"])
    lead_list += frappe.db.get_list("Lead", {'email_id': cur_lead.email_id, "name": ["!=", cur_lead.name]}, 
        ['name', "company_name", "email_id", "custom_primary_phone", "source", "custom_source_details",
        "creation"])
    
    lead_details = [i for n, i in enumerate(lead_list) if i not in lead_list[n + 1:]]

    # Sort leads by creation date
    lead_details = sorted(lead_details, key=lambda x: x['creation'])

    # Update the child table of the lead created very first
    if lead_details:	    
        parent_lead = lead_details[0]
        lead_doc = frappe.get_doc("Lead", parent_lead["name"])

        latest_lead = lead_details[-1]
        latest_doc = frappe.get_doc("Lead", latest_lead["name"])

        if lead_doc.email_id != cur_lead.email_id:
            secondary_email = cur_lead.email_id
        else:
            secondary_email = None

        if isinstance(nowdate(), str):
            cur_lead_creation = datetime.strptime(nowdate(), '%Y-%m-%d')
        
        difference_in_date = (cur_lead_creation.date() - latest_doc.creation.date()).days

        lead_doc.append("custom_lead_duplicate_details", {
            "name1": cur_lead.company_name, 
            "email": cur_lead.email_id if not(secondary_email) else None,
            "custom_secondary_email": secondary_email,
            "phone_no": cur_lead.custom_primary_phone,
            "source": cur_lead.source,
            "source_detail": cur_lead.custom_source_details if cur_lead.custom_source_details else None,
            "created_date_and_time": now_datetime(),
            "custom_age__range": difference_in_date,
        })
        lead_doc.save(ignore_permissions=True)
        frappe.db.commit()  
        parent_lead_url = frappe.utils.get_url_to_form('Lead', lead_doc.name)

        frappe.flags.in_update_lead_duplicates = False        	        

        return {
            "message": f"This lead is a duplicate of: <a href='{parent_lead_url}'>{lead_doc.name}</a>.<br> Lead duplicates updated successfully.",
            "refresh_form": "Y"
        }    
   
    else:
        
        frappe.flags.in_update_lead_duplicates = False
        return {
            "message": f"A new lead has been created successfully.",
            "refresh_form": "N"
        }
        
