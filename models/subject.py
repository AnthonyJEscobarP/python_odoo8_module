# -*- coding: utf-8 -*-
from openerp import models, fields, api,_
from openerp.exceptions import Warning

class Subject(models.Model):
    _name = 'python_odoo8_module.subject'
    _description = 'Modelo de cursos'

    name = fields.Char('Nombre de Materia', required=True)
    description = fields.Text('Descripción')
    
    student_ids = fields.Many2many(
        'python_odoo8_module.student',
        'student_subject_rel',
        'subject_id', 'student_id',
        string='Estudiantes'
    )
    
    classroom_id = fields.Many2one(
        'python_odoo8_module.classroom',
        string='Aula',
        ondelete='set null'
    )
    
    _sql_constraints = [
        ('subject_name_unique', 'unique(name)', 'Esta materia ya existe, intenta de nuevo con un nombre diferente.'),
    ]
    
    @api.constrains('student_ids', 'classroom_id')
    def checkCapacity(self):
        for subject in self:
            if subject.classroom_id and len(subject.student_ids) > subject.classroom_id.capacity:
                raise Warning(_("El aula %s solo permite %s alumnos, pero intentas asignar %s.") %
                    (subject.classroom_id.name, subject.classroom_id.capacity, len(subject.student_ids)))
 