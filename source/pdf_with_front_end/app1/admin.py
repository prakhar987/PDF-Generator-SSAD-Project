from django.contrib import admin
from app1.models import Company
from app1.models import User
from app1.models import Test
from app1.models import TestSectionDef
from app1.models import Question
from app1.models import TestSectionQuestions
from app1.models import QuestionAnswer
from app1.models import TestCandidateQuestionHistory
admin.site.register(Company)
admin.site.register(User)
admin.site.register(Test)
admin.site.register(TestSectionQuestions)
admin.site.register(TestSectionDef)
admin.site.register(Question)
admin.site.register(QuestionAnswer)
admin.site.register(TestCandidateQuestionHistory)




# Register your models here.
