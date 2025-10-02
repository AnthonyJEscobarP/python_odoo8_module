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
    
    exam_ids = fields.One2many(
        'python_odoo8_module.exam', 
        'subject_id', 
        string='Exámenes'
    )

    _sql_constraints = [
        ('subject_name_unique', 'unique(name)', 'Esta materia ya existe, intenta de nuevo con un nombre diferente.'),
    ]
    
    schedule_ids = fields.One2many(
        'python_odoo8_module.schedule',
        'subject_id',
        string='horario'
    )
 
    # update_subject_to_teacher_relation
    @api.multi
    def write(self, vals):
        res = super(Subject, self).write(vals)
        if 'teacher_id' in vals:
            for subject in self:
                if subject.teacher_id:
                    subject.teacher_id.subject_id = subject.id
        return res

    #add_subject_to_teacher_relation
    @api.model
    def create(self, vals):
        subject = super(Subject, self).create(vals)
        if vals.get('teacher_id'):
            subject.teacher_id.subject_id = subject.id
        return subject