from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Setup, Category, Temp, User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from blogapp.forms import CreatePostForm, UserCreateForm, EditPostForm, NewsletterForm, ContatoForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail

# Create your views here.

# def ContatoView(request):
#     if request.method == 'POST':
#         form = ContatoForm(data=request.POST)
#         if form.is_valid():
#             contato = form.save()
#             contato.save()
#             return HttpResponseRedirect(reverse_lazy('blog:index'))
#     else:
#         form = ContatoForm()
#     return render(request, 'blogapp/contato.html', {'form': form} )


def index(request):
    if request.method == 'POST' and 'btn-contato' in request.POST:
        form_contato = ContatoForm(data=request.POST)
        if form_contato.is_valid():
            contato = form_contato.save()
            contato.save()
            print(contato.EmailContato)
            print(contato.MensagemContato)
            email_user = str(contato.EmailContato)
            message = contato.MensagemContato + 'this is coming from: ' + str(contato.EmailContato)
            list = 'ccfitgym@gmail.com'
            send_mail('Teste', message, contato.EmailContato, [list], fail_silently=False)
            return HttpResponseRedirect(reverse_lazy('blog:index'))
    else:
        form_contato = ContatoForm()

    if request.method=='POST' and 'btn-newsletter' in request.POST:
        form = NewsletterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return HttpResponseRedirect(reverse_lazy('blog:index'))
    else:
        form = NewsletterForm()
    dict = {'data' : None}
    try:
        limit = Setup.objects.get(SetupKey='blog')
        Posts = Post.objects.all().order_by('-date_creation')[:limit.NumberPostsHome]
        dict = {'data' : Posts}
    except:
        print("No result for thhis query")
    return render(request, 'blogapp/index.html', {'form': form, 'data' : Posts, 'form_contato': form_contato})

#####################################################################################################################################

def Signup(request):
    print('got here')
    print(request.method)
    if request.method=='POST':
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, user)
            user_info = User.objects.get(email=form.cleaned_data['email'])
            request.session['user'] = user_info.first_name
            return HttpResponseRedirect(reverse_lazy('blog:management'))
    else:
        form = UserCreateForm()
    context = {'form': form}
    return render(request, 'blogapp/signup.html', context)

#####################################################################################################################################

@login_required
def Management(request):
    # if request.method == 'GET': # If the form is submitted
    #     search_query = request.GET.get('search_box', None)
    #     print('here inside')
    #     print(search_query)
        # Do whatever you need with the word the user looked for
    categories = Category.get_all_categories()
    # print(request.user)
    # posts = Post.get_all_posts()
    categoryID = request.GET.get('category')
    search_query = request.GET.get('search_box', None)
    message = ''
    if categoryID:
        print(categoryID)
        print('just sees here')
        search = Category.objects.get(pk=categoryID)
        search_found = search.name
        print(search_found)
        posts = Post.objects.filter(categories__contains=search_found)
        if not posts:
            print('anything')
            # posts = Post.get_all_posts().order_by('-date_creation');
            # return message for this
            message = 'Nothing found for ' + search_found
        print(search_query)
    elif search_query:
        # posts = Post.get_all_posts_by_categoryid(categoryID)
        posts = Post.objects.filter(title__contains=search_query)
        if not posts:
            print('anything')
            posts = Post.get_all_posts().order_by('-date_creation');
            # return message for this
            message = 'Nothing found for ' + search_query
        print(posts)
        print('search')
    else:
        posts = Post.get_all_posts().order_by('-date_creation');
        print('postsssssssssss', posts)
        print(type(posts))
    data = {}
    data['categories'] = categories
    data['posts'] = posts
    if message != '':
        data['message'] = message
    return render(request, 'blogapp/management.html', data)

#####################################################################################################################################


def LoginView(request):
    request.session['confirm_message'] = ''
    print('GOT HERE IN THE LOGINVIEW')
    if request.method == 'POST':
        print(request.POST.get('email'))
        print(request.POST.get('password'))
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Authenticating the user
        user = authenticate(request, email=email, password=password)
        user_info = User.objects.get(email=email)
        request.session['user'] = user_info.first_name
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('blog:management'))
        else:
            return HttpResponseRedirect(reverse_lazy('blog:management'))
    context = {}
    return render(request, 'blogapp/login.html', context)

