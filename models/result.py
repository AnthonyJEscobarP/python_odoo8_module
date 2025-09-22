# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

class result(models.Model):
    _name = 'python_odoo8_module.result'
    _description = 'Modelo de resultados de examen'

    exam_id = fields.Many2one(
        'python_odoo8_module.exam', 
        string='Examen', 
        required=True
    )
    
    student_id = fields.Many2one(
        'python_odoo8_module.student',
        string='Estudiante', 
        required=True
    )
    
    answer_ids = fields.Many2many(
        'python_odoo8_module.answer', 
        string='Respuestas'
    )
    
    score = fields.Integer('Puntuacion', compute='get_exam_score', store=True)

    @api.depends('answer_ids')
    def get_exam_score(self):
        for result in self:
            result.score = sum(ans.points for ans in result.answer_ids if ans.correct)
            
    @api.constrains('exam_id', 'student_id')
    def one_try_by_student(self):
        for rec in self:
            existing = self.search([
                ('exam_id', '=', rec.exam_id.id),
                ('student_id', '=', rec.student_id.id),
                ('id', '!=', rec.id)
            ])
            if existing:
                raise Warning(_("No tienes mas intentos para este examen."))
        
    @api.constrains('exam_id', 'student_id')
    def validate_inscription(self):
        for rec in self:
            subject = rec.exam_id.subject_id
            if rec.student_id not in subject.itinerary_ids.mapped('student_ids'):
                raise Warning(_("No cuentas con inscripcion en esta materia."))