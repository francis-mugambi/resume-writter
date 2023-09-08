from django.db import models
from django.contrib.auth.models import User, auth
from django.contrib.auth.models import AbstractUser
from  datetime import date

class contactDetail(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)   
    first_name = models.CharField(max_length=100, default='John')
    last_name = models.CharField(max_length=100, default='Doe')
    title = models.CharField(max_length=100, default='Software Developer')
    image = models.ImageField(upload_to='photos', default='default-profile.jpg', blank=True)
    email = models.EmailField(default='johndoe@gmail.com')
    phone = models.CharField(max_length=20, default='+254712345678');
    website = models.CharField(max_length=100, default='john-doe.com');
    linkedin = models.CharField(max_length=100, default='linkedin.com/in/john-doe');
    github = models.CharField(max_length=150, default='github.com/john-doe');    
    def __str__(self):
        return self.first_name +" "+ self.last_name
class careerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    career_profile = models.TextField(default=f'John Doe is a Software developer with a strong passion for using technology to solve problems. He is proficient in Python, PHP programming languages, MYSQL database and Django framework. He is eager to continue learning and growing as a web developer. He enjoys staying up to date with the latest technology trends. He is team player and is excited to contribute his skills and knowledge to any project.');
    def __str__(self):
        return self.career_profile[0:50]
class professionalSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100, default='Python, PHP, Ruby');
    def __str__(self):
        return self.skill_name[0:50]

class softSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100, default='Analytical skills');
    def __str__(self):
        return self.skill_name

class areaOfInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_of_interest = models.CharField(max_length=100, default='Reading story books');
    def __str__(self):
        return self.name_of_interest

class educationDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=250, default='BSc in Mathematics and Computer Science');
    school_name = models.CharField(max_length=200, default='Technical University of Munich');
    start = models.DateField(max_length=20, default='2018-02-04');
    end = models.DateField(max_length=20, default=date.today);
    def __str__(self):
        return self.course_name[0:50]
class experienceDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, default='Software Developer');
    company = models.CharField(max_length=200, default='Google');
    start = models.DateField(max_length=20, default='2019-04-05');
    end = models.DateField(max_length=20, default=date.today);
    def __str__(self):
        return self.title

class task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experience = models.ForeignKey(experienceDetail, on_delete=models.CASCADE)
    role = models.CharField(max_length=200, default='Developed a website');
    def __str__(self):
        return self.role[0:50]

class reference(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    first_name = models.CharField(max_length=100, default='John')
    last_name = models.CharField(max_length=100, default='Doe')
    title = models.CharField(max_length=100, default='Software Developer')
    email = models.EmailField(default='johndoe@gmail.com')
    phone = models.CharField(max_length=20, default='+254712345678');
    
    def __str__(self):
        return self.first_name +" "+ self.last_name

class professionalCourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    course_name = models.CharField(max_length=100, default='Docker form scratch Course (Udemy)') 
    def __str__(self):
        return self.course_name

class project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    project_name = models.CharField(max_length=100, default='Voting System') 
    description = models.CharField(max_length=100, default='Developed and implemented a voting system.') 
    def __str__(self):
        return self.project_name

class certification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    certification_name = models.CharField(max_length=250, default='Certified AWS Developer');
    school_name = models.CharField(max_length=200, default='Amazon Web Services');
    start = models.DateField(max_length=20, default='2018-02-04');
    end = models.DateField(max_length=20, default=date.today);
    def __str__(self):
        return self.certification_name
