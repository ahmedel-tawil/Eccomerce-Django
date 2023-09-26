from django.db.models.signals import post_save
from django.dispatch import receiver

from sales.models import OrderItem, Order
from inventory.models import Product, ProductAttribute


@receiver(post_save, sender=Order)
def update_item(sender, instance, created, **kwargs):
    if instance.ordered:
        for item in instance.items.all():
            item_to_update = ProductAttribute.objects.get(product__slug=item.product.slug,
                                                          size__title=item.size.size.title)
            item_to_update.qty = item_to_update.qty - item.quantity
            item_to_update.save()

        # print("fetch the items")
        # print(items)
        # for item in items:
        #     #  item_to_update = ProductAttribute.objects.get(size=item.size)
        #     item_to_update = ProductAttribute.objects.get(product__slug=item.product.slug,
        #                                                   size__title=item.size.size.title)
        #     print(item_to_update.qty)
        # item_to_update.qty = item_to_update.qty - item.quantity
        # item_to_update.save()

        # print(item_to_update.qty)
        # int('Stock level updated...')

        # print(items)
        # for x in items_bought:
        #     item_to_update = Product.objects.get(id=x.product.id)
        #     print('product name ', x.product.name, ' availble-qty ', item_to_update.available_qty,
        #           ' quantity-purchased ', x.quantity)
        #     # item_to_update.available_qty = item_to_update.available_qty - x.quantity
        #     # item_to_update.save()
        #     print('Stock level updated...')
