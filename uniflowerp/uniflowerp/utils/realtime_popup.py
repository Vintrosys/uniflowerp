import frappe
import json

from frappe.utils import comma_and,	get_link_to_form

@frappe.whitelist()
def realtime_popup(data):

    try:

        data = json.loads(data)

        if data.get("doctype") == "ToDo":

            link = get_link_to_form(data.get('reference_type'), data.get('reference_name'))

            message = f"Hi {data.get('owner')}, <b>New Task For {data.get('reference_type')}: {link}</b> Assigned To You."

            notification = frappe.new_doc("Notification Log")

            notification.for_user = data.get('owner')

            notification.document_type = data.get('reference_type')

            notification.document_name = data.get('reference_name')

            notification.subject = f"Hi <b>New Task For {data.get('reference_type')}: {data.get('reference_name')}</b> Assigned To You."

            notification.type = "Energy Point"
            
            notification.save()

            frappe.publish_realtime(event = 'msgprint', message = message, user = str(data.get("owner")))
    
    except:
        pass