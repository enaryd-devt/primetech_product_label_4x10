from odoo import fields, models


class ProductLabelLayout(models.TransientModel):
    """Add a 4 by 10, price-bearing layout to Odoo's label wizard."""

    _inherit = "product.label.layout"

    print_format = fields.Selection(
        selection_add=[("4x10xprice", "4 x 10 with price")],
        ondelete={"4x10xprice": "set default"},
    )

    def _prepare_report_data(self):
        """Use the zero-margin report action for the custom label format.

        Odoo's base implementation parses the selection key and prepares the
        4-column/10-row grid as well as ``price_included``. Keeping that logic
        in the base module preserves product-variant and quantity support.
        """
        xml_id, data = super()._prepare_report_data()
        if self.print_format == "4x10xprice":
            xml_id = (
                "primetech_product_label_4x10."
                "action_report_product_label_4x10_price"
            )
            # Keep the custom layout stable if the base parser changes later.
            data.update(columns=4, rows=10, price_included=True)
        return xml_id, data
