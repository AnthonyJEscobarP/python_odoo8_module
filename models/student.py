# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning
import re
from datetime import datetime

class Student(models.Model):
    _name = 'python_odoo8_module.student'
    _description = 'Modelo de estudiante'

    name = fields.Char('Nombre Completo', required=True)
    age = fields.Integer('Edad', required=True)
    photo = fields.Binary('Foto de perfil')
    card = fields.Char('Carnet', readonly=True)
    email = fields.Char('Email', required=True)
    
    grade = fields.Selection([('1p', '1ro primaria'), ('2p', '2do primaria'), ('3p', '3ro primaria'),('4p', '4to primaria'), ('5p', '5to primaria'), ('6p', '6to primaria'),
                              ('1b', '1ro basico'), ('2b', '2do basico'), ('3b', '3ro basico'), 
                              ('1d', '1ro diversificado'), ('2d', '2do diversificado'),('3d', '3ro diversificado'), 
                              ], 'Grado', required=True)
    
    section = fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C')], 'Seccion', required=True)
    
    
    user_id = fields.Many2one('res.users', 'Usuario Odoo', help='Usuario vinculado con Odoo',ondelete='cascade')
    
    _sql_constraints = [
        ('student_card_unique', 'unique(card)', 'El carnet debe ser único.'),
        ('student_email_unique', 'unique(email)', 'El email ya está en uso.'),
    ]
    
    schedule_ids = fields.Many2many(
        'python_odoo8_module.schedule',
        'schedule_student_rel',
        'student_id', 'schedule_id',
        string='horario'
    )
    
    @api.constrains('email')
    def validateEmail(self):
        emailValidation = re.compile(r'^[^@]+@[^@]+\.[^@]+$')
        for rec in self:
            if rec.email and not emailValidation.match(rec.email):
                raise Warning(_("El correo debe ser válido (ej. usuario@dominio.com)."))
            
    @api.constrains('age')
    def validateAge(self):
        for rec in self:
            if rec.age < 7 or rec.age > 19:
                raise Warning(_("Edad ingresada no válida."))

    @api.model
    def create(self, vals):
        if not vals.get('card'):
            sequence = self.env['ir.sequence'].next_by_code('student_seq') or '1'
            sequence_string = str(sequence).zfill(3)
            year = datetime.now().year
            vals['card'] = "%s%s" % (year, sequence_string)
            
        if vals.get('email') and not vals.get('user_id'):
            try:
                email = vals.get('email')
                existing_user = self.env['res.users'].search([('login', '=', email)], limit=1)
                group = self.env['res.groups'].search([('name', '=', 'Estudiantes')], limit=1)
                if existing_user:
                    vals['user_id'] = existing_user.id
                    if group and group.id not in existing_user.groups_id.ids:
                        existing_user.groups_id = [(4, group.id)]
                else:
                    user_data = {
                        'name': vals.get('name'),
                        'login': vals.get('email'),
                        'email': vals.get('email'),
                        'password': 'temporal',
                    }
                    if group:
                        user_data['groups_id'] = [(6, 0, [group.id])]
                    user_odoo = self.env['res.users'].create(user_data)
                    vals['user_id'] = user_odoo.id
            except Exception:
                pass

        return super(Student, self).create(vals)

    @api.multi
    def write(self, vals):
        res = super(Student, self).write(vals)
        for rec in self:
            if 'email' in vals and rec.user_id:
                rec.user_id.login = vals['email']
        return res