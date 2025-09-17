# -*- coding: utf-8 -*-
from openerp import models, fields, api,_
from openerp.exceptions import Warning

class Subject(models.Model):
    _name = 'python_odoo8_module.subject'
    _description = 'Modelo de cursos'

    name = fields.Char('Nombre de Materia', required=True)
    description = fields.Text('Descripción')
    
    teacher_id = fields.Many2one(
        'python_odoo8_module.teacher',
        string='Profesor'
    )

    _sql_constraints = [
        ('subject_name_unique', 'unique(name)', 'Esta materia ya existe, intenta de nuevo con un nombre diferente.'),
    ]
    
    itinerary_ids = fields.One2many(
        'python_odoo8_module.itinerary',
        'subject_id',
        string='Itinerario'
    )
 