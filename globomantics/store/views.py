from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator, PageNotAnInteger
from django.views.generic import View,TemplateView,ListView
from django.contrib import messages
from django.utils.translation import gettext


def index(request):
    #return HttpResponse("Hello there, e-commerce store front coming here...")
    return render(request, "store/index.html")

def detail(request):
    return HttpResponse('This is detail page')

def logout(request):
    try:
        del request.session['customer']
    except KeyError:
        print("Error while logging out")
    return HttpResponse("You're logged out")


def electronis(request):
    items = ("Windows PC","Apple Mac","Apple İphone","Lenovo","Samsung","Google")
    if request.method == 'GET':
        paginator = Paginator(items,2)
        pages = request.GET.get('page',1)
        name = "Mert"
        message = gettext("Customer Successfully Fetched")
        messages.info(request, message)
        try:
            items = paginator.page(pages)
        except PageNotAnInteger:
            items = paginator.page(1)
        response = render(request, 'store/list.html',{'items': items})
        if not request.session.has_key('customer'):
            request.session['customer'] = name
            print("session value set")
        if request.COOKIES.get('visits'):
            value = int(request.COOKIES.get('visits'))
            print('Getting Cookie.')
            response.set_cookie('visits',value+1)
        else:
            value = 1
            print("Setting Cookie.")
            response.set_cookie('visits',value)
        return response


class ElectronicsView(View):
    def get(self,request):
        items = ("Windows PC","Apple Mac","Apple İphone","Lenovo","Samsung","Google")
        if request.method == 'GET':
            paginator = Paginator(items,2)
            pages = request.GET.get('page',1)
            try:
                items = paginator.page(pages)
            except PageNotAnInteger:
                items = paginator.page(1)
            return render(request, 'store/list.html',{'items': items})

class ElectronicsView2(TemplateView):
    template_name = 'store/list.html'
    def get_context_data(self,**kwargs):
        items = ("Windows PC","Apple Mac","Apple İphone","Lenovo","Samsung","Google")
        context = {"items": items}
        return context

class ElectronicsView3(ListView):
    template_name = 'store/list.html'
    queryset = ("Windows PC","Apple Mac","Apple İphone","Lenovo","Samsung","Google")
    context_object_name = 'items'
    paginate_by = 2