from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
import json
from django.views.decorators.csrf import csrf_exempt
from push_notifications.models import GCMDevice,APNSDevice

from rest_framework import viewsets
from serializers import *
from suds.xsd.doctor import ImportDoctor, Import
from suds.client import Client

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from web.models import *
from push_notifications.models import GCMDevice

def getCategories(request):
    if request.method == "GET":
           categories = Category.objects.all()
           response = render_to_response(
               'json/category.json',
               {'categories': categories},
               context_instance=RequestContext(request)
           )
           response['Content-Type'] = 'application/json; charset=utf-8'
           response['Cache-Control'] = 'no-cache'
           return response


def getDishes(request):
    if request.method == "GET":
           dishes = RestaurantDish.objects.raw('select * from web_restaurantdish')
           response = render_to_response(
               'json/restaurant_dish.json',
               {'dishes': dishes},
               context_instance=RequestContext(request)
           )
           response['Content-Type'] = 'application/json; charset=utf-8'
           response['Cache-Control'] = 'no-cache'
           return response



def isinlist( dishes, dish):
    for d in dishes:
        if (d.id ==  dish.id):
            return True
    return False

def getDishesCategory(categorys):
    categories = []
    dishes = []
    for category in categorys:
        categories.append(category.evaluation)
    restaurantdishes = RestaurantDish.objects.all()
    cont = 0
    for dish in  restaurantdishes:
        for evaluation in categories:
            evaluations = EvaluationCriteria.objects.filter(restaurantdish = dish, evaluation = evaluation)
            if (len(evaluations)>0):
                cont = cont +1
        if (cont == len(categories)):
            dishes.append(dish)
        cont = 0

    result = []
    for dish in dishes:
        votes = 0
        for category in categorys:
            for evaluation in EvaluationCriteria.objects.filter(restaurantdish = dish, evaluation = category.evaluation):
                votes = votes + evaluation.points
        result.append((dish,votes))
    return  result

def getTopFull(request):
    if request.method == 'GET':
        id_category = 0
        id_category = request.GET.get('category', False)
        try:
            id_category = int(id_category)
        except:
            return HttpResponseBadRequest(json.dumps({'error':'parametros errados'}))
        if (id_category ==0):
            categorys = Category.objects.all()
        else:
            categorys = Category.objects.filter(pk = id_category)
        results = []
        for category in categorys:
            evaluations = CategoryCriteria.objects.filter(category = category)
            from operator import itemgetter, attrgetter
            result = getDishesCategory(evaluations)
            results.append((category, sorted(result, key=itemgetter(1), reverse = True)))
        dishes = results
        response = render_to_response(
            'json/category_dishes.json',
            {'dishes': dishes},
            context_instance=RequestContext(request)
        )
        restaurants_ = RestaurantDish.objects.filter(restaurant = 1)
        i = 0
        restaurants = []
        for restaurant in restaurants_:
           restaurants.append((i,restaurant))
           i = i +1
        template = 'web/list.html'
        return render_to_response(template,{'dishes':dishes, 'restaurants':restaurants}, context_instance= RequestContext(request))

#        response['Content-Type'] = 'application/json; charset=utf-8'
 #       response['Cache-Control'] = 'no-cache'
  #      return response

def getByFilter(request):
    if request.method == 'GET':
        name =  request.GET.get('name', False)
        restaurant = request.GET.get('restaurant', False)
        category = request.GET.get('category', False)
        filters = []
        results = []
        for f in [('name',name), ('restaurant',restaurant), ('category',category)]:
            if (f[1]):
                    filters.append((f))
        dishes = []
        for f in filters:
            if(f[0]=='name'):
                dishes = RestaurantDish.objects.filter(name__contains =f[1])
                results = dishes
                if (len(results)==0):
                    break
            elif(f[0]=='restaurant'):
                if(len(dishes)==0):
                    dishes = RestaurantDish.objects.filter(restaurant = f[1])
                    results = dishes
                    if (len(results)==0):
                        break
                else:
                    results = []
                    for d in dishes:
                        if (str(d.restaurant.id) == str(f[1])):
                            results.append(d)
                    if (len(results)==0):
                        break
                    dishes = results
            elif(f[0]=='category'):
                categorys = Category.objects.filter(pk = f[1])
                if (len(categorys)>0):
                    evaluations = CategoryCriteria.objects.filter(category = categorys)
                    from operator import itemgetter, attrgetter
                    result = getDishesCategory(evaluations)
                    result = sorted(result, key=itemgetter(1), reverse = True)
                    if(len(dishes)==0):
                        for r in result:
                            results.append(r[0])
                    else:
                        results=[]
                        for d in dishes:
                            for r in result:
                                if(r[0].id == d.id):
                                   results.append(d)
                else:
                    return HttpResponseBadRequest(json.dumps({'error':'parametros errados'}))

        dishes = results
        response = render_to_response(
            'json/dishes.json',
            {'dishes': dishes},
            context_instance=RequestContext(request)
        )
        response['Content-Type'] = 'application/json; charset=utf-8'
        response['Cache-Control'] = 'no-cache'
        template = 'web/list2.html'
        return render_to_response(template,{'dishes':dishes}, context_instance= RequestContext(request))

