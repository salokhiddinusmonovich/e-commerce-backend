from rest_framework import serializers

from products.models import Product, Category, Comment, Images

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name', 'order', 'type']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['type_name'] = instance.get_type_display()
        return data

class ProductSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['pk', 'title', 'price', 'main_image']

    def get_main_image(self, obj):
        main_image = Images.objects.filter(product=obj).first()
        if main_image and main_image.image:
            return main_image.image.url
        return ""


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['pk', 'image']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'pk', 'title', 'description', 'price', 'quantity', 'detail', 'images', 'category'
        ]

    def get_images(self, obj):
        images = Images.objects.filter(product=obj)
        serializers = ImageSerializer(images, many=True)

        return serializers.data