from django.shortcuts import render
from django.contrib.auth.models import User
from templates.models import contactDetail, careerProfile, softSkill, areaOfInterest, professionalSkill, educationDetail, experienceDetail, task, project, certification, reference, professionalCourses
import reportlab
from reportlab.lib.colors import HexColor
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
# Create your views here.
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.colors import Color, black, blue, red
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab import platypus
def resumepdf(request, str):
	if str == '1':
	
		tum_logo = 'media/photos/tum-logo.jpg'
		my_profile = 'media/photos/tum-logo.jpg'
		styles = getSampleStyleSheet()
		styleN = PS(name = 'Normal',
					fontSize = 10,
					leading = 14,
					firstLineIndent=-5,
					)
		stylePhoto = PS(name = 'Normal',
					fontSize = 10,
					leading = 84,
					firstLineIndent=25,
					)
		styleS = PS(name = 'Normal',
					fontSize = 12,
					leading = 22,	
					leftPadding=6			
					)
		styleName = PS(name = 'Normal',
					fontSize = 12,
					leading = 32,				
					firstLineIndent=0,		
					)
		styleP = PS(name = 'Normal',				
					leftPadding=16			
					)
		styleF = PS(name = 'Normal',				
					leading = 40,				
					)
		normal = styles['Normal']
		styleH = styles['Heading3']
		styleH3 = styles['Heading4']
		styleH5 = styles['Heading5']
		styleHIdent = PS(name = 'Heading6',
					fontSize = 10,
					leading = 14,
					firstLineIndent=0,
					)
		styleH6 = PS(name = 'Heading6',
					fontSize = 10,
					leading = 14,
					firstLineIndent=-5,
					)

		#side sestion
		user = User.objects.get(id=1)
		contact = contactDetail.objects.get(user_id=user.id)
		career_profile = careerProfile.objects.get(user_id=user.id)
		skills = professionalSkill.objects.filter(user_id=user.id)
		soft_skills = softSkill.objects.filter(user_id=user.id)
		interests = areaOfInterest.objects.filter(user_id=user.id)
		educations = educationDetail.objects.filter(user_id=user.id).order_by("-end")
		experiences = experienceDetail.objects.filter(user_id=user.id).order_by("-end")
		tasks = task.objects.filter(user_id=user.id)
		references = reference.objects.filter(user_id=user.id)
		courses = professionalCourses.objects.filter(user_id=user.id)
		projects = project.objects.filter(user_id=user.id)

		profile =  []
		#contacts
		email = '<link href="' + f'mailto:{contact.email}' + '">'+ f"<font color=white ><img height=12 width=10 src='media/photos/email.png' valign='top'/> {contact.email}</font>"+ '</link>'
		web = '<link href="' + f'http://www.{contact.website}' + '">'+ f"<font color=white ><img height=12 width=10 src='media/photos/web.png' valign='top'/> {contact.website}</font>"+ '</link>'
		linkedin = '<link href="' + f'http://www.{contact.linkedin}' + '">'+ f"<font color=white ><img height=12 width=10 src='media/photos/linkedin.png' valign='top'/> {contact.linkedin}</font>"+ '</link>'
		github = '<link href="' + f'http://www.{contact.github}' + '">'+ f"<font color=white ><img height=12 width=10 src='media/photos/github.png' valign='top'/> {contact.github}</font>"+ '</link>'
		
		profile.append(Paragraph(f"<font color=white size=23 name=Times-Roman>{contact.first_name} {contact.last_name}</font>",styleName))
		profile.append(Paragraph(f"<font color=white size=14>{contact.title}</font>", styleF))	
		profile.append(platypus.Paragraph(email, styleS))	
		profile.append(Paragraph(f"<font color=white ><img height=12 width=10 src='media/photos/phone.png' valign='top'/> +254706046810</font>",styleS))
		profile.append(platypus.Paragraph(web, styleS))
		profile.append(platypus.Paragraph(linkedin, styleS))
		profile.append(platypus.Paragraph(github, styleF))
		#SKILLS
		profile.append(Paragraph("<font color=white size=15>SKILLS</font>",styleS))
		for skill in skills:
			profile.append(Paragraph(f"<font color=white size=10>{skill.skill_name}</font>",styleS))
		#SOFT SKILLS
		profile.append(Paragraph("<font color=white size=15>SOFT SKILLS</font>",styleS))
		for soft_skill in soft_skills:
			profile.append(Paragraph(f"<font color=white size=10>{soft_skill.skill_name}</font>",styleS))	
		#INTERESTS
		profile.append(Paragraph("<font color=white size=15>INTERESTS</font>",styleS))
		for interest in interests:
			profile.append(Paragraph(f"<font color=white size=10>{interest.name_of_interest}</font>",styleS))
		
		story = []
		#career Summary
		story.append(Paragraph("<font>CAREER PROFILE</font> ",styleH))
		story.append(Paragraph(f"{career_profile.career_profile}",
		normal))
		#experiences
		story.append(Paragraph("<font>EXPERIENCES</font>",styleH))
		for experience in experiences:
			story.append(Paragraph(f"{experience.title}, <font size=9><i>{experience.start.strftime('%Y')}-{experience.start.strftime('%m')} - {experience.end.strftime('%Y')}-{experience.end.strftime('%m')}</i></font>",styleH3))
			story.append(Paragraph(f"<i>{experience.company}</i>",styleH5))
			for iteam in tasks:	
				if iteam.experience_id == experience.id:
					story.append(Paragraph(f"- {iteam.role}",
					styleH6))
		#projects
		story.append(Paragraph("<font color=black>PROJECTS</font>",styleH))
		for iteam in projects:
			story.append(Paragraph(f"- <b> {iteam.project_name} </b> , {iteam.description}",
			styleN))
		#Education
		story.append(Paragraph("<font color=black>EDUCATION</font>",styleH))
		for education in educations:
			story.append(Paragraph(f"<b><font size=10>{education.course_name}</font></b>",
			styleH5))
			story.append(Paragraph(f"{education.school_name}",
			styleH5))
			story.append(Paragraph(f"<i>{education.start} - {education.end}</i>",	styleHIdent))
		#professional courses
		story.append(Paragraph("<font>COMPLETED PROFESSIONAL COURSES</font>",styleH))
		for iteam in courses:
			story.append(Paragraph(f"- {iteam.course_name}",
			styleN))
		#references
		reference1 = []	
		reference1.append(Paragraph("<font>REFERENCES</font>",styleH))
		for iteam in references:
			reference1.append(Paragraph(f"{iteam.first_name} {iteam.last_name}",styleN))
			reference1.append(Paragraph("Technical University of Mombasa",styleN))
			reference1.append(Paragraph("University Lecturer",styleN))
			reference1.append(Paragraph("Phone: +254733770772",styleN))
			reference1.append(Paragraph("Email: khadullo@gmail.com",styleN))
		
		reference2 = []
		reference2.append(Paragraph("Eliud Muigu",styleN))
		reference2.append(Paragraph("Kenya Revenue Authority",styleN))
		reference2.append(Paragraph("KRA Officer",styleN))
		reference2.append(Paragraph("Phone: +254722844588",styleN))
		reference2.append(Paragraph("Email: muigue43@gmail.com",styleN))
		
		# Create a file-like buffer to receive PDF data.
		buffer = io.BytesIO()

		# Create the PDF object, using the buffer as its "file."
		p = canvas.Canvas(buffer)
		#p.setFillColorRGB(0.3,0.54,0.6)
		#p.setFillColorRGB(0.12,0.576,1)
		#p.setFillColorRGB(0.12,0.576,0.6)
		# p.setFillColorRGB(0.52,0.576,0.7)
		p.setFillColorRGB(0.130,0.130,0.199)
		p.setTitle(f'{contact.first_name} {contact.last_name} Resume')
		p.setSubject(f'This resume was generated for {contact.first_name} {contact.last_name}.') 
		#canvas.rect(left_padding, bottom_padding, width, height, fill=1)
		p.rect(0,0,205,850, stroke=0, fill=1)
		p.setFillColor(HexColor("#f5f5f5"))
		p.setFontSize(17)
		p.setAuthor('Francis Mugambi - +254706046810')

		i = inch
		d = i/4
		# define the bezier curve control points
		x1,y1, x2,y2, x3,y3, x4,y4 = d,1.5*i, 1.5*i,d, 3*i,d, 5.5*i-d,3*i-d
		p.setLineWidth(inch*0.015)
		p.setStrokeColor(red)
		p.line(0,845,595,0)
		p.setStrokeColor(black)
		p.line(595,810,220,810)

		f = Frame(215, 0, 377,830, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
		c = Frame(10, 0, 195,830, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
		d = Frame(225, 0, 377,110, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
		e = Frame(420, 0, 377,90, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
		f.addFromList(story,p)
		c.addFromList(profile,p)
		#d.addFromList(reference1,p)
		#e.addFromList(reference2,p)
		# p.drawImage(tum_logo, 18, 780, width=40,height=50, preserveAspectRatio=True, mask='auto')
		#p.drawImage(my_profile, 35, 730, width=110,height=90, preserveAspectRatio=True, mask='auto')
		#p.circle(90, 794, 43, stroke=1, fill=0)	

		# Close the PDF object cleanly, and we're done.
		p.showPage()
		p.save()

		# FileResponse sets the Content-Disposition header so that browsers
		# present the option to save the file.
		buffer.seek(0)
		return FileResponse(buffer, as_attachment=False, filename=f'{contact.first_name} Resume.pdf')
	elif str == '2':
		tum_logo = 'media/photos/tum-logo.jpg'
		my_profile = 'media/photos/tum-logo.jpg'
		styles = getSampleStyleSheet()
		styleN = PS(name = 'Normal', fontSize = 10,	leading = 14, firstLineIndent=-5)
		stylePhoto = PS(name = 'Normal', fontSize = 10,	leading = 84, firstLineIndent=25)
		styleS = PS(name = 'Normal', fontSize = 12,	leading = 22,leftPadding=6)
		styleName = PS(name = 'Normal',	fontSize = 12,	leading = 32,firstLineIndent=0)
		styleP = PS(name = 'Normal', leftPadding=16)
		styleF = PS(name = 'Normal', leading = 40)
		normal = styles['Normal']
		styleH = styles['Heading3']
		styleH3 = styles['Heading4']
		styleH5 = styles['Heading5']
		styleH6 = PS(name = 'Heading6',	fontSize = 10, leading = 14, firstLineIndent=-5)

		#side sestion
		user = User.objects.get(id=1)
		contact = contactDetail.objects.get(user_id=user.id)
		career_profile = careerProfile.objects.get(user_id=user.id)
		skills = professionalSkill.objects.filter(user_id=user.id)
		soft_skills = softSkill.objects.filter(user_id=user.id)
		interests = areaOfInterest.objects.filter(user_id=user.id)
		educations = educationDetail.objects.filter(user_id=user.id).order_by("-end")
		experiences = experienceDetail.objects.filter(user_id=user.id).order_by("-end")
		tasks = task.objects.filter(user_id=user.id)
		references = reference.objects.filter(user_id=user.id)
		courses = professionalCourses.objects.filter(user_id=user.id)
		projects = project.objects.filter(user_id=user.id)

		profile =  []
		#contacts
		email = '<link href="' + f'mailto:{contact.email}' + '">'+ f"<font color=white ><img height=12 width=10 src='media/photos/email.png' valign='top'/> {contact.email}</font>"+ '</link>'
		web = '<link href="' + f'http://www.{contact.website}' + '">'+ f"<font color=white ><img height=12 width=10 src='media/photos/web.png' valign='top'/> {contact.website}</font>"+ '</link>'
		linkedin = '<link href="' + f'http://www.{contact.linkedin}' + '">'+ f"<font color=white ><img height=12 width=10 src='media/photos/linkedin.png' valign='top'/> {contact.linkedin}</font>"+ '</link>'
		github = '<link href="' + f'http://www.{contact.github}' + '">'+ f"<font color=white ><img height=12 width=10 src='media/photos/github.png' valign='top'/> {contact.github}</font>"+ '</link>'
		
		profile.append(Paragraph(f"<font color=white size=23 name=Times-Roman>{contact.first_name} {contact.last_name}</font>",styleName))
		profile.append(Paragraph(f"<font color=white size=14>{contact.title}</font>", styleF))	
		profile.append(platypus.Paragraph(email, styleS))	
		profile.append(Paragraph(f"<font color=white ><img height=12 width=10 src='media/photos/phone.png' valign='top'/> +254706046810</font>",styleS))
		profile.append(platypus.Paragraph(web, styleS))
		profile.append(platypus.Paragraph(linkedin, styleS))
		profile.append(platypus.Paragraph(github, styleF))
		#SKILLS
		profile.append(Paragraph("<font color=white size=15>SKILLS</font>",styleS))
		for skill in skills:
			profile.append(Paragraph(f"<font color=white size=10>{skill.skill_name}</font>",styleS))
		#SOFT SKILLS
		profile.append(Paragraph("<font color=white size=15>SOFT SKILLS</font>",styleS))
		for soft_skill in soft_skills:
			profile.append(Paragraph(f"<font color=white size=10>{soft_skill.skill_name}</font>",styleS))	
		#INTERESTS
		profile.append(Paragraph("<font color=white size=15>INTERESTS</font>",styleS))
		for interest in interests:
			profile.append(Paragraph(f"<font color=white size=10>{interest.name_of_interest}</font>",styleS))
		
		story = []
		#career Summary
		story.append(Paragraph("<font>CAREER PROFILE</font> ",styleH))
		story.append(Paragraph(f"{career_profile.career_profile}",
		normal))
		#experiences
		story.append(Paragraph("<font>EXPERIENCES</font>",styleH))
		for experience in experiences:
			story.append(Paragraph(f"{experience.title}, <font size=9><i>{experience.start.strftime('%Y')}-{experience.start.strftime('%m')} - {experience.end.strftime('%Y')}-{experience.end.strftime('%m')}</i></font>",styleH3))
			story.append(Paragraph(f"<i>{experience.company}</i>",styleH5))
			for iteam in tasks:	
				if iteam.experience_id == experience.id:
					story.append(Paragraph(f"- {iteam.role}",
					styleH6))
		#projects
		story.append(Paragraph("<font color=black>PROJECTS</font>",styleH))
		for iteam in projects:
			story.append(Paragraph(f"- <b> {iteam.project_name} </b> , {iteam.description}",
			styleN))
		#Education
		story.append(Paragraph("<font color=black>EDUCATION</font>",styleH))
		for education in educations:
			story.append(Paragraph(f"<b><font size=10>{education.course_name}</font></b>",
			styleH5))
			story.append(Paragraph(f"{education.school_name}",
			styleH5))
			story.append(Paragraph(f"<i>{experience.start.strftime('%Y')}-{experience.start.strftime('%m')} - {education.end.strftime('%Y')}-{education.end.strftime('%m')}</i>",	styleH5))
		#professional courses
		story.append(Paragraph("<font>COMPLETED PROFESSIONAL COURSES</font>",styleH))
		for iteam in courses:
			story.append(Paragraph(f"- {iteam.course_name}",
			styleN))
		#references
		reference1 = []	
		reference1.append(Paragraph("<font>REFERENCES</font>",styleH))
		for iteam in references:
			reference1.append(Paragraph(f"{iteam.first_name} {iteam.last_name}",styleN))
			reference1.append(Paragraph("Technical University of Mombasa",styleN))
			reference1.append(Paragraph("University Lecturer",styleN))
			reference1.append(Paragraph("Phone: +254733770772",styleN))
			reference1.append(Paragraph("Email: khadullo@gmail.com",styleN))
		
		reference2 = []
		reference2.append(Paragraph("Eliud Muigu",styleN))
		reference2.append(Paragraph("Kenya Revenue Authority",styleN))
		reference2.append(Paragraph("KRA Officer",styleN))
		reference2.append(Paragraph("Phone: +254722844588",styleN))
		reference2.append(Paragraph("Email: muigue43@gmail.com",styleN))
		
		# Create a file-like buffer to receive PDF data.
		buffer = io.BytesIO()

		# Create the PDF object, using the buffer as its "file."
		p = canvas.Canvas(buffer)
		#p.setFillColorRGB(0.3,0.54,0.6)
		#p.setFillColorRGB(0.12,0.576,1)
		#p.setFillColorRGB(0.12,0.576,0.6)
		# p.setFillColorRGB(0.52,0.576,0.7)
		p.setFillColorRGB(0.130,0.130,0.199)
		p.setTitle(f'{contact.first_name} {contact.last_name} Resume')
		p.setSubject(f'This resume was generated for {contact.first_name} {contact.last_name}.') 
		#canvas.rect(left_padding, bottom_padding, width, height, fill=1)
		p.rect(400,0,205,850, stroke=0, fill=1)
		p.setFillColor(HexColor("#f5f5f5"))
		p.setFontSize(17)
		p.setAuthor('Francis Mugambi - +254706046810')

		i = inch
		d = i/4
		# define the bezier curve control points
		x1,y1, x2,y2, x3,y3, x4,y4 = d,1.5*i, 1.5*i,d, 3*i,d, 5.5*i-d,3*i-d
		p.setLineWidth(inch*0.02)
		p.setStrokeColor(red)
		p.line(0,845,595,0)
		p.setStrokeColor(black)
		p.line(400,810,27,810)


		f = Frame(20, 0, 377,830, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
		c = Frame(400, 0, 195,830, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
		d = Frame(20, 0, 377,100, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
		e = Frame(190, 0, 377,90, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
		
		c.addFromList(profile,p)
		f.addFromList(story,p)		
		#d.addFromList(reference1,p)
		#e.addFromList(reference2,p)
		# p.drawImage(tum_logo, 18, 780, width=40,height=50, preserveAspectRatio=True, mask='auto')
		#p.drawImage(my_profile, 35, 730, width=110,height=90, preserveAspectRatio=True, mask='auto')
		#p.circle(90, 794, 43, stroke=1, fill=0)	

		# Close the PDF object cleanly, and we're done.
		p.showPage()
		p.save()

		# FileResponse sets the Content-Disposition header so that browsers
		# present the option to save the file.
		buffer.seek(0)
		return FileResponse(buffer, as_attachment=False, filename=f'{contact.first_name} Resume.pdf')
	elif str == '3':
		tum_logo = 'media/photos/tum-logo.jpg'
		my_profile = 'media/photos/tum-logo.jpg'
		styles = getSampleStyleSheet()
		styleN = PS(name = 'Normal', fontSize = 10,	leading = 14, firstLineIndent=-5)
		stylePhoto = PS(name = 'Normal', fontSize = 10,	leading = 84, firstLineIndent=25)
		styleS = PS(name = 'Normal', fontSize = 12,	leading = 22,leftPadding=6)
		styleName = PS(name = 'Normal',	fontSize = 12,	leading = 32,firstLineIndent=0)
		styleP = PS(name = 'Normal', leftPadding=16)
		styleF = PS(name = 'Normal', leading = 40)
		stylel25 = PS(name = 'Normal', leading = 25)
		normal = styles['Normal']
		styleH = styles['Heading3']
		styleH3 = styles['Heading4']
		styleH5 = styles['Heading5']
		styleH6 = PS(name = 'Heading6',	fontSize = 10, leading = 14, firstLineIndent=-5)

		#side sestion
		user = User.objects.get(id=1)
		contact = contactDetail.objects.get(user_id=user.id)
		career_profile = careerProfile.objects.get(user_id=user.id)
		skills = professionalSkill.objects.filter(user_id=user.id)
		soft_skills = softSkill.objects.filter(user_id=user.id)
		interests = areaOfInterest.objects.filter(user_id=user.id)
		educations = educationDetail.objects.filter(user_id=user.id).order_by("-end")
		experiences = experienceDetail.objects.filter(user_id=user.id).order_by("-end")
		tasks = task.objects.filter(user_id=user.id)
		references = reference.objects.filter(user_id=user.id)
		courses = professionalCourses.objects.filter(user_id=user.id)
		projects = project.objects.filter(user_id=user.id)

		profile =  []
		#contacts
		email = '<link href="' + f'mailto:{contact.email}' + '">'+ f"<font><img height=12 width=10 src='media/photos/email.png' valign='top'/> {contact.email}</font>"+ '</link>'
		web = '<link href="' + f'http://www.{contact.website}' + '">'+ f"<font ><img height=12 width=10 src='media/photos/web.png' valign='top'/> {contact.website}</font>"+ '</link>'
		linkedin = '<link href="' + f'http://www.{contact.linkedin}' + '">'+ f"<font><img height=12 width=10 src='media/photos/linkedin.png' valign='top'/> {contact.linkedin}</font>"+ '</link>'
		github = '<link href="' + f'http://www.{contact.github}' + '">'+ f"<font ><img height=12 width=10 src='media/photos/github.png' valign='top'/> {contact.github}</font>"+ '</link>'
			
		#SKILLS
		profile.append(Paragraph("<font size=15>SKILLS</font>",styleS))
		for skill in skills:
			profile.append(Paragraph(f"<font size=10>{skill.skill_name}</font>",styleS))
		#SOFT SKILLS
		profile.append(Paragraph("<font size=15>SOFT SKILLS</font>",styleS))
		for soft_skill in soft_skills:
			profile.append(Paragraph(f"<font size=10>{soft_skill.skill_name}</font>",styleS))	
		#INTERESTS
		profile.append(Paragraph("<font size=15>INTERESTS</font>",styleS))
		for interest in interests:
			profile.append(Paragraph(f"<font size=10>{interest.name_of_interest}</font>",styleS))
		
		story = []
		#career Summary
		story.append(Paragraph("<font>CAREER PROFILE</font> ",styleH))
		story.append(Paragraph(f"{career_profile.career_profile}",
		normal))
		#experiences
		story.append(Paragraph("<font>EXPERIENCES</font>",styleH))
		for experience in experiences:
			story.append(Paragraph(f"{experience.title}, <font size=9><i>{experience.start.strftime('%Y')}-{experience.start.strftime('%m')} - {experience.end.strftime('%Y')}-{experience.end.strftime('%m')}</i></font>",styleH3))
			story.append(Paragraph(f"<i>{experience.company}</i>",styleH5))
			for iteam in tasks:	
				if iteam.experience_id == experience.id:
					story.append(Paragraph(f"- {iteam.role}",
					styleH6))
		#projects
		story.append(Paragraph("<font color=black>PROJECTS</font>",styleH))
		for iteam in projects:
			story.append(Paragraph(f"- <b> {iteam.project_name} </b> , {iteam.description}",
			styleN))
		#Education
		story.append(Paragraph("<font color=black>EDUCATION</font>",styleH))
		for education in educations:
			story.append(Paragraph(f"<b><font size=10>{education.course_name}</font></b>",
			styleH5))
			story.append(Paragraph(f"{education.school_name}",
			styleH5))
			story.append(Paragraph(f"<i>{experience.start.strftime('%Y')}-{experience.start.strftime('%m')} - {education.end.strftime('%Y')}-{education.end.strftime('%m')}</i>",	styleH5))
		#professional courses
		story.append(Paragraph("<font>COMPLETED PROFESSIONAL COURSES</font>",styleH))
		for iteam in courses:
			story.append(Paragraph(f"- {iteam.course_name}",
			styleN))
		#references
		head = []				
		head.append(Paragraph(f"<font size=22>{contact.first_name} {contact.last_name}</font>",stylel25))
		head.append(Paragraph("<font size=15>Software Developer</font>",stylel25))
		social1 = []		
		social1.append(Paragraph(f"<font><img height=12 width=10 src='media/photos/phone.png' valign='top'/> +254706046810</font>",styleS))
		social2 = []		
		social2.append(platypus.Paragraph(email, styleS))
		social3 = []
		social3.append(platypus.Paragraph(web, styleS))		
		# Create a file-like buffer to receive PDF data.
		buffer = io.BytesIO()

		# Create the PDF object, using the buffer as its "file."
		p = canvas.Canvas(buffer)
		p.setFillColorRGB(0.130,0.130,0.199)
		p.setTitle(f'{contact.first_name} {contact.last_name} Resume')
		p.setSubject(f'This resume was generated for {contact.first_name} {contact.last_name}.') 
		#canvas.rect(left_padding, bottom_padding, width, height, fill=1)
		p.setFontSize(17)
		p.setAuthor('Francis Mugambi - +254706046810')

		f = Frame(20, 0, 377,700, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
		c = Frame(400, 0, 195,700, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
		d = Frame(230, 0, 377,830, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
		e = Frame(20, 0, 377,750, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
		g = Frame(190, 0, 377,750, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
		h = Frame(420, 0, 377,750, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
		
		c.addFromList(profile,p)
		f.addFromList(story,p)		
		d.addFromList(head,p)
		e.addFromList(social1,p)
		g.addFromList(social2,p)
		h.addFromList(social3,p)
		# p.drawImage(tum_logo, 18, 780, width=40,height=50, preserveAspectRatio=True, mask='auto')
	
		# Close the PDF object cleanly, and we're done.
		p.showPage()
		p.save()

		# FileResponse sets the Content-Disposition header so that browsers
		# present the option to save the file.
		buffer.seek(0)
		return FileResponse(buffer, as_attachment=False, filename=f'{contact.first_name} Resume.pdf')
	else:
		return render(request, 'templates/templates.html')