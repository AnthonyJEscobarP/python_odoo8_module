# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning
import re
from datetime import datetime

class teacher(models.Model):
    _name = 'python_odoo8_module.teacher'
    _description = 'Modelo de maestro'

    name = fields.Char('Nombre Completo', required=True)
    age = fields.Integer('Edad', required=True)
    photo = fields.Binary('Foto de perfil')
    email = fields.Char('Email', required=True)
    
    subject_id = fields.Many2one(
        'python_odoo8_module.subject',
        string='Materia'
    )
    
    itinerary_ids = fields.Many2many(
        'python_odoo8_module.itinerary',
        compute='itinerary_access',
        string='Itinerarios',
        store=False
    )

    @api.depends('subject_ids')
    def itinerary_access(self):
        for teacher in self:
            itineraries = self.env['python_odoo8_module.itinerary'].search([('subject_id', 'in', teacher.subject_ids.ids)])
            teacher.itinerary_ids = itineraries

    user_id = fields.Many2one('res.users', 'Usuario Odoo', help='Usuario vinculado con Odoo')

    _sql_constraints = [
        ('teacher_email_unique', 'unique(email)', 'El email ya está en uso.'),
    ]
    
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
                    'password': 'temporal', 
                }
                if group:
                    user_data['groups_id'] = [(6, 0, [group.id])]
                user_odoo = self.env['res.users'].create(user_data)
                vals['user_id'] = user_odoo.id
            except Exception:
                pass
        return super(teacher, self).create(vals)

    @api.multi
    def write(self, vals):
        res = super(teacher, self).write(vals)
        for rec in self:
            if 'email' in vals and rec.user_id:
                rec.user_id.login = vals['email']
        return res