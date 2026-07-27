from odoo import fields, models


class ProductLabelLayout(models.TransientModel):
    """Add a 4 by 10, price-bearing layout to Odoo's label wizard."""

    _inherit = "product.label.layout"

    print_format = fields.Selection(
        selection_add=[("4x10xprice", "4 x 10 with price")],
        # This is a transient wizard: deleting its rows is the only reliable
        # uninstall policy. ``set default`` prevents the registry from loading
        # on Odoo releases where print_format has no model-level default.
        ondelete={"4x10xprice": "cascade"},
    )

    def _prepare_report_data(self):
        """Set the dimensions expected by Odoo's standard label report.

        Odoo's base implementation prepares the products and quantities, but
        it also derives ``product.report_product_template_label_4x10`` from the
        new format. That external ID does not exist in the product module, so
        the custom action must replace it before ``process`` resolves it.
        """
        xml_id, data = super()._prepare_report_data()
        if self.print_format == "4x10xprice":
            xml_id = (
                "primetech_product_label_4x10."
                "action_report_product_label_4x10_price"
            )
            data.update(columns=4, rows=10, price_included=True)
        return xml_id, data
