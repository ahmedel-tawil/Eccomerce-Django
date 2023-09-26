from celery import shared_task
from celery.utils.log import get_task_logger
from time import sleep
from .order_confirmation_email import send_order_confirmation_email

logger = get_task_logger(__name__)


# Order Confirmation task
@shared_task(name='send_oc_mail_task')
def send_oc_mail_task(email, order):
    logger.info("send Order Conf Email")
    return send_order_confirmation_email(email, order)
