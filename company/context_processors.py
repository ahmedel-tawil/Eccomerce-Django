from .models import Company


def company_context(request):
    company = Company.objects.get(is_main=True)
    return {'company': company}
