{
    "name": "Product Labels 4 x 10 with Price",
    "summary": "Print 40 marginless product labels with sales prices on A4 paper",
    # Keep the description in the manifest: the legacy repository README is
    # UTF-16 and must never be decoded by Odoo as the module description.
    "description": "Print product labels in a 4-column by 10-row A4 layout with prices.",
    "version": "18.0.1.0.0",
    "category": "Sales/Products",
    "author": "PrimeTech",
    "license": "LGPL-3",
    "depends": ["product"],
    "data": ["report/product_label_templates.xml"],
    "installable": True,
    "application": False,
}