#####################################################################################################################################



def Newsletter(request):
    cat = request.GET.get('newsletter')
    print('here')
    print(cat)
    if cat:
        print(cat)
        p = Newsletter(email=cat, status='ACTIVE')
        p.save(force_insert=True)
    return HttpResponseRedirect(reverse_lazy('blog:index'))

#####################################################################################################################################

# class CreatePost(LoginRequiredMixin, CreateView):
#     model = Post
#     form_class = CreatePostForm
#     template_name = "blogapp/create_post.html"
#     success_url = reverse_lazy( "blog:management" )

#####################################################################################################################################

def Redirects(request, pk):
    print('building it')
    # posts = get_object_or_404(Post, pk=pk)
    # form = EditPostForm(request.POST or None, instance = posts)
    # # Deleting everything in the table
    # all = Temp.objects.all().first()
    # if all:
    #     all.delete()
    # # filling temp table
    # first = Post.objects.get(pk=pk)
    # p = Temp(categories=first.categories)
    # p.save(force_insert=True)
    # categor = ''
    # print('ve se chega aqui pelo menos')
    # first = Temp.objects.all().first()
    # print(pk)
    # print(first)
    # if first.categories:
    #     categor = first.categories.split(',')
    #     print(categor, 'chunks')
    # if form.is_valid():
    #     form.save()
    #     return HttpResponseRedirect(reverse_lazy('blog:management'))
    # # context = {'form': form}
    # # return render(request, 'blogapp/edit_post.html', context)
    return render(request, 'blogapp/edit_post.html', {'form': form, 'data':categor})

#####################################################################################################################################

def DeleteAllCategories(request):
    print('got hereeeeeee delete all')
    temp_categories = Temp.objects.all().first()
    temp_categories.delete()
    return HttpResponseRedirect(reverse_lazy('blog:management'))

#####################################################################################################################################

def ChangeTag(request, pk):
    request.session['pk'] = pk
    cat = False
    if request.method=='GET':
        cat = request.GET.get('change')
    if cat:
        find = Post.objects.get(pk=pk)
        print(find, 'THIS IS THE ONE')
        if find:
            if find.categories == '':
                new = cat
                find.categories = new
                find.save()
                print(cat, 'cat')
                print(new, 'new')
                print('none')
            else:
                new = cat + ',' + str(find.categories)
                print(new, 'inseriu')
                find.categories = new
                find.save()
                print('first')
        else:
            find = Post(categories=cat)
            find.save(force_insert=True)
            print('second')
    # second session
    posts = get_object_or_404(Post, pk=pk)
    if posts.categories:
        chunks = posts.categories.split(',')
        print(chunks, 'chunks')
        categor = chunks
    else:
        categor= ''
    return render(request, 'blogapp/change_tag.html', {'data':categor})

#####################################################################################################################################

def CreatePost(request):
    print("return this")
    cat = False
    # set = CreatePostForm()
    if request.method=='GET':
        cat = request.GET.get('add')
    if cat:
        # set = CreatePostForm(data=request.GET)
        print(set)
        print('see whts in here')
        find = Temp.objects.all().exists()
        print(find, 'THIS IS THE ONE')
        if find:
            first = Temp.objects.all().first()
            new = cat + ',' + first.categories
            print(str, 'inseriu')
            p = Temp.objects.get(categories=first.categories)
            p.categories = new
            p.save()
        else:
            p = Temp(categories=cat)
            p.save(force_insert=True)
    first = Temp.objects.all().first()
    if first:
        chunks = first.categories.split(',')
        print(chunks, 'chunks')
        categor = chunks
    else:
        categor= ''
    # data = categor
    # three = set
    print(request.method)
    if request.method=='POST':
        print('got here')
        form = CreatePostForm(data=request.POST)
        if form.is_valid():
            post = form.save()
            username = User.objects.get(email=request.user)
            post.author = str(request.user)
            post.name = username.first_name
            temp_categories = Temp.objects.all().first()
            if temp_categories:
                # insert to category table here
                categor_unit = temp_categories.categories.split(',')
                for category in categor_unit:
                    p = Category(name=category, description=category)
                    p.save(force_insert=True)
                print(categor_unit)
                print(type(categor_unit))
                print('=-=-=-=-=-=-=-=-=-=-=------------------------------==============================================')
                print(temp_categories.categories)
                post.categories = temp_categories.categories
                temp_categories.delete()
            post.save()
            # Send email
            # all_users = Newsletter.objects.filter(status='ok')
            # print(all_users)
            # if all_users.exists():
            #     for user in all_users:
            #         print(user, 'each of')
            #         email_user = str(user.email)
            #         message = 'NOVO POST GALERA'
            #         send_mail('Teste', message, 'ccfitgym@gmail.com', [email_user], fail_silently=False)
            return HttpResponseRedirect(reverse_lazy('blog:management'))
    else:
        form = CreatePostForm()
        # form = three
    # context = {'data': data}
    print('oficial', form)
    return render(request, 'blogapp/create_post.html', {'form': form, 'data':categor})

