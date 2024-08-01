import frappe
from frappe.utils import get_datetime, date_diff
from resend_integration.api import send_resend_emails


#! CHECK THE DUPLICATED LEAD
@frappe.whitelist()
def check_lead_duplicated(docname, custom_primary_phone):
    # ? FINAL RESPONSE MESSAGE
    response_message = {}

    # ? LIST OF DUPLICATE RECORDS
    check_duplicate_lead = frappe.get_all(
        "Lead",
        filters={
            "name": ["!=", docname],
            "custom_primary_phone": custom_primary_phone,
        },
        fields=["name"],
        order_by="creation asc",
    )

    # ? IF DUPLICATE LEAD EXISTS
    if check_duplicate_lead:
        parent_lead_id = check_duplicate_lead[0].name

        response_message["is_duplicate"] = True
        response_message["parent_lead"] = parent_lead_id

    # ? IF DUPLICATE LEAD DOES EXISTS
    else:
        response_message["is_duplicate"] = False
        response_message["parent_lead"] = None

    return response_message


#! HANDLE THE DUPLICATED LEAD
def handle_duplicated_lead(doc, event):
    # ? LIST OF DUPLICATE RECORDS
    check_duplicate_lead = check_lead_duplicated(doc.name, doc.custom_primary_phone)

    # ? SET THE PARENT LEAD NAME
    parent_lead = check_duplicate_lead.get("parent_lead") or None

    # ? IF DUPLICATE LEAD EXISTS
    if parent_lead:

        # ? DELETE THE DUPLICATE DOC
        doc.delete()

        # ? CREATE THE RECORDS IN CHILD TABLE OF THE PARENT DOC
        parent_doc = frappe.get_doc("Lead", parent_lead)

        # ? SET THE CHILD TABLE DOC DATA
        lead_doc = {
            "lead_name": doc.company_name,
            "lead_owner": doc.lead_owner,
            "phone_no": doc.custom_primary_phone,
            "email": parent_doc.email_id,
            "source": doc.source,
            "source_detail": doc.custom_source_details,
            "created_date_and_time": doc.creation,
        }

        # ? SET THE SECONDARY EMAIL
        if parent_doc.email_id != doc.email_id:
            lead_doc["custom_secondary_email"] = doc.email_id

        # ? SET THE DATE RANGE
        child_list = frappe.get_all(
            "Lead Duplicate Details",
            filters={"parent": parent_lead},
            fields=["name", "created_date_and_time"],
            order_by="created_date_and_time desc",
        )

        # ? IF THE CHILD LEAD EXISTS USE IT'S CREATION TIME
        if child_list:
            days_diff = date_diff(
                get_datetime(doc.creation),
                get_datetime(child_list[0].created_date_and_time),
            )
            lead_doc["custom_age__range"] = days_diff

        # ? ELSE USE PARENT'S CREATION TIME
        else:
            days_diff = date_diff(
                get_datetime(doc.creation), get_datetime(parent_doc.creation)
            )
            lead_doc["custom_age__range"] = days_diff

        # ? APPEND THE DUPLICATE DATA INTO CHILD TABLE AND DELETE RECORD
        parent_doc.append("custom_lead_duplicate_details", lead_doc)
        parent_doc.save()
        parent_doc.reload()

        # ! SEND EMAIL TO LEAD OWNER
        # ? DEFINE VARIABLES
        lead_owner_email = frappe.db.get_value(
            "User", doc.lead_owner or parent_doc.lead_owner, "email"
        )
        lead_owner = frappe.db.get_value(
            "User", doc.lead_owner or parent_doc.lead_owner, "full_name"
        )
        company = parent_doc.company
        parent_lead = parent_lead
        lead_link = f"{frappe.utils.get_url()}/app/lead/{parent_lead}"

        # ? LEAD OWNER HTML
        lead_owner_email_html = f"""
            <h1>
                Hello {lead_owner},
            </h1>
            <p>
                The New Duplicate Lead is Created for {company}.
            </p>
            <p>
                Here is the link of the parent lead <a href="{lead_link}">{parent_lead}</a>.
            </p>
            """

        # ? SEND EMAIL
        if lead_owner_email:
            try:
                send_resend_emails(
                    "New Lead!",
                    from_email="marketing@uniflowerp.in",
                    to_emails=lead_owner_email,
                    email_html=lead_owner_email_html,
                )
            except Exception as e:
                print(f"unexpected error {str(e)}")

        # ! SEND EMAIL TO NEW LEAD
        # ? DEFINE VARIABLES
        lead_email = doc.email_id or parent_doc.email
        lead_name = doc.company or parent_doc.lead_name
        company = parent_doc.company

        # ? LEAD OWNER HTML
        lead_owner_email_html = f"""
            <h1>
                Hello {lead_name},
            </h1>
            <p>
                The New Lead is Created for Company: {company}.
            </p>
            """

        # ? SEND EMAIL
        if lead_email:
            try:
                send_resend_emails(
                    "New Lead!",
                    from_email="marketing@uniflowerp.in",
                    to_emails=lead_email,
                    email_html=lead_owner_email_html,
                )
            except Exception as e:
                print(f"unexpected error {str(e)}")
