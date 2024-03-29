from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from .models import Question,Choice
from django.utils import timezone

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions."""
		#return Question.objects.order_by('-pub_date')[:5]
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
		
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	output = ', '.join([q.question_text for q in latest_question_list])	
	#template = loader.get_template('polls/index.html')
	context = {'latest_question_list': latest_question_list,}
	#return HttpResponse(template.render(context, request))
	return render(request,'polls/index.html',context)
	
def detail(request, question_id):
	'''try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		message = "There is No Such Question for Given Question ID"
		return render(request, 'polls/error404.html', {'message': message})
	return render(request, 'polls/detail.html', {'question': question})'''
	question = get_object_or_404(Question,pk=question_id)
	return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
		'question': question,
		'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('results', args=(question.id,)))
		#return render(request,"polls/results.html")

def first(request):
	response = HttpResponse(" Good Morning ")
	response.set_cookie('name','Grapess Solutions')
	request.session["name"] = "Mukesh Jamwal"
	return response

def second(request):
	result = " Second Morning " + str(request.session.session_key)
	if "name" in request.session:
		result += " Name : " + str(request.session["name"])
	print(type(request.session))
	if "sessionid" in request.COOKIES:
		result += " Session ID : " + str(request.COOKIES["sessionid"])
	response = HttpResponse(result)
	return response

def clear_data(request):
	response = HttpResponse("Clear All Cookie Data")
	response.delete_cookie("name")
	response.delete_cookie('sessionid')
	return response