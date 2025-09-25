# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from cStringIO import StringIO
from datetime import datetime

class StudentScheduleWizard(models.TransientModel):
    _name = 'python_odoo8_module.student_schedule_wizard'
    _description = 'Wizard para horarios de estudiantes'
    
    student_id = fields.Many2one(
        'python_odoo8_module.student', 
        string='Estudiante',
        required=True
    )
    
    file_data = fields.Binary('PDF data', readonly=True)
    file_name = fields.Char('Archivo', size=64)
    
    @api.model
    def default_get(self, fields_list):
        """Seleccion de estudiante segun el usuario logueado"""
        res = super(StudentScheduleWizard, self).default_get(fields_list)
        
        if self.env.user.has_group('python_odoo8_module.student_role_group'):
            student = self.env['python_odoo8_module.student'].search([
                ('user_id', '=', self.env.user.id)
            ], limit=1)
            if student:
                res['student_id'] = student.id
                
        return res
    
    @api.multi
    def generate_schedule_pdf(self):
        """Generar PDF con horario de estudiantes"""
        for wizard in self:
            student = wizard.student_id
            
            if self.env.user.has_group('python_odoo8_module.student_role_group'):
                if student.user_id != self.env.user:
                    raise Warning("Denegado: Solo puedes generar tu propio horario.")
            
            buffer = StringIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            title_style = styles['Heading1']
            title_style.alignment = 1
            title = Paragraph("HORARIO ACADEMICO", title_style)
            elements.append(title)
            elements.append(Spacer(1, 20))
            
            info_style = styles['BodyText']
            student_info = [
                f"<b>Estudiante:</b> {student.name}",
                f"<b>Carnet:</b> {student.card}",
                f"<b>Grado:</b> {student.grade} - Sección: {student.section}",
                f"<b>Creacion de horario:</b> {datetime.now().strftime('%d/%m/%Y')}"
            ]
            
            for info in student_info:
                elements.append(Paragraph(info, info_style))
            
            elements.append(Spacer(1, 30))
            
            schedules = self.env['python_odoo8_module.schedule'].search([
                ('student_ids', 'in', [student.id])
            ], order='day, hour')
            
            if schedules:
                days_order = {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5}
                days_grouped = {}
                
                for schedule in schedules:
                    day = schedule.day
                    if day not in days_grouped:
                        days_grouped[day] = []
                    days_grouped[day].append(schedule)
                
                sorted_days = sorted(days_grouped.keys(), key=lambda x: days_order.get(x, 6))
                
                for day in sorted_days:
                    day_names = {'monday': 'LUNES', 'tuesday': 'MARTES', 'wednesday': 'MIÉRCOLES', 
                                'thursday': 'JUEVES', 'friday': 'VIERNES'}
                    
                    day_title = Paragraph(f"<b>{day_names.get(day, day.upper())}</b>", styles['Heading2'])
                    elements.append(day_title)
                    elements.append(Spacer(1, 10))
                    
                    schedule_data = [['Hora', 'Materia', 'Profesor', 'Aula']]
                    
                    for schedule in sorted(days_grouped[day], key=lambda x: x.hour):
                        schedule_data.append([
                            schedule.hour,
                            schedule.subject_id.name,
                            schedule.subject_id.teacher_id.name,
                            schedule.classroom_id.name
                        ])
                    
                    table = Table(schedule_data, colWidths=[80, 200, 150, 80])
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                    ]))
                    
                    elements.append(table)
                    elements.append(Spacer(1, 20))
            else:
                no_schedule = Paragraph("El estudiante no cuenta con horarios.", info_style)
                elements.append(no_schedule)
            
            doc.build(elements)
            pdf_data = buffer.getvalue()
            buffer.close()
            
            wizard.write({
                'file_data': base64.b64encode(pdf_data),
                'file_name': f'Horario de {student.name} - {student.card} | {datetime.now().strftime("%Y%m%d")}.pdf'
            })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'python_odoo8_module.student_schedule_wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new',
        }