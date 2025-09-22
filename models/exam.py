from openerp import models, fields, api, _

class exam(models.Model):
    _name = 'python_odoo8_module.exam'
    _description = 'Modelo de examenes'

    name = fields.Char('Nombre de examen', required=True)
    
    subject_id = fields.Many2one(
        'python_odoo8_module.subject', 
        string='Materia', 
        required=True
    )
    
    question_ids = fields.One2many(
        'python_odoo8_module.exam_question', 
        'exam_id', 
        string='Preguntas',
        required=True
    )
    
    result_ids = fields.One2many(
        'python_odoo8_module.result', 
        'exam_id', 
        string='Resultados'
    )
