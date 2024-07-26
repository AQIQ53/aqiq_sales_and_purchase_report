# Copyright (c) 2024, Aqiq Sales And Purchase Report and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.desk.reportview import build_match_conditions
from frappe.utils import cstr, getdate


def execute(filters=None):
    if not filters:
        filters = {}
    columns = get_columns()
    conditions = get_conditions(filters)
    query_data = get_data(conditions)
    data = []

    for d in query_data:
        row = {}
        row["supplier_name"] = d.get("supplier_name")
        row["etr_sno"] = filters.get("etr_sno")
        row["supp_inv_date"] = d.get("supp_inv_date")
        row["supp_inv"] = d.get("supp_inv")
        row["custom_description"] = d.get("custom_description")
        row["commercial_inv"] = ""
        row["custom_customs_entry"] = d.get("custom_customs_entry")
        row["custom_exit_border"] = d.get("custom_exit_border")
        row["custom_destination"] = d.get("custom_destination")
        row["production"] = d.get("production")
        row["custom_destination"] = d.get("custom_destination")
        if d.is_return == 1:
            row["base_net_amount"] = -abs(d.get("base_net_amount"))
        else:
            row["base_net_amount"] = d.get("base_net_amount")
        row["return_against"] = d.get("return_against")
        row["cnote_date"] = d.get("cnote_date")
        data.append(row)

    return columns, data


def get_columns():

    columns = [
        {
            "fieldname": "supplier_name",
            "label": _("supplier"),
            "fieldtype": "Data",
            "options": "Purchase Invoice",
            "width": 150,
        },
        {
            "fieldname": "etr_sno",
            "label": _("etr serial no"),
            "fieldtype": "Data",
            "options": "Purchase Invoice",
            "width": 150,
        },
        {
            "fieldname": "supp_inv_date",
            "label": _("date"),
            "fieldtype": "Date",
            "options": "Purchase Invoice",
            "width": 150,
        },
        {
            "fieldname": "supp_inv",
            "label": _("inv no"),
            "fieldtype": "Data",
            "options": "Purchase Invoice",
            "width": 150,
        },
        {
            "fieldname": "custom_description",
            "label": _("desc"),
            "fieldtype": "Data",
            "options": "Doctype",
            "width": 150,
        },
        {
            "fieldname": "commercial_inv",
            "label": _("commercial inv"),
            "fieldtype": "Data",
            "options": "Purchase Invoice",
            "width": 150,
        },
        {
            "fieldname": "custom_customs_entry",
            "label": _("customs entyry no"),
            "fieldtype": "Data",
            "options": "Purchase Invoice",
            "width": 150,
        },
        {
            "fieldname": "custom_exit_border",
            "label": _("exit border"),
            "fieldtype": "Data",
            "options": "Purchase Invoice",
            "width": 150,
        },
        {
            "fieldname": "custom_destination",
            "label": _("custom_destination"),
            "fieldtype": "Data",
            "options": "Purchase Invoice",
            "width": 150,
        },
        {
            "fieldname": "prod_category",
            "label": _("production category"),
            "fieldtype": "Data",
            "options": "Purchase Invoice",
            "width": 150,
        },
        {
            "fieldname": "base_net_amount",
            "label": _("amount excl"),
            "fieldtype": "Currency",
            "options": "Purchase Invoice",
            "width": 150,
        },
        {
            "fieldname": "return_against",
            "label": _("credit note allocation"),
            "fieldtype": "Data",
            "options": "Purchase Invoice",
            "width": 150,
        },
        {
            "fieldname": "cnote_date",
            "label": _("cnote date"),
            "fieldtype": "Date",
            "options": "Purchase Invoice",
            "width": 150,
        },
    ]

    return columns


def get_data(conditions):

    data = frappe.db.sql(
        """select s.bill_no as supp_inv, s.bill_date as supp_inv_date,c.custom_company, s.supplier_name as supplier_name, s.posting_date as posting_date, s.name as name,
			s.return_against return_against, s.is_return as is_return, (select posting_date from `tabPurchase Invoice` where name=s.return_against) as cnote_date,
			s.custom_exit_border as custom_exit_border, s.custom_destination as custom_destination, s.custom_description as custom_description, s.custom_customs_entry as custom_customs_entry, SUM(i.base_net_amount) as base_net_amount 
		 	from `tabPurchase Invoice` s 
			inner join `tabPurchase Invoice Item` i on s.name = i.parent
			inner join `tabSupplier` c on s.supplier = c.name
			where s.docstatus=1 {} and c.custom_unregistered=0 and c.custom_import_vat=0 and i.item_tax_template IN ('Zero Rated - IG', 'Zero Rated - IAL' ) group by s.name order by s.posting_date DESC""".format(
            conditions
        ),
        as_dict=1,
    )
    return data


def get_conditions(filters):
    conditions = ""
    if filters.get("custom_company"):
        conditions += " and c.custom_company =  '{}' ".format(filters.get("custom_company"))
    if filters.get("supplier"):
        conditions += " and supplier =  '{}' ".format(filters.get("supplier"))
    if filters.get("month"):
        conditions += " and MONTHNAME(posting_date) = '{}' ".format(
            filters.get("month")
        )
    if filters.get("fiscal_year"):
        fyr_start_date = frappe.db.get_value(
            "Fiscal Year", filters.get("fiscal_year"), "year_start_date"
        )
        fiscal_year = getdate(fyr_start_date).year
        conditions += " and YEAR(posting_date) =  '{}' ".format(fiscal_year)

    return conditions
