from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import OuterRef, Subquery, F, Avg, Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product, Images, Comment, Category
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


def home(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    main_image_subquery = Images.objects.filter(
        product=OuterRef('pk'),
        is_main=True
    ).values('image')[:1]

    products = products.annotate(
        main_image=Subquery(main_image_subquery)
    ).values('pk', 'title', 'price', 'main_image')

    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'home.html', context)





def store(request):
    main_image_subquery = Images.objects.filter(
        product=OuterRef('pk'),
        # is_main=True
    ).values('image')[:1]

    price_gte = request.GET.get('price__gte')
    price_lte = request.GET.get('price__lte')
    if price_lte and price_gte:
        products = Product.objects.filter(price__gte=price_gte, price__lte=price_lte)
    elif price_gte and not price_lte:
        products = Product.objects.filter(price__gte=price_gte)
    else:
        products = Product.objects.all()

    products = products.annotate(
        main_image=Subquery(main_image_subquery)
    ).values('pk', 'title', 'price', 'main_image')

    products = Paginator(products, 3)
    page = request.GET.get('page')
    try:
        products = products.page(page)
    except (PageNotAnInteger, EmptyPage):
        products = products.page(1)

    # products = ProductFilter(request.GET, queryset=page_products.object_list)
    context = {'products': products}
    return render(request, 'product/store.html', context)

def get_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    main_image_subquery = Images.objects.filter(
        product=OuterRef('pk'),
        # is_main=True
    ).values('image')[:1]

    products = Product.objects.filter(category=category).annotate(
        main_image=Subquery(main_image_subquery)
    ).values('pk', 'title', 'price', 'main_image')

    products = Paginator(products, 3)
    page = request.GET.get('page')
    try:
        products = products.page(page)
    except (PageNotAnInteger, EmptyPage):
        products = products.page(1)

    context = {'products': products, "category": category}
    return render(request, 'product/store.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)


    main_image_subquery = Images.objects.filter(
        product=OuterRef('pk'),
        # is_main=True
    ).values('image')[:1]


    product = Product.objects.filter(pk=pk).annotate(
        main_image=Subquery(main_image_subquery)
    ).first()

    if request.method == "POST":
        text = request.POST.get('text')
        star = request.POST.get('star')
        if request.user.is_authenticated:
            Comment.objects.create(
                product=product,
                owner=request.user,
                text=text,
                star=star if star else 0
            )
            return redirect(reverse('product:detail', kwargs={"pk": product.pk}))

    avg_rating = product.comments.filter(star__gt=0).aggregate(Avg('star'))['star__avg']
    context = {"product": product, "star_avg": avg_rating}
    return render(request, 'product/product_detail.html', context)