from odoo import fields, models, api
from odoo.exceptions import ValidationError


class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color Index")

    @api.constrains('color')
    def _check_color(self):
        for record in self:
            if record.color > 100:
                raise ValidationError("Color Index must be less than 100")