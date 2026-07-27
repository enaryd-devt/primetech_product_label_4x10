from odoo import _, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_open_barcode_label_layout(self):
        """Open the independent PrimeTech label wizard."""
        products = self
        if not products:
            products = self.browse(self.env.context.get("active_ids", []))
        wizard = self.env["primetech.product.label.layout"].create(
            {"product_tmpl_ids": [(6, 0, products.ids)]}
        )
        return {
            "type": "ir.actions.act_window",
            "name": _("Print Barcodes"),
            "res_model": "primetech.product.label.layout",
            "res_id": wizard.id,
            "view_mode": "form",
            "target": "new",
        }
