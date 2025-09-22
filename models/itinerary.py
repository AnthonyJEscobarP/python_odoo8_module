from openerp import models, fields, api, _
from datetime import datetime, timedelta
from openerp.osv import expression
from collections import defaultdict
import re

class Itinerary(models.Model):
    _name = 'python_odoo8_module.itinerary'
    _description = 'Modelo de itinerario para sesiones de clases'

    day = fields.Selection([
        ('mon', 'Lunes'),
        ('tue', 'Martes'),
        ('wed', 'Miércoles'),
        ('thu', 'Jueves'),
        ('fri', 'Viernes'),
    ], 'Día', required=True)

    hour = fields.Char('Hora', required=True)

    subject_id = fields.Many2one(
        'python_odoo8_module.subject', 
        string='Materia', 
        required=True
    )
    classroom_id = fields.Many2one(
        'python_odoo8_module.classroom', 
        string='Aula', 
        required=True
    )
    
    student_ids = fields.Many2many(
        'python_odoo8_module.student',
        'itinerary_student_rel',
        'itinerary_id', 'student_id',
        string='Estudiantes'
    )

    _sql_constraints = [
        ('unique_itinerary', 'unique(classroom_id, day, hour)', 'Aula, día y hora ocupados, verifica nuevamente'),
    ]
    
    @api.constrains('student_ids')
    def validate_same_grade(self):
        for itinerary in self:
            if itinerary.student_ids:
                grades = defaultdict(list)
                for student in itinerary.student_ids:
                    grades[student.grade].append(student.name)
                
                if len(grades) > 1:
                    raise Warning(_("No se pueden asignar estudiantes de diferentes grados al mismo periodo"))
                    
    @api.constrains('student_ids', 'classroom_id')
    def validate_capacity(self):
        for itinerary in self:
            if itinerary.classroom_id and len(itinerary.student_ids) > itinerary.classroom_id.capacity:
                raise Warning(_("La capacidad maxima del aula es de %s solo permite %s alumnos, pero intentas asignar %s.") %
                    (itinerary.classroom_id.name, itinerary.classroom_id.capacity, len(itinerary.student_ids)))
                
    @api.constrains('hour', 'day', 'classroom_id')
    def validate_mixed_hours(self):
        for rec in self:
            try:
                start = datetime.strptime(rec.hour, "%H:%M")
                end = start + timedelta(hours=1)
                mixed_hours = self.search([
                    ('id', '!=', rec.id),
                    ('classroom_id', '=', rec.classroom_id.id),
                    ('day', '=', rec.day),
                ])
                
                for other in mixed_hours:
                    other_start = datetime.strptime(other.hour, "%H:%M")
                    other_end = other_start + timedelta(hours=1)
                    if (start < other_end) and (end > other_start):
                        raise Warning(_("Tu horario "))
            except Exception:
                raise Warning(_("La hora debe estar en formato de 24H HH:MM."))
                
    @api.constrains('hour')
    def validate_hour(self):
        hour_validation = re.compile(r'^([01]\d|2[0-3]):([0-5]\d)$')
        for rec in self:
            if rec.hour and not hour_validation.match(rec.hour):
                raise Warning(_("La hora debe estar en formato de 24H HH:MM."))

    @api.model
    def one_hour_search(self, args, offset=0, limit=None, order=None, count=False):
        for argument in args:
            if isinstance(argument, (list, tuple)) and argument[0] == 'hour' and argument[1] == '=':
                try:
                    start_time = datetime.strptime(argument[2], "%H:%M")
                    end_time = start_time + timedelta(hours=1)
                    args = expression.AND([args,[('hour', '>=', start_time.strftime("%H:%M")), ('hour', '<', end_time.strftime("%H:%M"))]])
                except ValueError:
                    raise Warning(_("Debe estar en formato de 24h: HH:MM."))
        return super(itinerary, self).search(args, offset, limit, order, count)