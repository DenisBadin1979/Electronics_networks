from rest_framework import serializers
from .models import NetworkNode, Contact, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class NetworkNodeSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    supplier = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = NetworkNode
        fields = ['id', 'name', 'contact', 'products', 'supplier', 'debt', 'created_at', 'level']
        read_only_fields = ['created_at', 'level']


class NetworkNodeCreateSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    class Meta:
        model = NetworkNode
        fields = ['name', 'contact', 'products', 'supplier', 'debt']

    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        products = validated_data.pop('products')
        contact = Contact.objects.create(**contact_data)
        node = NetworkNode.objects.create(contact=contact, **validated_data)
        node.products.set(products)
        return node


class NetworkNodeUpdateSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    class Meta:
        model = NetworkNode
        fields = ['name', 'contact', 'products', 'supplier']  # поле debt исключено

    def update(self, instance, validated_data):
        contact_data = validated_data.pop('contact', None)
        products = validated_data.pop('products', None)

        if contact_data:
            contact_serializer = ContactSerializer(instance.contact, data=contact_data)
            if contact_serializer.is_valid(raise_exception=True):
                contact_serializer.save()

        if products is not None:
            instance.products.set(products)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance