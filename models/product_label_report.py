from odoo import api, models


class ReportProductLabelCustom(models.AbstractModel):
    _name = "report.primetech_product_label_4x10.report_product_label_custom"
    _description = "Étiquettes produits PrimeTech"

    @api.model
    def _get_report_values(self, docids, data=None):
        data = data or {}
        wizard = self.env["primetech.product.label.layout"].browse(data.get("wizard_id")).exists()
        wizard.ensure_one()
        layouts = {
            # format: (colonnes, lignes, hauteur imprimable en millimètres)
            "dymo": (1, 1, 99.0),       # A7 : 105 - 2 x 3 mm
            "2x7xprice": (2, 7, 204.0), # A5 : 210 - 2 x 3 mm
            "4x7xprice": (4, 7, 291.0),
            "4x12": (4, 12, 291.0),
            "4x12xprice": (4, 12, 291.0),
            "zpl": (1, 1, 142.5),       # A6 : 148,5 - 2 x 3 mm
            "zplxprice": (1, 1, 142.5),
            "4x10xprice": (4, 10, 291.0),
        }
        columns, rows, page_height_mm = layouts[wizard.print_format]
        labels = [
            product
            for product in wizard.product_tmpl_ids
            for _index in range(wizard.quantity)
        ]
        page_size = columns * rows
        pages = []
        for start in range(0, len(labels), page_size):
            page = labels[start : start + page_size]
            page += [False] * (page_size - len(page))
            pages.append([page[index : index + columns] for index in range(0, page_size, columns)])
        prices = {}
        currencies = {}
        for product in wizard.product_tmpl_ids:
            if wizard.pricelist_id:
                prices[product.id] = wizard.pricelist_id._get_product_price(product, 1.0)
                currencies[product.id] = wizard.pricelist_id.currency_id
            else:
                prices[product.id] = product.list_price
                currencies[product.id] = product.currency_id
        return {
            "doc_ids": wizard.ids,
            "doc_model": wizard._name,
            "docs": wizard,
            "wizard": wizard,
            "pages": pages,
            "columns": columns,
            "rows": rows,
            "price_included": "xprice" in wizard.print_format,
            "prices": prices,
            "currencies": currencies,
            "page_height_mm": page_height_mm,
            # border-spacing ajoute un espace avant/après chaque ligne.
            "label_height_mm": (page_height_mm - (rows + 1)) / rows,
        }
