import frappe

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_lead_source_details(doctype, txt, searchfield, start, page_len, filters):
	data = frappe.get_all("Companywise Lead Source Details",filters=[["company", "=", filters.get("company")]],pluck="parent")

	lead_source_details = set()
	for row in data:
		lead_source_details.add(row)
	return [(d,) for d in lead_source_details]