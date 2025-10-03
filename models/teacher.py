# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning
import re
from datetime import datetime

class Teacher(models.Model):
    _name = 'python_odoo8_module.teacher'
    _description = 'Modelo de maestro'

    name = fields.Char('Nombre Completo', required=True)
    age = fields.Integer('Edad', required=True)
    photo = fields.Binary('Foto de perfil')
    email = fields.Char('Email', required=True)

    subject_id = fields.Many2one(
        'python_odoo8_module.subject',
        string='Materia',
        compute='teacher_to_subject_relation',
        store=False
    )
    
    schedule_ids = fields.One2many(
        'python_odoo8_module.schedule',
        related='subject_id.schedule_ids', 
        string='Horarios',
        readonly=True
    )
    
    @api.depends()
    def teacher_to_subject_relation(self):
        for teacher in self:
            subject = self.env['python_odoo8_module.subject'].search([('teacher_id', '=', teacher.id)], limit=1)
            teacher.subject_id = subject.id if subject else False
        
    @api.constrains('email')
    def validateEmail(self):
        emailValidation = re.compile(r'^[^@]+@[^@]+\.[^@]+$')
        for rec in self:
            if rec.email and not emailValidation.match(rec.email):
                raise Warning(_("El correo debe ser válido (ej. usuario@dominio.com)."))

    @api.model
    def create(self, vals):
        if vals.get('email') and not vals.get('user_id'):
            try:
                group = self.env['res.groups'].search([('name', '=', 'Profesores')], limit=1)
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
        return super(Teacher, self).create(vals)
    
    @api.multi
    def write(self, vals):
        res = super(Teacher, self).write(vals)
        for rec in self:
            if 'email' in vals and rec.user_id:
                rec.user_id.login = vals['email']     
        return res