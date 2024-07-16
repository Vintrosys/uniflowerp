import frappe
from frappe.model.document import Document
from datetime import date, datetime


def before_save(self, event):
    update_lead_duplicates(self)

def update_lead_duplicates(self):	

    if frappe.flags.in_update_lead_duplicates:
        return

    # Set the flag to prevent recursion
    frappe.flags.in_update_lead_duplicates = True

    lead_list = frappe.db.get_list("Lead", {'custom_primary_phone': self.custom_primary_phone, "name": ["!=", self.name] }, 
        ['name', "company_name", "email_id", "custom_primary_phone", "source", "custom_source_details",
        "creation"])
    lead_list += frappe.db.get_list("Lead", {'email_id': self.email_id, "name": ["!=", self.name]}, 
        ['name', "company_name", "email_id", "custom_primary_phone", "source", "custom_source_details",
        "creation"])
    
    lead_details = [i for n, i in enumerate(lead_list) if i not in lead_list[n + 1:]]

    # Sort leads by creation date
    lead_details = sorted(lead_details, key=lambda x: x['creation'])

    # Update the child table of the lead created very first
    if lead_details:	
        self.custom_is_duplicate = 1		
        parent_lead = lead_details[0]
        lead_doc = frappe.get_doc("Lead", parent_lead["name"])

        latest_lead = lead_details[-1]
        latest_doc = frappe.get_doc("Lead", latest_lead["name"])

        if lead_doc.email_id != self.email_id:
            secondary_email = self.email_id
        else:
            secondary_email = None

        if isinstance(latest_doc.creation, str):
            latest_doc.creation = datetime.strptime(latest_doc.creation, '%Y-%m-%d %H:%M:%S.%f')
        latest_doc_creation_date = latest_doc.creation.date()
        frappe.msgprint(f"latest doc creation time: {latest_doc_creation_date}")

        if isinstance(self.creation, str):
            self.creation = datetime.strptime(self.creation, '%Y-%m-%d %H:%M:%S.%f')
        self_creation_date = self.creation.date()
        frappe.msgprint(f"self creation: {self_creation_date}")

        difference_in_date = (self_creation_date - latest_doc_creation_date).days
        frappe.msgprint(f"date diff: {difference_in_date}")

        lead_doc.append("custom_lead_duplicate_details", {
            "name1": self.company_name, 
            "lead_id": self.name,
            "email": self.email_id if not(secondary_email) else None,
            "custom_secondary_email": secondary_email,
            "phone_no": self.custom_primary_phone,
            "source": self.source,
            "source_detail": self.custom_source_details if self.custom_source_details else None,
            "created_date_and_time": self.creation,
            "custom_age__range": difference_in_date,

        })
        lead_doc.save(ignore_permissions=True)
        frappe.msgprint(f"This lead is the duplicate of : {lead_doc.name}<br><br>Lead duplicates updated successfully.", title="Duplicate Lead", indicator="blue")
    elif self.is_new():
        self.custom_is_duplicate = 0
        frappe.msgprint(f"A new lead has been created with ID : {self.name}")
    else:
        self.custom_is_duplicate = 0

frappe.flags.in_update_lead_duplicates = False







