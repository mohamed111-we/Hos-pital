from odoo import models, fields, api, _

# الوصف: قائمة بالشهادات والاعتمادات التي حصل عليها الطبيب.

class HospitalDoctorCertificate(models.Model):
    _name = 'hospital.doctor.certificate'
    _description = 'Doctor Certificate'


    name = fields.Char(string='Certificate Name', required=True)   #  اسم الشهادة.
    date_awarded = fields.Date(string='Date Awarded')              #   تاريخ الحصول عليها
    issuing_authority = fields.Char(string='Issuing Authority')    #  الجهة المانحة.
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
