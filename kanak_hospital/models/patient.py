from odoo import api, fields, models
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class HospitalPatient(models.Model):
	_name = "hospital.patient"
	_description = "Hospital Patient"

	name = fields.Char(string="Name")
	ref = fields.Char(string="Reference")
	gender = fields.Selection([('male', 'Male'),('female','Female')], string="Patient Gender")
	dob = fields.Date(string="Date of Birth")
	appointment_count = fields.Integer(string="Total Appointment",compute='_compute_appointment_count')
	appointment_ids=fields.One2many('hospital.appointment','patient_id', string="Details")
	image = fields.Binary("Image")
	stage = fields.Many2one('crm.stage', group_expand = '_read_group_stage_ids')

	def _compute_appointment_count(self):		
		appointment_count = self.env['hospital.appointment'].search_count([('patient_id','=',self.id),('state','=','done')])
		self.appointment_count = appointment_count	

	def action_open_appointment(self):
		action = self.env['ir.actions.actions']._for_xml_id("kanak_hospital.action_hospital_patient")
		action['context'] = {
			'default_patient_id': self.id
		}
		action['domain'] = [('patient_id','=',self.id)]
		opp_ids = self.env['hospital.appointment'].search([('patient_id','=',self.id),('state','=','done')])
		if len(opp_ids) == 1:
			action = self.env['ir.actions.actions']._for_xml_id("kanak_hospital.action_hospital_appointment")
			action['res_id'] = opp_ids.id
			action['views'] = [(self.env.ref('kanak_hospital.view_hospital_appointment_form').id,'form')]		
		else:
			action = self.env['ir.actions.actions']._for_xml_id("kanak_hospital.action_hospital_appointment")
			action['domain'] = [('patient_id','=',self.id),('state','=','done')]
			action['view_id'] = self.env.ref('kanak_hospital.view_hospital_patient_tree').id
		return action

	def action_test(self):
		return

	@api.model
	def _read_group_stage_ids(self,stages,domain,order):
	    stage_ids = self.env['crm.stage'].search([])
	    return stage_ids