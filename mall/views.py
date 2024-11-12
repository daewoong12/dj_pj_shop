from django.shortcuts import render,get_object_or_404,redirect
from .models import Stuff,Cart,Order
from .forms import StuffForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime,timedelta
from .models import Order
from .models import Stuff, Comment
from .forms import CommentForm
# Create your views here.

def index(request):
    stuffs=Stuff.objects.all()
    context={'stuffs':stuffs}
    return render(request,'mall/index.html',context)

def detail(request,stuff_id):
    stuff=Stuff.objects.get(id=stuff_id)
    context={'stuff':stuff}
    return render(request,'mall/detail.html',context)

def register_stuff(request):
    if request.method == 'POST':
        form = StuffForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('mall:index')  # 물품 목록 페이지로 리다이렉트
    else:
        form = StuffForm()
    return render(request, 'mall/register.html', {'form': form})
    
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order:
        order.delete()
        messages.success(request, "주문이 성공적으로 취소되었습니다.")
    else:
        messages.error(request, "주문 취소에 실패했습니다.")

    return redirect('mall:info')  # 'order_list'는 주문 목록 페이지의 URL 이름입니다.

@login_required(login_url='common:login')
def info(request):
    orders=Order.objects.filter(user=request.user)
    pub_times=[]
    orderlists=[]
    for order in orders:
        pub_times.append(order.order_date)
    pub_times=list(set(pub_times))
    for pub_time in pub_times:
        total=0
        orders=Order.objects.filter(order_date=pub_time)
        for order in orders:
            total+=order.subtotal
        orderlists.append([orders,total])
    context={'orderlists':orderlists,'username':request.user.username,'email':request.user.email}
    return render(request,'mall/info.html',context)

@login_required(login_url='common:login')
def cart(request):
    uCart=Cart.objects.filter(user=request.user)
    stuffs=uCart
    context={'stuffs':stuffs}
    return render(request,'mall/cart.html',context)

@login_required(login_url='common:login')
def addCart(request,stuff_id):
    uCart=Cart.objects.filter(user=request.user)
    stuff=Stuff.objects.get(id=stuff_id)
    for uCart2 in uCart:
        if uCart2.stuffs.id==stuff_id:
            uCart2.quantity+=1
            uCart2.save()
            break
    else:
        uCart2=Cart.objects.create(user=request.user,stuffs=stuff)
        uCart2.quantity+=1
        uCart2.save()
        
    return  redirect('mall:cart')

@login_required(login_url='common:login')
def subCart(request,stuff_id):
    uCart=Cart.objects.filter(user=request.user)
    for uCart2 in uCart:
        if uCart2.stuffs.id==stuff_id:
            uCart2.delete()
            break
    return  redirect('mall:cart')

@login_required(login_url='common:login')
def plusStuff(request,stuff_id):
    uCart=Cart.objects.filter(user=request.user)
    for uCart2 in uCart:
        if uCart2.stuffs.id==stuff_id:
            uCart2.quantity+=1
            uCart2.save()
            break
    return  redirect('mall:cart')

@login_required(login_url='common:login')
def minusStuff(request,stuff_id):
    uCart=Cart.objects.filter(user=request.user)
    for uCart2 in uCart:
        if uCart2.stuffs.id==stuff_id:
            uCart2.quantity-=1
            uCart2.save()
            if uCart2.quantity==0:
                uCart2.delete()
            break
    return  redirect('mall:cart')


@login_required(login_url='common:login')
def buyAtIndex(request,stuff_id):
    uCart=Cart.objects.filter(user=request.user)
    stuff=Stuff.objects.get(id=stuff_id)
    for uCart2 in uCart:
        if uCart2.stuffs.id==stuff_id:
            uCart2.quantity+=1
            uCart2.save()
            break
    else:
        uCart2=Cart.objects.create(user=request.user,stuffs=stuff)
        uCart2.quantity+=1
        uCart2.save()
    return  redirect('mall:cart')

