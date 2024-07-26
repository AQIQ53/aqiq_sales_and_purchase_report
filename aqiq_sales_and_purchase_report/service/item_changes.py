import frappe

@frappe.whitelist()
def item_before_insert(self):
    this_doc=frappe.get_doc("Item",self)
    company = frappe.get_doc("Company", this_doc.custom_company)
    this_doc.taxes = []
    for d in company.custom_item_tax_default:
        this_doc.append(
            "taxes",
            {
                "item_tax_template": d.item_tax_template,
                "tax_category": d.tax_category,
                "valid_from": d.valid_from,
                "minimum_net_rate": d.minimum_net_rate,
                "maximum_net_rate": d.maximum_net_rate,
            },
        )
    return company.custom_item_tax_default