from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    name = fields.Char(string='Full Name', required=True)
    image = fields.Binary("Image")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", default='male', tracking=True)
    state = fields.Selection([
        ('new', 'New'),                   #جديد
        ('consulting', 'Consulting'),     #استشاره
        ('treatment', 'Under Treatment'), #تحت العلاج
        ('discharged', 'Discharged'),     #تم اخراجه
    ], string="Health Status", default='new', tracking=True)
    birth_day = fields.Date(string='Birthday', required=True)
    age = fields.Integer(string='Age', compute='_compute_age', readonly=True, )
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    # الحقول الصحية
    blood_type = fields.Selection(
        [('a+', 'A+'),
         ('a-', 'A-'),
         ('b+', 'B+'),
         ('b-', 'B-'),
         ('ab+', 'AB+'),
         ('ab-', 'AB-'), ('o+', 'O+'),
         ('o-', 'O-')],
        string='Blood Type')
    current_health_status = fields.Selection(
        [('stable', 'Stable'),  # مستقر
         ('critical', 'Critical'),  # حرج
         ('improving', 'Improving')],  # في تحسن
        string='Health Status', tracking=True)
    allergies = fields.Text(string='Allergies')  # الحساسية للأدوية
    active = fields.Boolean(default=True)
    # جهات الاتصال في حالة الطوارئ
    emergency_contact_name = fields.Char(string='Emergency Contact Name')
    emergency_contact_number = fields.Char(string='Emergency Contact Number')
    emergency_contact_relation = fields.Selection(
        [('parent', 'Parent'),  # الوالدين
         ('sibling', 'Sibling'), # أخ أو أخت
         ('spouse', 'Spouse'),  # زوج
         ('friend', 'Friend')   # صديق
         ], string='Relation')
    prescription_id= fields.Many2many('hospital.prescription', string='Prescription')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointment')
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for record in self:
            record.appointment_count = len(record.appointment_ids)


    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if not record.phone.isdigit():
                raise ValidationError("Phone number must contain only digits.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref') or vals['ref'] == _('New'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        return super(HospitalPatient, self).create(vals_list)

    @api.depends('birth_day')
    def _compute_age(self):
        for record in self:
            if record.birth_day:
                today = fields.date.today()
                birth_date = record.birth_day
                record.age = today.year - birth_date.year - (
                        (today.month, today.day) < (birth_date.month, birth_date.day))
            else:
                record.age = 1

    def action_consulting(self):
        for rec in self:
            rec.state = 'consulting'

    def action_treatment(self):
        for rec in self:
            rec.state = 'treatment'

    def action_discharged(self):
        for rec in self:
            rec.state = 'discharged'

    def action_view_appointment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }
