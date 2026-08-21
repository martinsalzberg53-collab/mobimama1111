from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import date

output_path = 'mobi_mama_proposal.pdf'

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40,
)
styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']
styleH2 = styles['Heading2']

# Custom smaller heading
styleH3 = ParagraphStyle('Heading3', parent=styles['Heading3'], spaceAfter=6)

# Project-specific values (based on codebase inspection)
project_title = 'Mobi Mama: Maternal Health Support Platform'
student_name = 'Adukpo Macbeth, 11261849'
supervisor = 'Michael Kolugu'
submission_date = date.today().strftime('%Y-%m-%d')
course_code = 'DCIT 400 / INFOD 400'

# Abstract (approx 220 words) - based on actual features found in the codebase
abstract = (
    "Mobi Mama is a maternal-health support platform designed to improve access to antenatal care, "
    "patient–nurse coordination, and early risk detection for expecting mothers in Ghana. The system combines "
    "a Django REST API backend and a React + Vite frontend to provide appointment booking, a nurse-facing "
    "dashboard with automated safety alerts, curated pregnancy tips, and an AI-driven chat assistant for "
    "health guidance. Mothers can book and manage clinic appointments, while nurses can review assigned "
    "patients, approve bookings, and receive high-risk notifications informed by basic vitals and symptom data. "
    "The backend uses Django REST Framework with token authentication, and stores profile, clinic and appointment "
    "data in a lightweight SQLite database during development. The frontend consumes these endpoints via Axios, "
    "offering a responsive UI for mothers and nurses. This project addresses gaps in maternal-care coordination by "
    "reducing appointment friction, surfacing early warning signs through simple heuristics, and delivering approachable "
    "AI-powered assistance for common pregnancy questions. The expected outcome is a tested, documented prototype that "
    "demonstrates how low-cost digital tools can improve clinical communication and early detection of maternal risks."
)

# Problem statement
problem_statement = (
    "In many regions of Ghana, pregnant women face difficulties accessing timely antenatal care, coordinating appointments, "
    "and receiving early clinical attention for emergent risk factors. Health workers often lack tools that aggregate patient "
    "symptoms and vitals to prioritise high-risk cases. This project seeks to close that gap by delivering a practical web-based "
    "system that enables mothers to book appointments, nurses to monitor assigned patients with automated safety alerts, and "
    "care teams to coordinate more effectively. The system focuses on pragmatic, low-cost implementation suitable for local clinics."
)

# Objectives
main_objective = 'To design, implement and evaluate a prototype digital platform (Mobi Mama) that improves antenatal care access and early risk detection for mothers.'
specific_objectives = [
    'Build a RESTful backend (Django + DRF) to manage users, clinics, mother profiles and appointments.',
    'Develop a responsive React frontend (Vite) for mothers and nurses to interact with the system.',
    'Implement automated safety alerting based on mothers\' recorded vitals and symptoms to surface high-risk cases.',
    'Integrate a conversational AI assistant for user guidance and to support non-critical queries.',
    'Document, test, and deploy a working prototype with usage instructions and evaluation suggestions.'
]

# Methodology & Tech Stack
sdlc = (
    "Agile / iterative development: requirement gathering, rapid prototyping, implementation, testing and documentation. "
    "Frequent demos and user feedback cycles with stakeholders."
)

requirements_instruments = (
    "Stakeholder interviews, developer-driven feature listing, and informal usability feedback sessions with potential users and "
    "clinical staff. Logging and lightweight analytics during pilot runs for evaluation."
)

architecture = (
    "The implementation uses a two-tier architecture: a Django backend exposing a REST API (Django REST Framework) with token "
    "authentication, and a React + Vite SPA frontend communicating over Axios to `http://localhost:8000/api`. Data is persisted using "
    "SQLite for development (models: `Clinic`, `MotherProfile`, `Appointment`, `User`) and can be migrated to PostgreSQL for production. "
    "Key components: authentication (custom email-based user model), appointment booking logic, nurse dashboard with risk heuristics, "
    "tips module, and AI chat endpoints."
)

# Timeline (Phase 1..5) - reflect current state: many core features implemented
timeline_data = [
    ['Phase', 'Activities', 'Weeks'],
    ['Phase 1', 'Requirements, basic models, authentication, initial backend APIs (completed)', 'Weeks 1-3'],
    ['Phase 2', 'Frontend prototypes for mothers and nurses, appointment UI, clinic listing (completed)', 'Weeks 4-6'],
    ['Phase 3', 'AI chat integration, risk heuristics, nurse dashboard alerts (mostly implemented)', 'Weeks 7-9'],
    ['Phase 4', 'Testing, migrations, documentation, accessibility improvements (remaining)', 'Weeks 10-12'],
    ['Phase 5', 'Deployment preparation, evaluation, final report and presentation (remaining)', 'Weeks 13-15'],
]

