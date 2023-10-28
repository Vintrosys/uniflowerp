frappe.listview_settings['Lead'] = {
	filters: [["company", "=",frappe.defaults.get_user_default("Company")]],
		get_indicator: function(doc) {
			if(doc.status==="Yet to Connect") {
				return [__("Yet to Connect"), "blue", "status,=,Yet to Connect"];
			} else {
				return [__(doc.status), {
					"RNR": "yellow",
					"RNR2": "orange",
					"RNR3": "darkgrey",
					"RNR4": "purple",
					"RNR5": "red",
					"Switched Off": "purple",
					"Details Shared": "pink",
					"Interested": "green",
					"Plan Dropped": "red",
					"Clicked Mistake": "darkgrey",
					"Budget Mismatch": "darkgrey",
					"Inventory Mismatch": "darkgrey",
					"Location Mismatch": "darkgrey",
					"Less Amenities": "yellow"
				}[doc.status], "status,=," + doc.status];
			}
		},

		refresh:function(listview){
        cur_list.page.clear_primary_action()
    },
	refresh: function(listview) {
		if(listview.page.fields_dict.company && listview.page.fields_dict.company.get_input_value() != frappe.defaults.get_user_default("Company") && !frappe.ignore_company){
			listview.page.fields_dict.company.set_input(frappe.defaults.get_user_default("Company"))
			listview.refresh()
		}
	},
	onload: function(listview) {
		if(listview.page.fields_dict.company && listview.page.fields_dict.company.get_input_value() != frappe.defaults.get_user_default("Company") && !frappe.ignore_company){
			listview.page.fields_dict.company.set_input(frappe.defaults.get_user_default("Company"))
			listview.refresh()
		}
		if (frappe.boot.user.can_create.includes("Prospect")) {
			listview.page.add_action_item(__("Create Prospect"), function() {
				frappe.model.with_doctype("Prospect", function() {
					let prospect = frappe.model.get_new_doc("Prospect");
					let leads = listview.get_checked_items();
					frappe.db.get_value("Lead", leads[0].name, ["company_name", "no_of_employees", "industry", "market_segment", "territory", "fax", "website", "lead_owner"], (r) => {
						prospect.company_name = r.company_name;
						prospect.no_of_employees = r.no_of_employees;
						prospect.industry = r.industry;
						prospect.market_segment = r.market_segment;
						prospect.territory = r.territory;
						prospect.fax = r.fax;
						prospect.website = r.website;
						prospect.prospect_owner = r.lead_owner;

						leads.forEach(function(lead) {
							let lead_prospect_row = frappe.model.add_child(prospect, 'leads');
							lead_prospect_row.lead = lead.name;
						});
						frappe.set_route("Form", "Prospect", prospect.name);
					});
				});
			});
		}
	}
};