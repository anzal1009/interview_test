from odoo import models, fields, api, _


class AccountingJournalInherit(models.Model):
    _inherit = "account.journal"

    bank_charges_percent = fields.Float("Bank Charge Percentage")
    bank_charge_account = fields.Many2one('account.account',"Bank Charge Account")




