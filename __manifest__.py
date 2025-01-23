{
    'name': 'Hospital',
    'version': '17.0',
    'author': 'Arafa',
    'category': 'Healthcare',
    'summary': 'Manage hospital operations, patients, doctors, and appointments.',
    'description': """
        Hospital Management System
        ==========================
        This module is designed to manage hospital operations including:
        - Patient management
        - Doctor management
        - Appointment scheduling
        - Medical records
    """,
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/patient_view.xml',
        'views/appointment_view.xml',
        'views/doctor_view.xml',
        'views/prescription_view.xml',
        'views/doctor_certificate_view.xml',


        'reports/patient_report.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
