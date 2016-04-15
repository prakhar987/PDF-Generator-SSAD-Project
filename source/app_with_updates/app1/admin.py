from django.contrib import admin
from app1.models import * # Company
admin.site.register(Company)
admin.site.register(User)
admin.site.register(Test)
admin.site.register(TestSectionQuestions)
admin.site.register(TestSectionDef)
admin.site.register(Question)
admin.site.register(QuestionAnswer)
admin.site.register(TestCandidateQuestionHistory)
admin.site.register(TestParagraph)
admin.site.register(TestChatTranscripts)
admin.site.register(MediaFiles)



# Register your models here.
