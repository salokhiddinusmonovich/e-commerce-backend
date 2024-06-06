from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CategorySerializer, ProductSerializer, ProductDetailSerializer, CommentCreateSerializer
from  ...models import Category, Product, Comment


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     ids = [1, 3]
    #     qs = qs.filter(id__in=ids)
    #     return qs

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductByCategoryListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        pk = self.kwargs.get('pk')
        qs = qs.filter(category=pk)
        return qs

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.select_related('category'
                                              ).prefetch_related('images_set').all()
    serializer_class = ProductDetailSerializer



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