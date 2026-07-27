from odoo import _, fields, models
from odoo.exceptions import UserError


class PrimetechProductLabelLayout(models.TransientModel):
    """Independent quantity and format wizard for PrimeTech labels."""

    _name = "primetech.product.label.layout"
    _description = "PrimeTech Product Label Layout"

    quantity = fields.Integer(string="Quantity per product", default=1, required=True)
    print_format = fields.Selection(
        [
            ("dymo", "Dymo"),
            ("2x7xprice", "2 x 7 with price"),
            ("4x7xprice", "4 x 7 with price"),
            ("4x12", "4 x 12"),
            ("4x12xprice", "4 x 12 with price"),
            ("zpl", "ZPL Labels"),
            ("zplxprice", "ZPL Labels with price"),
            ("4x10xprice", "4 x 10 with price"),
        ],
        string="Format",
        default="4x10xprice",
        required=True,
    )
    product_tmpl_ids = fields.Many2many(
        "product.template",
        string="Products",
        required=True,
    )
    pricelist_id = fields.Many2one("product.pricelist", string="Pricelist")
    extra_html = fields.Html(string="Additional content")

    def action_print(self):
        self.ensure_one()
        if self.quantity <= 0:
            raise UserError(_("The label quantity must be greater than zero."))
        if not self.product_tmpl_ids:
            raise UserError(_("Select at least one product."))
        report = self.env["ir.actions.report"].search(
            [("report_name", "=", "primetech_product_label_4x10.report_product_label_custom")],
            limit=1,
        )
        if not report:
            raise UserError(_("The PrimeTech label PDF report is not installed."))
        return report.report_action(self, data={"wizard_id": self.id})
