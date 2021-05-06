from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Coupon_SU
from socius.models import memberdirectory 
from .forms import Coupon_code_SU_
from django.contrib import messages

def create_SU_coupon_(request):

    directories = memberdirectory.objects.all().filter(user = request.user.id)

    context = {}
    form_su = Coupon_code_SU_(request.POST)
    if request.method == 'POST':
        if form_su.is_valid():
            form_su.save()
            code = form_su.cleaned_data.get('code')
            messages.success(request, 'Coupon Code is generated successfully!')
            return redirect('SuCoupon') 
    
    else:
        form_su = Coupon_code_SU_()

    context['form_su'] = form_su
    context['directories'] = directories

    return render(request, 'Coupons/CouponSUGeneration.html', context)


def Coupon_SU_table(request):
    context = {}
    coupons = Coupon_SU.objects.filter(Name = request.user.get_username())
    context['coupons'] = coupons
    return render(request, 'Coupons/CouponsSU_table.html', context)


def SuCoupon_update(request, id): 

    context ={} 
   
    obj = get_object_or_404(Coupon_SU, id = id) 
   
    form = Coupon_code_SU_(request.POST or None, instance = obj) 
  
    coupons = Coupon_SU.objects.filter(Name = request.user.get_username())

    directories = memberdirectory.objects.all().filter(user = request.user.id)

    for coupon in coupons:
        if request.user.get_username() == coupon.Name:
            if form.is_valid(): 
                form.save() 
                return redirect('SUCoupon_table') 
           
        context["form"] = form
        context['directories'] = directories 
      
        return render(request, "Coupons/SuCoupon_update.html", context)