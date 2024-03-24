from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPaymentInherited(models.Model):
    _inherit = "account.payment"

    bank_charge_amount = fields.Float("Bank Charges" ,compute="compute_bank_charge")
    bank_charge_percentage = fields.Float("Bank Percentage",compute="compute_bank_charge_percent")


    def open_bank_charges(self):
        print("hellooo")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bank Charges',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('move_type', '=', 'entry'),('payment_id', '=', self.id)],
            'target': 'current'
        }

    @api.depends('journal_id')
    def compute_bank_charge_percent(self):
        for rec in self:
            if rec.journal_id.type == 'bank':
                if rec.journal_id.bank_charges_percent:
                    rec.bank_charge_percentage = rec.journal_id.bank_charges_percent
            else:
                rec.bank_charge_percentage = 0

    @api.depends('journal_id','amount')
    def compute_bank_charge(self):
        for rec in self:
            if rec.amount and rec.bank_charge_percentage:
                rec.bank_charge_amount = rec.amount * rec.bank_charge_percentage / 100
            else:
                rec.bank_charge_amount = 0

    def action_post(self):
        print("gggggggg")
        for rec in self:
            if rec.bank_charge_amount > 0:
                if not rec.journal_id.bank_charge_account:
                    raise ValidationError(_("Please add bank charge account in the journal."))
                move_vals = {
                    'ref': rec.ref,
                    'journal_id': rec.journal_id.id,
                    'date': rec.date,
                    'move_type': 'entry',
                    # 'payment_id':self.id,

                    'line_ids': [
                        (0, 0, {
                            'name': 'Bank Charges',
                            'account_id': rec.journal_id.bank_charge_account.id,
                            'debit': rec.bank_charge_amount,
                            'credit': 0.0,
                        }),
                        (0, 0, {
                            'name': 'Bank Charges',
                            # 'account_id': your_account_id_2,
                            'debit': 0.0,
                            'credit': rec.bank_charge_amount,
                        }),
                    ],
                }

                move = self.env['account.move'].create(move_vals)
                move.post()
                move.payment_id = self.id
        return super().action_post()






class PaymentWizard(models.TransientModel):
    _inherit = 'account.payment.register'

    bank_charge_amount = fields.Float("Bank Charges", compute="compute_bank_charge")
    bank_charge_percentage = fields.Float("Bank Percentage", compute="compute_bank_charge_percent")

    @api.depends('journal_id')
    def compute_bank_charge_percent(self):
        for rec in self:
            if rec.journal_id.type == 'bank':
                if rec.journal_id.bank_charges_percent:
                    rec.bank_charge_percentage = rec.journal_id.bank_charges_percent
            else:
                rec.bank_charge_percentage = 0

    @api.depends('journal_id', 'amount')
    def compute_bank_charge(self):
        for rec in self:
            if rec.amount and rec.bank_charge_percentage:
                rec.bank_charge_amount = rec.amount * rec.bank_charge_percentage / 100
            else:
                rec.bank_charge_amount = 0


    # def action_create_payments(self):
    #     for rec in self:
    #         vals = super().action_create_payments()
    #         if rec.bank_charge_amount > 0:
    #             if not rec.journal_id.bank_charge_account:
    #                 raise ValidationError(_("Please add bank charge account in the journal."))
    #             move_vals = {
    #                 'ref': rec.communication,
    #                 'journal_id': rec.journal_id.id,
    #                 'date': rec.payment_date,
    #                 'move_type': 'entry',
    #
    #                 'line_ids': [
    #                     (0, 0, {
    #                         'name': 'Bank Charges',
    #                         'account_id': rec.journal_id.bank_charge_account.id,
    #                         'debit': rec.bank_charge_amount,
    #                         'credit': 0.0,
    #                     }),
    #                     (0, 0, {
    #                         'name': 'Bank Charges',
    #                         # 'account_id': your_account_id_2,
    #                         'debit': 0.0,
    #                         'credit': rec.bank_charge_amount,
    #                     }),
    #                 ],
    #             }
    #
    #             move = self.env['account.move'].create(move_vals)
    #             move.post()
    #     return vals







