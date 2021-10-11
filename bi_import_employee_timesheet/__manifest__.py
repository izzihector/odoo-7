# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
	"name" : "Import Employee Timesheet from XLS/CSV File",
	"version" : "14.0.0.1",
	"category" : "Human Resources",
	'summary': "Odoo Employee Timesheet import timesheet from excel import timesheets import multiple employee timesheet import timesheets import attendance import employee attendance import time-sheet import timesheet from csv import employee timesheet from csv file",
	"description": """
	
				timesheet,
				import timesheet,
				import employee timesheet,
				import employee timesheet from xls,
				import employee timesheet from csv,
				import timesheet from xls,
				import timesheet using excel,
				import timesheet xls,
	
	""",
	"author": "BrowseInfo",
	"website" : "https://www.browseinfo.in",
	"price": 10,
	"currency": 'EUR',
	"depends" : ['hr_timesheet','base'],
	"data": [
				"security/ir.model.access.csv",
				'wizard/import_employee_timesheet_view.xml',
				'views/import_employee_timesheet_menu.xml',
			],
	"auto_install": False,
	"installable": True,
	"live_test_url":'https://youtu.be/8HWNzdcpC7Y',
	"images":["static/description/Banner.png"],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
