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

class StudentTranscriptWizard(models.TransientModel):
    _name = 'python_odoo8_module.student_transcript_wizard'
    _description = 'Wizard para boleta de calificaciones de estudiantes'
    
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
        res = super(StudentTranscriptWizard, self).default_get(fields_list)
        
        if self.env.user.has_group('python_odoo8_module.student_role_group'):
            student = self.env['python_odoo8_module.student'].search([
                ('user_id', '=', self.env.user.id)
            ], limit=1)
            if student:
                res['student_id'] = student.id
                
        return res
    
    @api.multi
    def generate_transcript_pdf(self):
        """Generar boleta de calificaciones"""
        for wizard in self:
            student = wizard.student_id
            
            if self.env.user.has_group('python_odoo8_module.student_role_group'):
                if student.user_id != self.env.user:
                    raise Warning("Denegado: Solo puedes generar tu propia boleta.")
            
            buffer = StringIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            title_style = styles['Heading1']
            title_style.alignment = 1
            title = Paragraph("BOLETA DE CALIFICACIONES", title_style)
            elements.append(title)
            elements.append(Spacer(1, 20))
            
            info_style = styles['BodyText']
            student_info = [
                "<b>Estudiante:</b> {0}".format(student.name),
                "<b>Carnet:</b> {0}".format(student.card),
                "<b>Email:</b> {0}".format(student.email),
                "<b>Grado:</b> {0}".format(student.grade),
                "<b>Sección:</b> {0}".format(student.section),
                "<b>Creacion de boleta:</b> {0}".format(datetime.now().strftime('%d/%m/%Y'))
            ]
            
            for info in student_info:
                elements.append(Paragraph(info, info_style))
            
            elements.append(Spacer(1, 30))
            
            subjects = self.env['python_odoo8_module.subject'].search([
                ('schedule_ids.student_ids', 'in', [student.id])
            ])
            
            if subjects:
                subtitle = Paragraph("<b>NOTAS</b>", styles['Heading2'])
                elements.append(subtitle)
                elements.append(Spacer(1, 15))
                
                for subject in subjects:
                    subject_header = Paragraph("<b>Materia: {0}</b>".format(subject.name), styles['Heading3'])
                    elements.append(subject_header)
                    
                    exams = self.env['python_odoo8_module.exam'].search([
                        ('subject_id', '=', subject.id)
                    ])
                    
                    if exams:
                        exam_data = [['Examen', 'Puntaje']]
                        total_score = 0
                        exam_count = 0
                        
                        for exam in exams:
                            result = self.env['python_odoo8_module.result'].search([
                                ('exam_id', '=', exam.id),
                                ('student_id', '=', student.id)
                            ], limit=1)
                            
                            if result:
                                exam_data.append([exam.name, str(result.score)])
                                total_score += result.score
                                exam_count += 1
                        
                        if exam_count > 0:
                            promedio = total_score / exam_count
                            exam_data.append(['<b>NOTA FINAL</b>', '<b>{0:.2f}</b>'.format(promedio)])
                            
                            table = Table(exam_data, colWidths=[400, 100])
                            table.setStyle(TableStyle([
                                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('FONTSIZE', (0, 0), (-1, 0), 12),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                            ]))
                            
                            elements.append(table)
                            elements.append(Spacer(1, 20))
                    else:
                        no_exams = Paragraph("Sin exámenes en esta materia.", info_style)
                        elements.append(no_exams)
                        elements.append(Spacer(1, 15))
            else:
                no_subjects = Paragraph("No inscrito en ninguna materia.", info_style)
                elements.append(no_subjects)
            
            doc.build(elements)
            pdf_data = buffer.getvalue()
            buffer.close()
            
            wizard.write({
                'file_data': base64.b64encode(pdf_data),
                'file_name': 'Boleta: {0} - {1} | {2}.pdf'.format(
                    student.name, 
                    student.card, 
                    datetime.now().strftime("%Y%m%d")
                )
            })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'python_odoo8_module.student_transcript_wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new',
        }