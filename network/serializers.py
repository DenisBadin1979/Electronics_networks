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
        read_only_fields = ('node',)  # поле node будет устанавливаться автоматически


class NetworkNodeSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(source='contact', read_only=True)  # обратная связь
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkNode
        fields = ['id', 'name', 'contact', 'products', 'supplier', 'debt', 'created_at', 'level']
        read_only_fields = ['created_at', 'level']


class NetworkNodeCreateSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()  # вложенный сериализатор для создания контакта
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    class Meta:
        model = NetworkNode
        fields = ['name', 'contact', 'products', 'supplier', 'debt']

    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        products = validated_data.pop('products')
        # Сначала создаём узел (без контакта)
        node = NetworkNode.objects.create(**validated_data)
        # Создаём контакт, привязывая к узлу
        Contact.objects.create(node=node, **contact_data)
        node.products.set(products)
        return node


class NetworkNodeUpdateSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()  # для обновления контакта
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    class Meta:
        model = NetworkNode
        fields = ['name', 'contact', 'products', 'supplier']  # поле debt исключено

    def update(self, instance, validated_data):
        contact_data = validated_data.pop('contact', None)
        products = validated_data.pop('products', None)

        # Обновляем контакт, если есть данные
        if contact_data:
            contact_serializer = ContactSerializer(instance.contact, data=contact_data)
            if contact_serializer.is_valid(raise_exception=True):
                contact_serializer.save()

        # Обновляем список продуктов
        if products is not None:
            instance.products.set(products)

        # Обновляем остальные поля узла (кроме debt)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance