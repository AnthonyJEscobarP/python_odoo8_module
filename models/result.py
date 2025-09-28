# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

class Result(models.Model):
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
            result.score = sum(ans.point for ans in result.answer_ids if ans.correct)
            
    @api.constrains('exam_id', 'student_id')
    def validate_exam_attempt(self):
        for rec in self:
            # Validacion 1: intento por estudiante
            existing = self.search([
                ('exam_id', '=', rec.exam_id.id),
                ('student_id', '=', rec.student_id.id),
                ('id', '!=', rec.id)
            ])
            if existing:
                raise Warning(_("No tienes mas intentos para este examen."))
            
            # Validacion 2: Inscripcion en la materia
            subject = rec.exam_id.subject_id
            if rec.student_id not in subject.schedule_ids.mapped('student_ids'):
                raise Warning(_("No cuentas con inscripcion en esta materia."))