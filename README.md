## Uniflowerp

Uniflow ERP

#### License

MIT

apps/frappe/frappe/templates/includes/navbar/navbar.html - Empty File

apps/frappe/frappe/templates/includes/footer/footer.html

<footer>
	<!-- <div class="container"> -->
		<!-- {% include "templates/includes/footer/footer_logo_extension.html" %} -->

		<!-- {% if footer_items -%}
			{% include "templates/includes/footer/footer_grouped_links.html" %}
		{% endif %} -->

		<!-- {% include "templates/includes/footer/footer_links.html" %} -->
		{% include "templates/includes/footer/footer_info.html" %}
	<!-- </div> -->
</footer>


apps/frappe/frappe/templates/signup.html -  placeholder="{{ _('jane@example.com') }}" to placeholder="{{ _('Your Email ID') }}"

apps/frappe/frappe/public/scss/website/footer.scss:

.web-footer {
	padding: 3rem 0;
	min-height: 140px;
	background-color: var(--fg-color);
	background-image: url("https://app.uniflowerp.in//files/WhatsApp%20Image%202023-10-25%20at%2015.56.57.jpeg");
	border-top: 1px solid $border-color;
}

### Frappe/ERP next code files changes.
Paths: 
1./frappe-bench/apps/erpnext/erpnext/crm/doctype/lead/lead.py
2./frappe-bench/apps/frappe/frappe/desk/form/assign_to.py
3./frappe-bench/apps/frappe/frappe/public/js/desk.bundle.js

Run commands: 
bench build 
sudo supervisorctl reload

