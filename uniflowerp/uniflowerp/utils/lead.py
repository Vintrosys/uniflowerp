import frappe

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_lead_source_details(doctype, txt, searchfield, start, page_len, filters):
	data = frappe.db.get_list('Companywise Lead Source Details',{
	'company': filters.get("company")
	},['parent'])

	lead_source_details = set()
	for row in data:
		lead_source_details.add(row['parent'])
	return [(d,) for d in lead_source_details]