def get_user(email, username):
    mail = User.objects.filter(email=email.lower())
    nick = User.objects.filter(username = username.lower())
    return not(len(mail)>0 or len(nick)>0)


@csrf_exempt
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        password = request.POST['password']
        exist = get_user(email, username)
        if exist:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            #user = authenticate(username=user, password=password)
            #login
            response = { 'id' : user.id }
            response['status'] = 'ok'
            return HttpResponse(json.dumps(response))
        else:
            #messages
            response = {'error':'ya existe el nombre de usuario o esta registrado'}

        return HttpResponseBadRequest(json.dumps(response))
    elif request.method == "GET":
        return HttpResponse(json.dumps({}))

@never_cache
@csrf_exempt
def login(request):
    #if not request.is_ajax() or request.method != 'GET':
    #    return
    try:
        username = request.POST['username']
        password = request.POST['password']
    except:
        return HttpResponseBadRequest('Bad parameters')

    from django.contrib.auth import authenticate, login
    auth = authenticate(username = user , password = password)

    if auth is not None:
        login(request, auth)
        response_content = {
                'id':user.id,
                'username': user.username,
                'email': user.email,
                'firstname': user.first_name,
                'lastname': user.last_name,
            }
        response =  HttpResponse(json.dumps(response_content))
        response['Content-Type'] = 'application/json; charset=utf-8'
        response['Cache-Control'] = 'no-cache'
        return response

    else:

        url = 'http://ws.espol.edu.ec/saac/wsandroid.asmx?WSDL'
        imp = Import('http://www.w3.org/2001/XMLSchema')
        imp.filter.add('http://tempuri.org/')
        doctor = ImportDoctor(imp)
        client = Client(url, doctor=doctor)
        auth = client.service.autenticacion(user,pwd)

        if auth == True:
            auth = User.objects.create_user(username=user, password=pwd)
            auth.save()
            auth = authenticate(username = user , password = pwd)
            #auth = User.objects.filter(username = user)
            login(request,auth)
            auth_pk = auth.pk
            response_content = {
                'id':user.id,
                'username': user.username,
                'email': user.email,
                'firstname': user.first_name,
                'lastname': user.last_name,
            }
            response =  HttpResponse(json.dumps(response_content))
            response['Content-Type'] = 'application/json; charset=utf-8'
            response['Cache-Control'] = 'no-cache'
            return response

        else:
            #self.username = None
            #self.password = None
            return HttpResponseForbidden('Autenticacion Fallida')
    return HttpResponseBadRequest('Usuario o clave incorrecto')


from django.contrib.auth import logout
@never_cache
def logout(request):
    logout(request)
    return redirect('/')

@never_cache
def getRestaurants(request):

    if request.method == "GET":
        restaurants = Restaurant.objects.all()

        response = render_to_response(
            'json/restaurants.json',
            {'restaurants': restaurants},
            context_instance=RequestContext(request)
        )
        response['Content-Type'] = 'application/json; charset=utf-8'
        response['Cache-Control'] = 'no-cache'
        return response

def push_notifications_view(request):
    if request.method == "POST":
        if 'code' in request.POST:
            code = request.POST['code']

            devices = GCMDevice.objects.all()
            devices.send_message("Pruebaaaaa !!!")
            message = "message sent to android devices"


            #if code == 'android':
            #    print 'code == android'
            #    devices = GCMDevice.objects.all()
            #    devices.send_message({"message": "Hi Android!"})
            #    message = "message sent to android devices"

            #elif code == 'ios':
            #    print 'code == ios'
            #    devices = APNSDevice.objects.all()
            #    devices.send_message("Hi iOS!")
            #    message = "message sent to ios devices"

            #elif code == 'simple':
            #    print 'code == simple'

            #    device = APNSDevice.objects.get(registration_id='mi apns token')
            #    device.send_message(None, extra={"foo": "bar"})
            #    message = "simple message sent"

    return render_to_response('main.html', locals(), context_instance=RequestContext(request))


class GCMDeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows words to be viewed or edited.
    """
    queryset = GCMDevice.objects.all()
    serializer_class = GCMDeviceSerializer

def rank(request):
    #get top [:1]
    if request.method == 'GET':
        categorys = Category.objects.all()
        results = []
        for category in categorys:
            evaluations = CategoryCriteria.objects.filter(category = category)
            from operator import itemgetter, attrgetter
            result = getDishesCategory(evaluations)
            result = result[:1]
            results.append((category, sorted(result, key=itemgetter(1), reverse = True)))
        dishes = results
        template = 'web/list.html'
        return render_to_response(template,{'dishes':dishes}, context_instance= RequestContext(request))

def lasthuecas(request):
    if request.method == 'GET':
        lasthuecas = list(RestaurantDish.objects.all())[-5:]
        template = 'web/list_last.html'
        return render_to_response(template,{'dishes':lasthuecas}, context_instance= RequestContext(request))


