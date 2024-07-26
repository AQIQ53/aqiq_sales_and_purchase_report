import frappe

@frappe.whitelist()
def item_before_insert(self):
    this_doc=frappe.get_doc("Item",self)
    company = frappe.get_doc("Company", this_doc.custom_company)
    return company.custom_item_tax_default