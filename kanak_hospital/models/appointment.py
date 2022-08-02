from odoo import fields, models, api, SUPERUSER_ID, _
from datetime import date
from odoo.exceptions import ValidationError
from datetime import timedelta
import random


class HospitalAppointment(models.Model):
	_name = "hospital.appointment"
	_description = "Hospital Appointment"
	_rec_name='patient_id'

	patient_id = fields.Many2one('hospital.patient',string="Patient Name", tracking=2)
	doctor_id = fields.Many2one('hospital.doctor',string="Doctor Assign")	
	appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now, tracking=1 )
	booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today, tracking=3)
	spec = fields.Char(string="Name",related="doctor_id.specialist")
	ref = fields.Char(string="Reference",related="patient_id.ref" ) 
	charges = fields.Integer(string="Charges", related="doctor_id.charges")
	image = fields.Binary("Image",related="patient_id.image")
	state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('done','Done'),('cancel','Cancelled')], default='draft', string="status", group_expand = '_expand_states')

	def action_confirm(self):
		for rec in self:
			rec.state = 'confirm'

	def action_done(self):
		for rec in self:
			rec.state = 'done'

	def action_draft(self):
		for rec in self:
			rec.state = 'draft'

	def action_cancel(self):
		for rec in self:
			rec.state='cancel'

	def _expand_states(self, states, domain, order):
	    return [key for key, val in type(self).state.selection]