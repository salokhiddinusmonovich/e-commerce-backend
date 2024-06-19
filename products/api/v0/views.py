from django.db.models import Prefetch, OuterRef, Subquery
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from .serializers import CategorySerializer, ProductSerializer, ProductDetailSerializer, CommentCreateSerializer
from ...models import Category, Product, Comment, Images


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        category_list = cache.get('category_list')
        if category_list is None:
            category_list = Category.objects.all()
            cache.set('category_list', category_list)
        return category_list
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     ids = [1, 3]
    #     qs = qs.filter(id__in=ids)
    #     return qs

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


    def get_queryset(self):
        products = cache.get('product_list')
        if products is None:
            # products = Product.objects.prefetch_related(
            #     Prefetch('images_set', queryset=Images.objects.order_by('id'))
            #
            # )
            main_image_subquery = Images.objects.filter(
                product=OuterRef('pk'),
                # is_main=True
            ).values('image')[:1]
            products = Product.objects.annotate(
                main_image=Subquery(main_image_subquery)
            )
            cache.set('product_list', products)
        # cache.delete('product_list')
        return products


class ProductByCategoryListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        cache_key = f'products_by_category_{category_id}'
        products_by_category = cache.get(cache_key)

        if products_by_category is None:
            main_image_subquery = Images.objects.filter(
                product=OuterRef('pk'),
                is_main=True
            ).values('image')[:1]

            products = Product.objects.filter(category_id=category_id).annotate(
                main_image=Subquery(main_image_subquery)
            )
            cache.set(cache_key, products)
            products_by_category = products

        return products_by_category

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     pk = self.kwargs.get('pk')
    #     qs = qs.filter(category=pk)
    #     return qs

class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        product_detail = cache.get(f'product_detail_{pk}')
        if product_detail is None:
            queryset = Product.objects.select_related('category'
                                                      ).prefetch_related('images_set').all()
            cache.set(f'product_detail_{pk}', queryset)
        return product_detail





# class CommentCreateView(APIView):
#     permission_classes = ()
#     def post(self, request):
#         comment = CommentCreateSerializer(data=request.data)
#         if comment.is_valid():
#             comment.save()
#         return Response({"message":"Successfully created!"}, status=status.HTTP_201_CREATED)




class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)