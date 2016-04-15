from django.db import models

class Company(models.Model):    
    id         = models.AutoField(primary_key=True)
    name    = models.CharField(max_length=512)
    logo    = models.ImageField(upload_to='images/company/',null=False)

class User(models.Model):#AbstractEmailUser):
    first_name = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)
    company = models.ForeignKey(Company)
    picture = models.ImageField(upload_to = 'images/company/', null=False)
    phone = models.CharField(max_length=15)

class Test(models.Model):
    id = models.AutoField(primary_key=True)    
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company)

class TestSectionDef(models.Model):  ## tests are divided into sections - reports will also need to be divided into sections
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company)

class Question (models.Model): # for mcq
    id = models.AutoField(primary_key=True)
    text = models.TextField ()
    difficulty_level = models.CharField(max_length=1, default='3')   ## levels 1-4 - easy, medium, difficult, very difficult
    company = models.ForeignKey(Company, null=True) 


class TestSectionQuestions(models.Model):  ## table where sections and questions get mapped to a test
    id = models.AutoField(primary_key=True)
    test = models.ForeignKey(Test)
    section = models.ForeignKey(TestSectionDef)
    duration = models.IntegerField(blank=True, null=True)
    questions = models.ManyToManyField(Question)  # list of questions that in under a section

class QuestionAnswer (models.Model): # for mcq
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1024)
    question = models.ForeignKey(Question)


class TestCandidateQuestionHistory(models.Model):  # questions answered by the candidate
    question = models.ForeignKey(Question)
    candidate = models.ForeignKey(User) #AUTH_USER_MODEL)
    test = models.ForeignKey(Test)
    answer = models.ForeignKey(QuestionAnswer, null=True)
    answer_dateTime = models.DateTimeField(null=True)
    section = models.ForeignKey(TestSectionDef)
    duration = models.SmallIntegerField(default=0)
    status = models.SmallIntegerField(default=0) # 0 = wrong answer, 1 = right answer
    score = models.SmallIntegerField(default=0)   ## 0 if wrong answer


