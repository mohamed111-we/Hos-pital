from odoo import models, fields, api, _

class CreateAppointmentWizard(models.TransientModel):
    _name = 'create.appointment.wizard'
    _description = 'Wizard to Create Appointment'


    patient_id = fields.Many2one('hospital.patient', string = 'Patient')
    doctor_id = fields.Many2one('hospital.doctor', string = 'Doctor')
    appointment_date = fields.Date(string="Appointment Date", tracking=True)
    duration = fields.Float(string="Duration (Hours)")  # مدة الموعد
    fee = fields.Float(string='Appointment Fee')  # رسوم الموعد
    notes = fields.Text(string='Notes')

    def action_create_appointment(self):
        self.env['hospital.appointment'].create({
            'patient_id' : self.patient_id.id,
            'doctor_id' : self.doctor_id.id,
            'appointment_date' : self.appointment_date,
            'duration' : self.duration,
            'fee' : self.fee,
            'notes' : self.notes,
            'state': 'draft',
        })