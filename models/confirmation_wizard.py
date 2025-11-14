from odoo import fields
from odoo.models import TransientModel
from odoo.exceptions import UserError

class ConfirmationWizard(TransientModel):
    _name = 'confirmation.wizard'
    message = fields.Char(readonly=True)

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['message'] = self.env.context.get('message')
        return res

    def submit(self):
        target_model = self.env.context.get('target_model')
        target_id = self.env.context.get('target_id')
        target_method = self.env.context.get('target_method')
        target_args = self.env.context.get('target_args') or []

        assert type(target_model) is str and type(target_id) is int and type(target_method) is str and type(target_args) is list

        target = self.env[target_model].browse(target_id)
        if not target: raise UserError(f'Target record not found ({target_model = }, {target_id = }).')
        if not hasattr(target, target_method): raise UserError(f'Can\'t access target method ({target_method = }).')
        to_invoke = getattr(target, target_method)
        if callable(to_invoke): to_invoke(*target_args)
