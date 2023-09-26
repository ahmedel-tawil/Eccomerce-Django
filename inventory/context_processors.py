from .models import Brand


def brand_list(request):
    brand = Brand.objects.all()
    return {'brand': brand}