#####################################################################################################################################

def EditPost(request, pk):
    posts = get_object_or_404(Post, pk=pk)
    form = EditPostForm(request.POST or None, instance = posts)
    # Deleting everything in the table
    all = Temp.objects.all().first()
    if all:
        all.delete()
    # filling temp table
    first = Post.objects.get(pk=pk)
    p = Temp(categories=first.categories)
    p.save(force_insert=True)
    categor = ''
    print('ve se chega aqui pelo menos')
    first = Temp.objects.all().first()
    print(pk)
    print(first)
    if first.categories:
        categor = first.categories.split(',')
        print(categor, 'chunks')
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse_lazy('blog:management'))
    # context = {'form': form}
    # return render(request, 'blogapp/edit_post.html', context)
    return render(request, 'blogapp/edit_post.html', {'form': form, 'data':categor})

#####################################################################################################################################

def DeletePost(request, pk):
    posts = get_object_or_404(Post, pk=pk)
    print(posts)
    print(request.method)
    search = Post.objects.get(pk=pk)
    list_tags = search.categories.split(',')
    for list in list_tags:
        print(list)
        Category.objects.filter(name=list).delete()
    if request.method == 'GET':
        posts.delete()
    return HttpResponseRedirect(reverse_lazy('blog:management'))

#####################################################################################################################################


def DeleteCategory(request, value):
    print('test here')
    first = Temp.objects.all().first()
    string_set = first.categories.split(',')
    new_set = []
    for a_string in string_set:
        if value != a_string:
            new_set.append(a_string)
    print(new_set, 'new set')
    novo = ''
    print(new_set)
    for n in new_set:
        if new_set.index(n) == len(new_set)-1:
            novo = novo + n
        else:
            novo = n + ',' + novo
        print(novo, 'lets seeee the result')
    f = Temp.objects.all().first()
    p = Temp.objects.get(categories=f.categories)
    p.categories = novo
    p.save()
    blank = Temp.objects.all().first()
    if blank.categories == '':
        blank.delete()
    return HttpResponseRedirect(reverse_lazy('blog:create_post'))

#####################################################################################################################################

def DeleteCategoryEdit(request, value):
    print('check ifs gotten here')
    print('and did something')
    pk_number = int(request.session['pk'])
    posts = Post.objects.get(pk=pk_number)
    string_set = posts.categories.split(',')
    new_set = []
    for a_string in string_set:
        if value != a_string:
            new_set.append(a_string)
    print(new_set, 'new set')
    novo = ''
    print(new_set)
    for n in new_set:
        if new_set.index(n) == len(new_set)-1:
            novo = novo + n
        else:
            novo = n + ',' + novo
        print(novo, 'lets seeee the result')
    # updating post
    posts.categories = novo
    posts.save()
    response = HttpResponseRedirect(reverse_lazy('blogapp:change_tag', kwargs={'pk': pk_number}))
    return response



#####################################################################################################################################

# def AddCategory(request):
#     show = request.GET.get('add')
#     print(show)
#     return HttpResponseRedirect(reverse_lazy('blog:management'))

#####################################################################################################################################
# def Filter(request):
#     categories = Category.objects.all()
#     for unit in categories:
#         email = self.request.GET.get(unit.title)
#         print(email)
#     dict = {'data' : categories}
#     return render(request, 'blogapp/management.html', dict)


# class Management(ListView):
#     template_name = "blogapp/management.html"
#     model = Post
#     context_object_name = "posts"
