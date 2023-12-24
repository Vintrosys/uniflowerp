import frappe

def validate(self, event):

    if not self.get("__islocal") and self.allow == "Company":

        frappe.msgprint("User Permission updating...")

        changing_user_permission(self)

def after_insert(self, event):

    frappe.msgprint("User Permission creation moved to background job, It will complete shortly.")

    frappe.enqueue(create_user_permission, for_value = self.for_value, main_user = self.user, queue = "long")
   
def on_trash(self, event):

    if self.allow == "Company":

        frappe.msgprint("User Permission deletion moved to background job, It will complete shortly.")

        frappe.enqueue(deleting_user_permission, self = self, queue = "long")

def create_user_permission(for_value, main_user, current_doc = None):

    if current_doc:

        user_list = frappe.get_all("User Permission", {"allow": "Company", "for_value": for_value, "name": ["!=", current_doc]}, ["user"], pluck = "user")

    else:

        user_list = frappe.get_all("User Permission", {"allow": "Company", "for_value": for_value}, ["user"], pluck = "user")

    for user in user_list:

        new_doc = frappe.new_doc("User Permission")
        new_doc.user = main_user
        new_doc.allow = "User"
        new_doc.for_value = user

        new_doc.db_insert()

        if main_user != user:

            new_doc = frappe.new_doc("User Permission")
            new_doc.user = user
            new_doc.allow = "User"
            new_doc.for_value = main_user

            new_doc.db_insert()

def changing_user_permission(self):

    old_user = frappe.db.get_value("User Permission", self.name, "user")

    old_for_value =  frappe.db.get_value("User Permission", self.name, "for_value")
    
    if self.user != old_user or self.for_value != old_for_value:

        user_permission_list = frappe.get_all("User Permission", {"user": old_user, "allow": "User"}, ["name"], pluck = "name")

        user_permission_list += frappe.get_all("User Permission", {"for_value": old_user, "allow": "User"}, ["name"], pluck = "name")

        for user_permission in user_permission_list:

            frappe.delete_doc("User Permission", user_permission, delete_permanently = True)

        create_user_permission(for_value = self.for_value, main_user = self.user, current_doc = self.name)

        new_doc = frappe.new_doc("User Permission")
        new_doc.user = self.user
        new_doc.allow = "User"
        new_doc.for_value = self.user

        new_doc.db_insert()

def deleting_user_permission(self):

    user_permission_list = frappe.get_all("User Permission", {"user": self.user, "allow": "User"}, ["name"], pluck = "name")

    user_permission_list += frappe.get_all("User Permission", {"for_value": self.for_value, "allow": "User"}, ["name"], pluck = "name")

    user_permission_list += frappe.get_all("User Permission", {"user": self.for_value, "allow": "User"}, ["name"], pluck = "name")

    user_permission_list += frappe.get_all("User Permission", {"for_value": self.user, "allow": "User"}, ["name"], pluck = "name")

    for user_permission in user_permission_list:

        frappe.delete_doc("User Permission", user_permission, delete_permanently = True)