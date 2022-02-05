# coding:utf-8

from django.urls import path
from kakeibo import views
from kakeibo.views import KakeiboList
from kakeibo.views import PopupShopCreateView
from kakeibo.views import PopupKakeiboDetailCreateView
from kakeibo.views import PopupCategoryDetailCreateView

app_name= 'kakeibo'

urlpatterns = [
    path('import', views.import_csv, name='import_csv'),   # 一覧
    path('import_csv_dcard', views.import_csv_dcard, name='import_csv_dcard'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),   # 一覧
    path('calendar/<int:year>/<int:month>', views.CalendarView.as_view(),
        name='calendar_month'),
    path('shelf_registration', views.kakeibos_registration,
        name='kakeibo_shelf_registration'),
    path('bulk_update/<int:year>/<int:month>', views.kakeibos_update,
        name='bulk_update'),
    path('<str:kakeibo_type>', views.KakeiboList.as_view(), name='list_month'),
    path('<str:kakeibo_type>/<int:year>/<int:month>', views.KakeiboList.as_view(), name='list_month'),
    # url('kakeibo/(\d{4})/(\d{2})', views.CalendarView.as_view(),
    #     name='kakeibo_list_month'),
    path('add/', views.kakeibo_edit, name='kakeibo_add'),  # 登録
    path('mod/<int:kakeibo_id>/', views.kakeibo_edit, name='kakeibo_mod'),  # 修正
    path('category/add/', views.category_edit, name='category_add'),  # 登録
    path('category/mod/<int:category_id>/', views.category_edit, name='category_mod'),  # 修正
    path('del/<int:kakeibo_id>/', views.kakeibo_del, name='kakeibo_del'),   # 削除
    path('analysis/', views.analysis, name='analysis'), # 分析
    path('analysis/<int:year>', views.analysis, name='analysis'), # 分析    
    path('popup/add/shop/', PopupShopCreateView.as_view(), name='popup_shop_create'),
    path('popup/add/detail/', PopupKakeiboDetailCreateView.as_view(), name="popup_detail_create"),
    path('popup/add/category_detail/', PopupCategoryDetailCreateView.as_view(), name="popup_category_detail_create"),
    path('', views.index, name='index'),
    path('<int:year>/', views.index, name='index_year'),
    path('<int:year>/<int:month>/', views.index, name='index_month'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('change_family/', views.change_family, name='change_family')
]