# References (short list)
references = [
    'World Health Organization. WHO recommendations on antenatal care for a positive pregnancy experience. 2016.',
    'H. Schild, "Designing Web Applications with Django", O\'Reilly, 2020.',
    'M. Fowler, "Patterns of Enterprise Application Architecture", Addison-Wesley, 2002.',
    'Field, A., "Discovering Statistics Using IBM SPSS Statistics", Sage Publications, 2013.'
]

# Build document
story = []
story.append(Paragraph('UNIVERSITY OF GHANA', styleH))
story.append(Paragraph('DEPARTMENT OF COMPUTER SCIENCE / DEPARTMENT OF INFORMATION TECHNOLOGY', styleN))
story.append(Spacer(1, 6))
story.append(Paragraph('LEVEL 400 FINAL YEAR PROJECT PROPOSAL', styleH2))
story.append(Spacer(1, 12))

story.append(Paragraph(f'<b>Project Title:</b> {project_title}', styleN))
story.append(Paragraph(f'<b>Course Code:</b> {course_code}', styleN))
story.append(Paragraph(f'<b>Student Name(s) & ID(s):</b> {student_name}', styleN))
story.append(Paragraph(f'<b>Proposed Supervisor:</b> {supervisor}', styleN))
story.append(Paragraph(f'<b>Date of Submission:</b> {submission_date}', styleN))
story.append(Spacer(1, 12))

story.append(Paragraph('1. ABSTRACT / PROJECT SUMMARY', styleH2))
story.append(Spacer(1, 6))
story.append(Paragraph(abstract, styleN))
story.append(Spacer(1, 12))

story.append(Paragraph('2. INTRODUCTION & BACKGROUND', styleH2))
story.append(Spacer(1, 6))
story.append(Paragraph('2.1 Background of the Study', styleH3))
story.append(Paragraph('Mobi Mama addresses maternal care coordination by providing digital tools for appointment booking, tips, and communication between mothers and nurses.', styleN))
story.append(Spacer(1, 6))
story.append(Paragraph('2.2 Motivation', styleH3))
story.append(Paragraph('The motivation is to reduce barriers to antenatal care, improve early detection of risks, and provide approachable guidance to expecting mothers using low-cost web technologies.', styleN))
story.append(Spacer(1, 12))

story.append(Paragraph('3. PROBLEM STATEMENT', styleH2))
story.append(Spacer(1, 6))
story.append(Paragraph(problem_statement, styleN))
story.append(Spacer(1, 12))

story.append(Paragraph('4. PROJECT OBJECTIVES', styleH2))
story.append(Spacer(1, 6))
story.append(Paragraph('4.1 Main Objective', styleH3))
story.append(Paragraph(main_objective, styleN))
story.append(Spacer(1, 6))
story.append(Paragraph('4.2 Specific Objectives', styleH3))
for obj in specific_objectives:
    story.append(Paragraph(f'• {obj}', styleN))
story.append(Spacer(1, 12))

story.append(Paragraph('5. SIGNIFICANCE & SCOPE OF THE STUDY', styleH2))
story.append(Spacer(1, 6))
story.append(Paragraph('5.1 Significance', styleH3))
story.append(Paragraph('The project offers a practical prototype to clinics and students showing how digital systems can enhance antenatal care coordination, early risk detection and patient engagement.', styleN))
story.append(Spacer(1, 6))
story.append(Paragraph('5.2 Scope', styleH3))
story.append(Paragraph('The prototype focuses on appointment management, nurse dashboards with automated alerts, maternal profile recording, and an AI chat helper. It targets small clinics and pilot deployments, using SQLite during development and allowing migration to PostgreSQL for production.', styleN))
story.append(Spacer(1, 12))

story.append(Paragraph('6. SYSTEM METHODOLOGY & DESIGN', styleH2))
story.append(Spacer(1, 6))
story.append(Paragraph('6.1 Software Development Lifecycle (SDLC)', styleH3))
story.append(Paragraph(sdlc, styleN))
story.append(Spacer(1, 6))
story.append(Paragraph('6.2 Requirements Gathering Instruments', styleH3))
story.append(Paragraph(requirements_instruments, styleN))
story.append(Spacer(1, 6))
story.append(Paragraph('6.3 High-Level Architecture', styleH3))
story.append(Paragraph(architecture, styleN))
story.append(Spacer(1, 12))

story.append(Paragraph('7. PROJECT TIMELINE', styleH2))
story.append(Spacer(1, 6))

table = Table(timeline_data, colWidths=[80, 320, 120])
table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
]))
story.append(table)
story.append(Spacer(1, 12))

story.append(Paragraph('8. REFERENCES', styleH2))
story.append(Spacer(1, 6))
for ref in references:
    story.append(Paragraph(f'• {ref}', styleN))

# Footer note
story.append(Spacer(1, 20))
story.append(Paragraph('Generated from the Mobi Mama codebase (Django + React) on ' + submission_date, styleN))

# Build PDF
if __name__ == '__main__':
    doc.build(story)
    print('Created', output_path)
