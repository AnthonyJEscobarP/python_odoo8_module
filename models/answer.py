# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

class Answer(models.Model):
    _name = 'python_odoo8_module.answer'
    _description = 'Modelo de respuestas para examen'

    question_id = fields.Many2one(
        'python_odoo8_module.question', 
        string='Pregunta', 
        required=True
    )
    
    response = fields.Char(
        'Respuesta', 
        required=True
    )
    
    correct = fields.Boolean('validacion', default=False)
    point = fields.Integer('Puntos', default=0)
