# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning

class StudentTakeExamWizard(models.TransientModel):
    _name = 'python_odoo8_module.student_take_exam_wizard'
    _description = 'Wizard para que el estudiante realice un examen'

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
        string='Respuestas seleccionadas'
    )

    @api.model
    def default_get(self, fields_list):
        res = super(StudentTakeExamWizard, self).default_get(fields_list)
        student = self.env['python_odoo8_module.student'].search([('user_id','=',self.env.user.id)], limit=1)
        if student:
            res['student_id'] = student.id
        return res

    @api.onchange('exam_id')
    def answers_by_question(self):
        if self.exam_id:
            all_answers = self.env['python_odoo8_module.answer'].search([
                ('question_id.exam_id','=',self.exam_id.id)
            ])
            self.answer_ids = [(6, 0, all_answers.ids)]

    @api.multi
    def submit_exam(self):
        self.ensure_one()
        existing = self.env['python_odoo8_module.result'].search([
            ('exam_id','=',self.exam_id.id),
            ('student_id','=',self.student_id.id)
        ])
        if existing:
            raise Warning("Ya has realizado este examen. No se permiten más intentos.")
        score = sum(ans.point for ans in self.answer_ids if ans.correct)
        self.env['python_odoo8_module.result'].create({
            'exam_id': self.exam_id.id,
            'student_id': self.student_id.id,
            'answer_ids': [(6, 0, self.answer_ids.ids)],
            'score': score
        })
        return {'type': 'ir.actions.act_window_close'}