@login_required(login_url='common:login')
def buy(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        
        if not cart_items.exists():
            messages.error(request, '장바구니가 비어 있습니다.')
            return redirect('mall:cart')
        
        for cart_item in cart_items:
            stuff = cart_item.stuffs
            quantity = cart_item.quantity

            if quantity > 0 and quantity <= stuff.stock:
                # 주문 생성
                Order.objects.create(
                    user=request.user,
                    stuff=stuff,
                    quantity=quantity,
                    order_date=datetime.now(),
                    subtotal=stuff.price * quantity
                )
                # 재고 차감
                stuff.stock -= quantity
                stuff.save()
                # 장바구니에서 제거
                cart_item.delete()
            else:
                messages.error(request, f'{stuff.name}의 재고가 부족합니다.')
                return redirect('mall:cart')

        messages.success(request, '구매가 완료되었습니다.')
        return redirect('mall:info')  # 구매 후 내 정보 페이지로 리다이렉트

    return redirect('mall:cart')  # GET 요청 시 장바구니 페이지로 리다이렉트

def product_list(request):
    stuffs = Stuff.objects.all()  # 등록된 모든 물품 가져오기
    return render(request, 'mall/index.html', {'stuffs': stuffs})

def add_to_cart(request, stuff_id):
    stuff = get_object_or_404(Stuff, id=stuff_id)

    if stuff.stock > 0:  # 재고가 있는 경우에만 추가 가능
        cart_item, created = Cart.objects.get_or_create(user=request.user, stuffs=stuff)
        if not created:
            cart_item.quantity += 1  # 이미 존재하면 수량 증가
        cart_item.save()

        # 재고 감소
        stuff.stock -= 1
        stuff.save()

        return redirect('mall:cart')
    else:
        return render(request, 'mall/error.html', {'message': '재고가 부족합니다.'})
    
def cancel_order(request, order_id):
    # 주문 객체 가져오기
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # 해당 주문의 재고 복구
    stuff = order.stuff
    stuff.stock += order.quantity
    stuff.save()

    # 주문 삭제
    order.delete()

    # 주문 정보 페이지로 리다이렉트
    return redirect('mall:info')  # 주문 정보 페이지로 이동

def update_stuff(request, stuff_id):
    stuff = get_object_or_404(Stuff, id=stuff_id)
    
    if request.method == 'POST':
        form = StuffForm(request.POST, request.FILES, instance=stuff)
        if form.is_valid():
            form.save()
            return redirect('mall:product_list')  # 수정 후 목록 페이지로 리다이렉트
    else:
        form = StuffForm(instance=stuff)
    
    return render(request, 'mall/register.html', {'form': form, 'is_update': True})

def delete_stuff(request, stuff_id):
    stuff = get_object_or_404(Stuff, id=stuff_id)
    
    if request.method == 'POST':
        stuff.delete()
        return redirect('mall:product_list')  # 삭제 후 목록 페이지로 리다이렉트
    
def detail(request, stuff_id):
    stuff = get_object_or_404(Stuff, id=stuff_id)
    comments = stuff.comments.all().order_by('-created_at')  # 해당 상품의 댓글을 불러옴

    if request.method == 'POST':
        if not request.user.is_authenticated:  # 로그인 여부 확인
            messages.error(request, "로그인 후에 댓글을 작성할 수 있습니다.")
            return redirect('mall:detail', stuff_id=stuff.id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.stuff = stuff
            comment.save()
            return redirect('mall:detail', stuff_id=stuff.id)
    else:
        form = CommentForm()

    return render(request, 'mall/detail.html', {
        'stuff': stuff,
        'form': form,
        'comments': comments,
    })

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
    return redirect('mall:detail', stuff_id=comment.stuff.id)

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('mall:detail', stuff_id=comment.stuff.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'mall/edit_comment.html', {'form': form, 'comment': comment})