# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import io
import xlrd
import babel
import logging
import tempfile
import binascii
from io import StringIO
from datetime import date, datetime, time
from odoo import api, fields, models, tools, _
from odoo.exceptions import Warning, UserError, ValidationError
_logger = logging.getLogger(__name__)

try:
	import csv
except ImportError:
	_logger.debug('Cannot `import csv`.')
try:
	import xlwt
except ImportError:
	_logger.debug('Cannot `import xlwt`.')
try:
	import cStringIO
except ImportError:
	_logger.debug('Cannot `import cStringIO`.')
try:
	import base64
except ImportError:
	_logger.debug('Cannot `import base64`.')


class MassCancelPicking(models.TransientModel):
	_name = 'import.employee.timesheet'
	_description = 'Import Employee Timesheet'

	file_type = fields.Selection([('CSV', 'CSV File'),('XLS', 'XLS File')],string='File Type', default='CSV')
	file = fields.Binary(string="Upload File")

	def import_employee_timesheet(self):
		if not self.file:
			raise ValidationError(_("Please Upload File to Import Timesheet !"))

		if self.file_type == 'CSV':
			line = keys = ['date','employee_id','name','project_id','task_id','unit_amount']
			try:
				csv_data = base64.b64decode(self.file)
				data_file = io.StringIO(csv_data.decode("utf-8"))
				data_file.seek(0)
				file_reader = []
				csv_reader = csv.reader(data_file, delimiter=',')
				file_reader.extend(csv_reader)
			except Exception:
				raise ValidationError(_("Please Select Valid File Format !"))
				
			values = {}
			for i in range(len(file_reader)):
				field = list(map(str, file_reader[i]))
				values = dict(zip(keys, field))
				if values:
					if i == 0:
						continue
					else:
						res = self.create_employee_timesheet(values)
		else:
			try:
				file = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
				file.write(binascii.a2b_base64(self.file))
				file.seek(0)
				values = {}
				workbook = xlrd.open_workbook(file.name)
				sheet = workbook.sheet_by_index(0)
			except Exception:
				raise ValidationError(_("Please Select Valid File Format !"))

			for row_no in range(sheet.nrows):
				val = {}
				if row_no <= 0:
					fields = list(map(lambda row:row.value.encode('utf-8'), sheet.row(row_no)))
				else:
					line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
					values.update( {'date':line[0],
							'employee_id': line[1],
							'name': line[2],
							'project_id':line[3],
							'task_id':line[4],
							'unit_amount':line[5],
							})
					res = self.create_employee_timesheet(values)

	def create_employee_timesheet(self, values):
		timesheet = self.env['account.analytic.line']
		date = self.get_date(values.get('date'))
		employee_id = self.get_employee(values.get('employee_id'))
		project_id = self.get_project(values.get('project_id'))
		task_id = self.get_task(values.get('task_id'))
		vals = {
			'date':date,
			'employee_id':employee_id.id,
			'name':values.get('name'),
			'project_id':project_id.id,
			'task_id':task_id.id,
			'unit_amount' : values.get('unit_amount'),
			}
		if ':' in values.get('unit_amount') :
			raise UserError(_('Please Enter Hours in Float !'))
		if project_id.id == task_id.project_id.id:
			res = timesheet.create(vals)
			return res
		else:
			raise UserError(_('"%s" Task not in "%s" Project !') % (task_id.name, project_id.name))


	def get_date(self, date):
		try:
			timesheet_date = datetime.strptime(date, '%Y/%m/%d')
			return timesheet_date
		except Exception:
			raise ValidationError(_('Wrong Date Format ! Date Should be in format YYYY/MM/DD'))

	def get_employee(self, name):
		employee = self.env['hr.employee'].search([('name', '=', name)],limit=1)
		if employee:
			return employee
		else:
			employee_id = self.env['hr.employee'].create({'name':name})
			return employee_id


	def get_project(self, name):
		project = self.env['project.project'].search([('name', '=', name)],limit=1)
		if project:
			return project
		else:
			raise UserError(_('"%s" Project is not found in system !') % name)

	def get_task(self, name):
		task = self.env['project.task'].search([('name', '=', name)],limit=1)
		if task:
			return task
		else:
			raise UserError(_('"%s" Task is not found in system !') % name)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
