from django.shortcuts import render

# Create your views here.

def index(request):

    "学习笔记的主页"

    return render(request,'zkclientapp/template/index.html')

def get_html(request):
    return render(request, 'zkclientapp/template/get.html')

def get(request):
    context = {}
    # 通过request.GET['name']形式获取get表单内容
    # result为重定向到的result.html所使用的变量
    context['result'] = f"你搜索的内容为：{request.GET['q']}"
    return render(request, 'zkclientapp/template/result.html', context)

def post_html(request):
    # 不能和get一样使用render_to_response必须使用render进行重定向，不然服务端不会设置csrf_token
    # return render_to_response('post.html')
    return render(request, 'zkclientapp/template/post.html')

def post(request):
    context = {}
    # 通过request.GET['name']形式获取post表单内容
    # result为重定向到的result.html所使用的变量
    context['result'] = f"你搜索的内容为：{request.POST['q']}"
    return render(request, 'zkclientapp/template/result.html', context)
