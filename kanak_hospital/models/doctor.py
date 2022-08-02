from odoo import api, fields, models
from datetime import date


class HospitalDoctor(models.Model):
	_name = "hospital.doctor"
	_description = "Hospital Doctor"

	name = fields.Char(string="Name", copy=False)
	specialist = fields.Char(string="Specialist", copy=False)
	dob = fields.Date(string="Date of Birth")
	patient_id = fields.Many2one('hospital.patient',string="Patient Name")
	charges = fields.Integer(string="Charge")
	gender = fields.Selection([('male', 'Male'),('female','Female')], string="Doctor Gender")
	image = fields.Binary("Image")