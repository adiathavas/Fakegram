from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice, User
from django.views import generic
from django.utils import timezone
from .forms import LoginForm, InputForm
# from .caption_generator.py import Instabot, classify
from . import caption_generator
from . import config
from . import devices

counter = False
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            counter = False
            text1 = form.cleaned_data['Login']
            print("hooorahhhhhhh " + text1)
            text2 = form.cleaned_data['Password']
            form = LoginForm()

            bot = caption_generator.Instabot('portia_res', 'havas-reasearch')
            bot.login()
            # return redirect()
            return HttpResponseRedirect(reverse('polls:loginsuccess'))
        else:
            counter = True

            args = {'form': form, 'text1': text1, 'text2': text2 }
        return render(request, self.template_name, args )

class TopicView(generic.ListView):
    model = User
    template_name = 'polls/topic.html'

    def get(self, request):
        form = InputForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = InputForm(request.POST)
        # str = ""
        argument = form.get_data()
        # print(argument.to_python(argument, str))
        # print("this is the string" + str)
        bot = caption_generator.Instabot('portia_res', 'havas-reasearch')
        bot.login()

        """assume i have the right input, now calling post_2"""

        #dynamic version not working properly - currently a little hard coded
        # bot.post_2(argument.to_python())
        bot.post_2('toronto')

        return HttpResponseRedirect(reverse('polls:loginsuccess'))

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())



#login to IG
class LoginsuccessView(generic.ListView):
    model = User

    template_name = 'polls/loginsuccess.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return User.objects.get(pk=1)

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

#
# def login( username, password):
#     # user = get_object_or_404(User, pk=user_id)
#     print('login jazz here')
#     print(username, password)




def posting(request):
    option = get_object_or_404(User)

    # try:
    #     selected_choice = option.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting .
    #     return render(request, 'polls/loginsuccess.html', {
    #         'error_message': "You didn't select a choice.",
    #     })
    # else:
    #     if selected_choice.id == 1:

    # bot = caption_generator.Instabot('portia_res', 'havas-reasearch')
    # bot.login()
    #
    # bot.post()



    # selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:topic'))


# def topic(request):
#     print("yodelling")



# def topic(request):
#     form = InputForm(request.POST)
#     if form.is_valid():
#         counter = False
#         # bot = caption_generator.Instabot('portia_res', 'havas-reasearch')
#         # bot.login()
#         # return redirect()
#
#         return HttpResponseRedirect(reverse('polls:loginsuccess'))
