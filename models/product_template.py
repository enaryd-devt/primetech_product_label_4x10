from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_open_barcode_label_layout(self):
        """Open Odoo's quantity/format wizard from the barcode button."""
        self.ensure_one()
        # Both entry points intentionally share one complete wizard so all PDF
        # and ZPL formats, quantities, pricelists and extra content stay in
        # sync with Odoo's supported product-label workflow.
        return self.action_open_label_layout()
