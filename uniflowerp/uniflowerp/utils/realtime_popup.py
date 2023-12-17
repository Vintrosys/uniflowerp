import frappe
import json

@frappe.whitelist()
def realtime_popup(data):

    try:

        data = json.loads(data)

        if data.get("doctype") == "ToDo":

            message= f"Hi {data.get('owner')}, <b>New Task For {data.get('reference_type')}: {data.get('reference_name')}</b> Assigned To You."

            frappe.publish_realtime(event='msgprint',message=message,user=str(data.get("owner")))
    
    except:
        pass