from odoo import models, fields

class EstatePropertyTagInherit(models.Model):
    _inherit = "estate.property.tag"

    priority = fields.Integer(string="Tag Priority", default=0)
    color = fields.Integer(string="Color Index Overide field", required=True)

    # def create(self):
    # 	# put your codes here
    #     return super().create()
    
class SalesOrderInherit(models.Model):
    _inherit = "sale.order"

    client_document_number = fields.Char(string="SO Client Number")

class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    def action_send_msg(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Send Question',
            'res_model': 'send.question',
            'target': 'new',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {'default_user_id': self.id}, 
        }

class SendQuestion(models.TransientModel):
   _name = 'send.question'
   _description = "Send Question"

   user_id = fields.Many2one('res.partner', string="Recipient")
   mobile = fields.Char(related='user_id.mobile', required=True)
   question = fields.Text(string="question", required=True)

   def action_send_question(self):
        print(">>>>>>>>>>>>>>>> hai i am called")