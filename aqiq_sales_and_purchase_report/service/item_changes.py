import frappe

@frappe.whitelist()
def item_before_insert(self):
    company = frappe.get_doc("Company", self)
    return company.custom_item_tax_default