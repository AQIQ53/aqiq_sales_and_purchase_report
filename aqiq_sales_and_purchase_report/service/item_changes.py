import frappe

@frappe.whitelist()
def item_before_insert(self,name):
    company = frappe.get_doc("Company", self)
    
    # Clear existing taxes table entries
    frappe.db.sql("""DELETE FROM `tabItem Tax` WHERE parent = %s""", (name))

    # Iterate over the fetched data and insert into the taxes child table
    print(name)
    print(self)
    print(company.custom_item_tax_default)
    for tax in company.custom_item_tax_default:  # Assuming tax_details is a list of dictionaries containing the tax information
        tax_entry = frappe.get_doc({
            "doctype": "Item Tax",
            "item_tax_template": tax["item_tax_template"],
            "tax_category": tax["tax_category"],
            "valid_from": tax["valid_from"],
            "minimum_net_rate": tax["minimum_net_rate"],
            "maximum_net_rate": tax["maximum_net_rate"],
            "parent": name,
            "parentfield": "taxes",
            "parenttype": "Item"
        })
        print(tax_entry)
        tax_entry.insert(ignore_mandatory=True)
        

    # Commit the transaction to save the changes
    
    frappe.db.commit()
    return company.custom_item_tax_default
