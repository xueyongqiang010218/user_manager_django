from django.core.paginator import Paginator
from django.conf import settings

#接受两个参数
#request
#blogs_all_list所有的博客，Blog.objects.all()
def page_paginator(request,blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    # per_page: 每页显示条目数量
    # count:    数据总个数
    # num_pages:总页数
    # page_range:总页数的索引范围，如: (1,10),(1,200)
    # page:     page对象
    page_num = request.GET.get('p', 1)  # 获取url的页面参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    # has_next              是否有下一页
    # next_page_number      下一页页码
    # has_previous          是否有上一页
    # previous_page_number  上一页页码
    # object_list           分页之后的数据列表
    # number                当前页
    # paginator             paginator对象
    currentr_page_num = page_of_blogs.number  # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    # 返回当前页的博客，和[首页,前2页,.....当前页，....，后两页，尾页]
    return page_of_blogs,page_range