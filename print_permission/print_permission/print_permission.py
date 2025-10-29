import frappe
from frappe import _
from frappe.www import printview

original_get_html_and_style = printview.get_html_and_style

def before_print_check(doc, print_format=None, style=None, as_pdf=False, check_only=False):
    settings = frappe.get_single("Print Limit Settings")

    if getattr(settings, "disable_print_limit", 0):
        return

    user = frappe.session.user
    doctype = doc.doctype
    name = doc.name

    rule = next((d for d in settings.max_print_doc if d.document == doctype), None)
    if not rule or not rule.limit_per_doc:
        return

    limit = rule.limit_per_doc

    printed_count = frappe.db.count(
        "Print Log",
        filters={"ref_doctype": doctype, "ref_name": name}
    )

    if printed_count >= limit:
        frappe.throw(
            _("Print limit reached for {0} {1}. Allowed: {2}").format(doctype, name, limit)
        )

    if not check_only:
        frappe.get_doc({
            "doctype": "Print Log",
            "ref_doctype": doctype,
            "ref_name": name,
            "printed_by": user
        }).insert(ignore_permissions=True)



@frappe.whitelist()
def can_print_doc(doctype, name):
    doc = frappe.get_doc(doctype, name)
    before_print_check(doc, check_only=True)
    return True

