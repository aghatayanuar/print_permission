(() => {
    if (window._patched_print_guard_final) return;
    window._patched_print_guard_final = true;

    let last_route = null;

    frappe.router.on('change', () => {
        const route = frappe.get_route();
        const route_str = frappe.get_route_str();

        if (!route_str.startsWith("print/")) {
            last_route = route;
            return;
        }

        const parts = route;
        const doctype = decodeURIComponent(parts[1] || "");
        const name = decodeURIComponent(parts[2] || "");

        if (!doctype || !name) return;

        frappe.dom.freeze(__("Checking print permission..."));

        frappe.call({
            method: "print_permission.print_permission.print_permission.can_print_doc",
            args: { doctype, name },
            callback: (r) => {
                frappe.dom.unfreeze();

                if (r.exc || r.message === false) {
                    if (last_route) {
                        frappe.set_route(last_route);
                    } else {
                        frappe.set_route("List", doctype);
                    }
                }
            },
            error: () => {
                frappe.dom.unfreeze();
                if (last_route) frappe.set_route(last_route);
            }
        });
    });
})();
