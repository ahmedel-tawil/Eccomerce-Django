from rest_framework import serializers

from inventory.models import Product


class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'code',
            'category_name',
            'sale_price',
            'product_price',
            'discount_price',
            'slug',
            'description_l',
            'description_s',

        )

    def get_category(self, obj):
        return obj.get_category_display()
    #
    # def get_label(self, obj):
    #     return obj.get_label_display()


class ProductDetailSerializer(serializers.ModelSerializer):
    # category = serializers.SerializerMethodField()
    # label = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'code',
            'category',
            'sale_price',
            'product_price',
            'discount_price',
            'slug',
            'description_l',
            'description_s',

        )

    # def get_category(self, obj):
    #     return obj.get_category_display()
    #
    # def get_label(self, obj):
    #     return obj.get_label_display()
