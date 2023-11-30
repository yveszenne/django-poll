import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    """
    create a question with the given `question_text` and published the givern number of `days` offset to now
    (negative for questions published in the past, positive for questions that have yet to be published) 
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
    
class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """
        if no question exists, an appropriate message is displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
    
    def test_past_question(self):
        """
        questions with pub_date in the past are displayed on the index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question],)
    
    def test_future_question(self):
        """
        questions with a pub_date in the future aren't displayed on the index page
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
    
    def test_future_question_and_past_question(self):
        """
        even if both past and future questions exists, only past question are displayed
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question],)

    def test_two_past_questions(self):
        """
        the question index page may display multiple questions
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question2, question1],)

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        the detail view of a question with a pub_date in the future returns a 404 not found
        """
        future_question = create_question(question_text="Future question", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response =self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        the detail view of a question with a pub_date in the past displays the question's text
        """
        past_question = create_question(question_text="Past question", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

        
        
        
        


        
        
        
        
        
        
        



        
        
        
        
        
        
