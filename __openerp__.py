{
  'name': 'Modulo: administracion estudiantil',
  'version': '1.2',
  'author': 'Anthony Escobar / AE-Solutions',
  'category': 'Education',
  'depends': ['base','web'],
  'data': [
    'security/roles.xml',
    'security/auth.xml',
    'security/ir.model.access.csv',
    'views/teacher.xml',      # Primero
    'views/classroom.xml',    # Segundo  
    'views/student.xml',      # Tercero
    'views/subject.xml',      # Cuarto
    'views/schedule.xml', 
    'views/exam.xml',
    'views/result.xml',
    'views/menu.xml',
    'data/sequence_card.xml',
    'wizard/student_transcript_wizard.xml',
    'wizard/student_schedule_wizard.xml'
  ],
  'installable': True,
  'application': True,
}
