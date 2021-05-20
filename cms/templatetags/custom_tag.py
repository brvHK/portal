
from datetime import date
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
##logging.basicConfig(level=logging.DEBUG, 
#    filename="/home/pi/site/kakeibo/logs/debug.log",
#    format="%(asctime)s %(levelname)-7s %(message)s")

from django import template
register = template.Library()

from kakeibo.models import Kakeibo
from kakeibo.models import CategoryDetail
today = date.today()

def check_category_detail(category_detail_name=None):
    tartget_category_detail = None

    try:
        tartget_category_detail = CategoryDetail.objects.get(name=category_detail_name)
    except CategoryDetail.DoesNotExist:
        logger.error("{0}という小カテゴリはない!".format(category_detail_name))
    except CategoryDetail.MultipleObjectsReturned:
        logger.error("{0}という小カテゴリがいくつかある!".format(category_detail_name))
    return tartget_category_detail


@register.simple_tag
def a():
    return "a"

@register.inclusion_tag("kakeibo/hello.html")
def hello_world(user):
    logger.debug("make_messages")
    return {'hello': 'hello {0}'.format(user)}

@register.inclusion_tag("kakeibo/messages.html",takes_context=True)
def kakeibo_messages(context, **kwargs):
    logger.debug("make_messages")

    '''
    与えられた年月に対する家計簿のメッセージを返す。
    例えば、電気代、水道代が登録されていない、
    未分類の家計簿があるなど

    Parameters
    ----------
        year : int
            メッセージを年
        month : 

    Returns
    ----------  
        messages : list
            メッセージ

    '''

    messages = list()
    year =context["year"]
    month = context["month"]
    kazoku = context['kazoku_in_session']
    logger.debug("{0}/{1}".format(year, month))

    # 電気代
    denkidai = check_category_detail(category_detail_name="電気代")
    denkidai_message = make_not_reisterd_message(denkidai, year, month,kazoku)
    if denkidai_message:
        messages.append(denkidai_message)
    # ガス代
    gasudai = check_category_detail(category_detail_name="ガス代")
    gasudai_message = make_not_reisterd_message(gasudai, year, month,kazoku)
    if gasudai_message:
        messages.append(gasudai_message)

    # 未分類件数
    not_edited_kakeibo = check_category_detail(category_detail_name="未分類")
    not_registered_kakeibo_message = make_not_edited_kakeibo_count_message(not_edited_kakeibo, year, month,kazoku)
    if not_registered_kakeibo_message:
        messages.append(not_registered_kakeibo_message)
    
    return {"messages":messages}



def make_not_reisterd_message(category_detail, year=today.year, month=today.month,kazoku=None):
    ''''''
    message = dict()
    target_kakeibo = Kakeibo.objects.filter(category_detail=category_detail, date__year=year, date__month=month,kazoku=kazoku)
    logger.debug(target_kakeibo)
    if target_kakeibo.count() == 0:
        message["type"] = "warning"
        if category_detail:
            message["body"] = "今月は{}の登録がありません。".format(category_detail.name)
            message["link"] = "/cms/add/?date={0}{1}01&category={2}".format(year, month ,category_detail.id,kazoku=kazoku)
            logger.error("{0} message".format(message["body"]))
        return message
    else:
        logger.error("no MASSAGE")

        return None

def make_not_edited_kakeibo_count_message(category_detail, year=today.year, month=today.month,kazoku=None):
    ''''''

    message = dict()
    target_kakeibo = Kakeibo.objects.filter(category_detail=category_detail, date__year=year, date__month=month,kazoku=kazoku)
    logger.debug(target_kakeibo)
    if target_kakeibo.count() == 0:
        message["type"] = "info"
        message["body"] = "未登録ステータスの家計簿はありません。"
        message["link"] = "/cms/add/"
        logger.error("{0} message".format(message["body"]))
        return message
    else:
        message["type"] = "warning"
        message["body"] = "今月は未登録ステータスの家計簿は{}件あります。".format(target_kakeibo.count())
        message["link"] = "/cms/bulk_update/{0}/{1}".format(year, month)
        logger.error("{0} message".format(message["body"]))

        return message

