from odoo import _, fields, models
from odoo.exceptions import UserError


class PrimetechProductLabelLayout(models.TransientModel):
    """Assistant indépendant de mise en page des étiquettes PrimeTech."""

    _name = "primetech.product.label.layout"
    _description = "Mise en page des étiquettes produits PrimeTech"

    quantity = fields.Integer(string="Quantité par produit", default=1, required=True)
    print_format = fields.Selection(
        [
            ("dymo", "Dymo"),
            ("2x7xprice", "2 x 7 avec le prix"),
            ("4x7xprice", "4 x 7 avec le prix"),
            ("4x12", "4 x 12"),
            ("4x12xprice", "4 x 12 avec le prix"),
            ("zpl", "Étiquettes ZPL"),
            ("zplxprice", "Étiquettes ZPL avec prix"),
            ("4x10xprice", "4 x 10 avec le prix"),
        ],
        string="Format d'impression",
        default="4x10xprice",
        required=True,
    )
    product_tmpl_ids = fields.Many2many(
        "product.template",
        string="Produits",
        required=True,
    )
    pricelist_id = fields.Many2one("product.pricelist", string="Liste de prix")
    extra_html = fields.Html(string="Contenu supplémentaire")

    def action_print(self):
        self.ensure_one()
        if self.quantity <= 0:
            raise UserError(_("La quantité d'étiquettes doit être supérieure à zéro."))
        if not self.product_tmpl_ids:
            raise UserError(_("Sélectionnez au moins un produit."))
        report = self.env["ir.actions.report"].search(
            [("report_name", "=", "primetech_product_label_4x10.report_product_label_custom")],
            limit=1,
        )
        if not report:
            raise UserError(_("Le rapport PDF d'étiquettes PrimeTech n'est pas installé."))
        return report.report_action(self, data={"wizard_id": self.id})
