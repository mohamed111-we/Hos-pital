from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    name = fields.Char(string='Full Name', required=True, default='Dr/ ')
    image = fields.Binary("Image")
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", default='male', tracking=True)
    state = fields.Selection(
        [('available', 'Available'),  # متاح
        ('on_leave', 'On Leave'),  # في إجازة
        ('retired', 'Retired'),  # متقاعد
        ],string='Status', default='available',tracking=True, )
    specialization = fields.Selection(  # التخصص
        [('general', 'General'),  # عام
         ('surgery', 'Surgery'),  # جراحة
         ('cardiology', 'Cardiology'),  # أمراض القلب
         ('pediatrics', 'Pediatrics')  # طب الأطفال
         ], string='Specialization',)
    years_of_experience = fields.Integer(string='Years of Experience',  help='Number of years the doctor has been practicing.')
    # تكلفه الخدمات
    service_fee = fields.Float(string='Consultation Fee',)  # تكلفة الاستشارة
    surgery_fee = fields.Float(string='Surgery Fee')                      # تكلفة الجراحة
    examination_fee = fields.Float(string='Examination Fee')              # تكلفة الفحص
    anesthesia_fee = fields.Float(string='Anesthesia Fee')                # تكلفة التخدير
    # طريقه الدفع
    payment_method = fields.Selection([
        ('cash', 'Cash'),  # نقدي
        ('credit_card', 'Credit Card'),  # بطاقة ائتمان
        ('insurance', 'Health Insurance'),  # تأمين صحي
        ('any', 'Any Payment Method')  # أي طريقة دفع
    ], string='Payment Method', default='any')
    certificate_ids = fields.One2many('hospital.doctor.certificate', 'doctor_id', string='Certificates')                # التخصصات والخبرات
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id', string='Appointment')
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for record in self:
            record.appointment_count = len(record.appointment_ids)


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref') or vals['ref'] == _('New'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.doctor') or _('New')
        return super(HospitalDoctor, self).create(vals_list)


    def action_on_leave(self):
        for rec in self:
            rec.state = 'on_leave'

    def action_retired(self):
        for rec in self:
            rec.state = 'retired'

    @api.constrains('years_of_experience')
    def check_years_of_experience(self):
        for record in self:
            if record.years_of_experience <= 0:
                raise ValidationError(_("Please set a Years of Experience positive rounding value."))

    def action_view_appointment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'tree,form',
            'domain': [('doctor_id', '=', self.id)],
        }
