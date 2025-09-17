# -*- coding: utf-8 -*-
from openerp import models, fields, _

class Classroom(models.Model):
    _name = 'python_odoo8_module.classroom'
    _description = 'Modelo de Aulas'

    name = fields.Char('Aula', required=True)
    capacity = fields.Integer('Capacidad', required=True)
 
    _sql_constraints = [
        ('valid_capacity', 'CHECK (capacity > 0)', 'La capacidad debe ser mayor a cero.'),
        ('classroom_name_unique', 'unique(name)', 'Ya existe un aula con ese nombre.'),
    ]
    
    itinerary_ids = fields.One2many(
        'python_odoo8_module.itinerary',
        'classroom_id',
        string='Itinerario'
    )