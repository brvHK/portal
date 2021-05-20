import calendar
import datetime

from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from cms.models import Post
from cms.models import Tag
from cms.models import SmallCategory
from cms.models import PostBigCategory

def newest_posts(request):
        context = {
            # 最新記事：新しい記事から10件取得する
            'newest_posts': Post.objects.filter(is_publish=True).order_by('created_at').reverse()[:10],
            'tags_all': Tag.objects.all(),
            'not_published_posts': Post.objects.filter(is_publish=False).order_by('created_at').reverse(),
            'small_categories': SmallCategory.objects.all(),
            'post_big_categories': PostBigCategory.objects.all(),
        }
        return context

def my_kazoku(request):
    context = {}
    kazoku_id = request.session['kazoku_in_session'] if request.session.has_key('kazoku_in_session') else 2
    kazoku = ""
    kazoku = Group.objects.get(id=kazoku_id)
    context ={
        "kazoku_in_session" : kazoku
    }
    return context

calendar.setfirstweekday(calendar.SUNDAY)

import calendar
from collections import deque


class BaseCalendarMixin:
    """カレンダー関連Mixinの、基底クラス"""
    first_weekday = 0  # 0は月曜から、1は火曜から。6なら日曜日からになります。お望みなら、継承したビューで指定してください。
    week_names = ['月', '火', '水', '木', '金', '土', '日']  # これは、月曜日から書くことを想定します。['Mon', 'Tue'...

    def setup_calendar(self):
        """内部カレンダーの設定処理

        calendar.Calendarクラスの機能を利用するため、インスタンス化します。
        Calendarクラスのmonthdatescalendarメソッドを利用していますが、デフォルトが月曜日からで、
        火曜日から表示したい(first_weekday=1)、といったケースに対応するためのセットアップ処理です。

        """
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        """first_weekday(最初に表示される曜日)にあわせて、week_namesをシフトする"""
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)  # リスト内の要素を右に1つずつ移動...なんてときは、dequeを使うと中々面白いです
        return week_names

class CustomHTMLCal(calendar.HTMLCalendar):
    cssclasses = [style + " text-nowrap" for style in
                  calendar.HTMLCalendar.cssclasses]
    cssclass_month_head = "text-center month-head"
    cssclass_month = "text-center month"
    cssclass_year = "text-italic lead"

def sidebar_calendar(request):
    context = {}
    now = datetime.datetime.now()
    cal = CustomHTMLCal()
    month_html_calendar = cal.formatmonth(now.year, now.month)
    # mark_safeでhtmlがエスケープされないようにする
    context['sidebar_calendar'] = mark_safe(month_html_calendar)
    
    return context