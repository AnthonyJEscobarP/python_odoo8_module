# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

class Question(models.Model):
    _name = 'python_odoo8_module.question'
    _description = 'Modelo de preguntas para examenes'

    exam_id = fields.Many2one(
        'python_odoo8_module.exam', 
        string='Examen', 
        required=True
    )
    
    sentence = fields.Char(
        'Pregunta', 
        required=True
    )
    
    answer_ids = fields.One2many(
        'python_odoo8_module.answer', 
        'question_id', 
        string='Respuestas'
    )
