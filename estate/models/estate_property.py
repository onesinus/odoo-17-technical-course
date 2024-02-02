from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class EstateProperty(models.Model):
	_name = "estate.property"
	_description = "Estate Property"
	_order = "date_availability desc"

	_sql_constraints = [
	    (
	        'unique_name', 
	        'UNIQUE(name)', 
	        'The name must be unique'
	    )
	]

	@api.constrains('selling_price')
	def _check_selling_price(self):
	    for record in self:
	        if record.selling_price < 1:
	            raise ValidationError("The selling price must be greater than 0")

	@api.depends("living_area", "garden_area")
	def _compute_total_area(self):
	    for prop in self:
	        prop.total_area = prop.living_area + prop.garden_area

	@api.onchange("garden")
	def _onchange_garden(self):
	    if self.garden:
	        self.garden_area = 10
	        self.garden_orientation = "N"
	    else:
	        self.garden_area = 0
	        self.garden_orientation = False

	name = fields.Char(required=True)
	description = fields.Text(default="Estate Property Description")
	postcode = fields.Char()
	date_availability = fields.Date(default=fields.Datetime.now)
	expected_price = fields.Float()
	selling_price = fields.Float(default=1000000)
	bedrooms = fields.Integer()
	living_area = fields.Integer()
	facades = fields.Integer()
	garage = fields.Boolean()
	garden = fields.Boolean()
	garden_area = fields.Integer()
	garden_orientation = fields.Selection(
	    selection=[ ("N", "North"), ("S", "South"), ("E", "East"),  ("W", "West"),],
	    string="Garden Orientation",
	)
	last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)

	user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
	buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
	total_area = fields.Integer(readonly=True, compute="_compute_total_area")
	state = fields.Selection(
	    selection=[
	        ("new", "New"),
	        ("ready", "Ready"),
	        ("offer_received", "Offer Received"),
	        ("offer_accepted", "Offer Accepted"),
	        ("sold", "Sold"),
	        ("canceled", "Canceled"),
	    ],
	    string="Status",
	    required=True,
	    copy=False,
	    default="new",
	)

	def action_sold(self):
	    if "canceled" in self.mapped("state"):
	        raise UserError("Canceled properties cannot be sold.")
	    return self.write({"state": "sold"})

	def action_cancel(self):
	    if "sold" in self.mapped("state"):
	        raise UserError("Sold properties cannot be canceled.")
	    return self.write({"state": "canceled"})

	@api.model
	def create(self, vals):
	    if vals.get("selling_price") and vals.get("date_availability"):
	        vals["state"] = "ready"
	    return super().create(vals)

	def unlink(self):
	    if not set(self.mapped("state")) <= {"new", "canceled"}:
	        raise UserError("Only new and canceled state can be deleted.")
	    return super().unlink()

	def update_state_schedule(self):
		if not self.date_availability:
			self.env["estate.property"].search([]).write({"state": "canceled"})