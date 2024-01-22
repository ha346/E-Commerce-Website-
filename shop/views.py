from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Order,OrderUpdate
from math import ceil

import json
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
MERCHANT_KEY = 'kbzk1DSbJiV_03p5';

def index(request):
    # return HttpResponse("Shop Index")

    # products = Product.objects.all() 
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
    # allProds=[[products,range(1,nSlides),nSlides],
    #           [products,range(1,nSlides),nSlides ]
    #          ]

    allProds=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        # print(prod)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request,"shop/about.html")

def contact(request):
    thank=False
    if(request.method=="POST"):
        name=request.POST.get('name',"")
        email=request.POST.get('email',"")
        phone=request.POST.get('phone',"")
        desc=request.POST.get('desc',"")
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank=True
    return render(request,"shop/contact.html",{'thank':thank})

def tracker(request):
    if(request.method=="POST"):
        orderid=request.POST.get('orderid','')
        email=request.POST.get('email','')
        # console.log(f"{orderid} {email}")
        try:
            orders=Order.objects.filter(order_id=orderid,email=email)
            if(len(orders)>0):
                update=OrderUpdate.objects.filter(order_id=orderid)
                updates=[]
                for item in update:
                    updates.append({'text':item.order_desc,'time':item.timestamp})
                    response=json.dumps({'status':"success",'updates':updates,'itemsJson':orders[0].items_json},default=str)   # json.dumps convert object into string.
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
                # return HttpResponse(f"{e}")
                return HttpResponse('{"status":"error"}')

    return render(request,"shop/tracker.html") 

def productview(request,myid):
    product=Product.objects.filter(id=myid)
    print("Productssssssssss",product)
    return render(request,"shop/productView.html",{'product':product[0]})

def checkout(request):
    if(request.method=="POST"):
        items_json=request.POST.get('itemsJson','')
        name=request.POST.get('name','')
        amount=request.POST.get('amount','')
        email=request.POST.get('email','')
        address=request.POST.get('address1','') + " " + request.POST.get("address2",'')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip','')
        phone=request.POST.get('phone','')
        orders=Order(items_json=items_json,name=name,amount=amount,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone)
        orders.save();
        thank=True;
        id=orders.order_id;
        update=OrderUpdate(order_id=orders.order_id,order_desc="The order has been placed")
        update.save()
        return render(request,'shop/checkout.html',{'thank':thank,'id':id})
          # Request paytm to transfer the amount to your account after payment by user
        # param_dict = {

        #         'MID': 'WorldP64425807474247',
        #         'ORDER_ID': str(orders.order_id),
        #         'TXN_AMOUNT': str(amount),
        #         'CUST_ID': 'shuklaharsh83267@gmail.com',
        #         'INDUSTRY_TYPE_ID': 'Retail',
        #         'WEBSITE': 'WEBSTAGING',
        #         'CHANNEL_ID': 'WEB',
        #         'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        # }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        # return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    
    return render(request,"shop/checkout.html")

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {} 
    checksum="No"
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH': 
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
