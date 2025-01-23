from odoo import models, fields, api,_

class HospitalPrescription(models.Model):
    _name = 'hospital.prescription'
    _description = 'Hospital Prescription'
    _rec_name = 'medication'

    ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    medication = fields.Char(string='Medication', required=True)  # حقل الدواء
    dosage = fields.Char(string='Dosage', required=True)           # حقل الجرعة
    prescription_date = fields.Date(string='Prescription Date', default=fields.Date.today)  # حقل تاريخ الوصفة
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], string="State", default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref') or vals['ref'] == _('New'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.prescription') or _('New')
        return super(HospitalPrescription, self).create(vals_list)

    def action_confirmed(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_cancelled(self):
        for rec in self:
            rec.state = 'cancelled'
