# Create your views here.

from django.http import HttpResponse,HttpResponseNotFound
from django.http import HttpResponseRedirect,HttpResponseNotAllowed

# HTML rendering libraries.
from django.template.loader import get_template
from django.template import Context

# Data Base libraries.
from pages.models import Page
from pages.models import Subpage 
from pages.models import Article 
from pages.models import New

# Import the parser.
import parser2
import datetime

# Global variable to parse.
try:
	lastStoredDate = New.objects.order_by('-stored_date')[0].stored_date
except:
	lastStoredDate = datetime.date(2000,3,11)

newsParser = parser2.myContentHandler(lastStoredDate);

# ----------------------------------------------------------------------
#                                HOME
# ----------------------------------------------------------------------
# To render correctly the main view (home).
def home(request):

	# choose the template.
	template = get_template("home.html")

	try:
		# Get all the pages.
		allpages = Page.objects.all()

		# Parse the news.
		newsParser.parseNews()

		# Get the last five news (articles).
		try:
			news = New.objects.order_by('-updated_date')[:5]  
		except:
			news = []

		# Last new
		if len(news)>0:
			lastnew = news[0]
		else:
			lastnew = []

	except (ValueError):
		print(ValueError)

	return HttpResponse(template.render(Context({'current_page_path' : "home",
												 'all_pages' : allpages,
												 'news' : news,
												 'lastnew' : lastnew})))  


# ----------------------------------------------------------------------
#                             PAGE HANDLER
# ----------------------------------------------------------------------
# To render correctly the other views (about,documentation,contact,...)
def showNew(request,newID):
	
	# Choose the template.
	try:
		template = get_template("news.html")
	except (ValueError):
		print(ValueError)

	# Find the pages.
	try:
		# Get all the pages.
		allpages = Page.objects.order_by('order')

		# Get default subpages.
		defaultsubpages = Subpage.objects.filter(order=1)

		# Get all the subpages.
		allsubpages = Subpage.objects.filter(rootpage__path__exact="news").order_by('order')

		# The new selected.
		articles = New.objects.filter(pk=newID)

		# Get the last 5 articles modified.
		news = New.objects.order_by('-updated_date')[:5]  

	except (ValueError):
		print(ValueError)

	return HttpResponse(template.render(Context({'current_page_path' : 'news',
												 'current_subpage_path' : 'onenew',
												 'default_subpages' : defaultsubpages,
												 'all_pages' : allpages,
												 'all_subpages' : allsubpages,
												 'articles' : articles,
		                                         'news' : news})))  

# ----------------------------------------------------------------------
#                             PAGE HANDLER
# ----------------------------------------------------------------------
# To render correctly the other views (about,documentation,contact,...)
def pageHandler(request,page,subpage):
	
	# Choose the template.
	try:
		template = get_template(page + ".html")
	except (ValueError):
		print(ValueError)

	# Find the pages.
	try:
		# Get all the pages.
		allpages = Page.objects.order_by('order')

		# Get default subpages.
		defaultsubpages = Subpage.objects.filter(order=1)

		# Get all the subpages.
		allsubpages = Subpage.objects.filter(rootpage__path__exact=page).order_by('order')

		# Finding the articles.
		if subpage == 'allnews':
			# Get all the news.
			articles = New.objects.all().order_by('-updated_date')
		elif subpage == 'onenew':
			# Get the last news.
			articles = [New.objects.order_by('-updated_date')[0]]
		else:
			# Get the articles that are in page/subpage.
			articles = Article.objects.filter(rootsubpage__rootpage__path__exact=page, rootsubpage__path__exact=subpage)

		# Get the last 5 articles modified.
		news = New.objects.order_by('-updated_date')[:5]  

		# Last new
		if len(news)>0:
			lastnew = news[0]
		else:
			lastnew = []

	except (ValueError):
		print(ValueError)

	return HttpResponse(template.render(Context({'current_page_path' : page,
												 'current_subpage_path' : subpage,
												 'default_subpages' : defaultsubpages,
												 'all_pages' : allpages,
												 'all_subpages' : allsubpages,
												 'articles' : articles,
		                                         'news' : news,
		                                         'lastnew' : lastnew})))  


