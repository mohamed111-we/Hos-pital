from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):  # نموذج المواعيد
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'patient_id'

    ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, tracking=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True, tracking=True)
    appointment_date = fields.Date(string="Appointment Date", tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft', tracking=True)
    notes = fields.Text(string='Notes')
    duration = fields.Float(string="Duration (Hours)")  # مدة الموعد
    fee = fields.Float(string='Appointment Fee')  # رسوم الموعد
    appointment_type = fields.Selection(
        [('consultation', 'Consultation'),  # استشارة
         ('follow_up', 'Follow-up'),  # متابعة
         ('emergency', 'Emergency'),  # طارئ
         ], string='Appointment Type', required=True, default='consultation',
        help="Type of the appointment (e.g., Consultation, Follow-up, Emergency)")
    priority = fields.Selection(
        [('low', 'Low'),                                                    # (منخفضة): موعد روتيني لمتابعة حالة مستقرة
        ('medium', 'Medium'),                                               # (متوسطة): حالة تحتاج إلى تشخيص جديد لكنها ليست طارئة
        ('high', 'High'),                                                   #  حالة طبية حرجة تحتاج إلى تدخل فوري، مثل مريض يعاني من ألم حاد أو نزيف
        ],string='Priority', required=True, default='medium',)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachment')


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref') or vals['ref'] == _('New'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        return super(HospitalAppointment, self).create(vals_list)

    @api.constrains('appointment_date')
    def _check_appointment_date(self):
        for rec in self:
            if rec.appointment_date and rec.appointment_date < fields.Date.today():
                raise ValidationError(_("Appointment date must not be in the past."))

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_confirmed(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_cancelled(self):
        for rec in self:
            rec.state = 'cancelled'
