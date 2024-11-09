from django.shortcuts import render, redirect
from .models import *
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from .import auth_views
from django.contrib import messages
import logging

# Create your views here.
# here we user user=request.user to get get the currently logged in access of the user
# so the filter(user=request.user) only retrives the blogs of the logged in users

# home view
@login_required(login_url='/userLogin')
def home(request):
    user = request.user
    blogs = Blog.objects.filter(user=user)
    
    context = {"blogs": blogs}
    return render(request, 'blog_routes/home.html', context)


# view for adding a blog
@login_required(login_url='/userLogin')
def addBlogs(request):
    user = request.user
    blogs = Blog.objects.filter(user=user)
    categories = Category.objects.filter(user=user)
    
    if request.method == 'POST':
        data = request.POST
        
        if data['category'] != "none":
            category = Category.objects.get(id=data['category'], user=request.user)
        elif data['new_category'] != "":
            category = Category.objects.get_or_create(name=data['new_category'], user=request.user)
        else:
            category = None        
            
        if isinstance(category, tuple):
            category = category[0]
            
        blogs = Blog.objects.create(
            user=user,
            title = data['title'],
            category = category,
            description = data['description']
        )            
        
        return redirect('home')
        
    context = {"blogs": blogs, 'categories': categories}
    return render(request, 'blog_routes/addBlogs.html', context)


# global blogs -> display all the users blogs around the world
@login_required(login_url='/userLogin')
def blogFeed(request):
    # in this conditio if request.user i.e if it is a current user its is logged in then exclude all his blogs from the blog field
    if request.user:
        blogs = Blog.objects.exclude(user=request.user)
    #else display all 
    else:
        blogs = Blog.objects.all()
    
    context = {'blogs': blogs}
    return render(request, 'blog_routes/blogFeed.html', context)


# view for viewing your own blog
@login_required(login_url='/userLogin')
def yourBlogs(request, pk):
    blogs = Blog.objects.get(id = pk)
    
    # this comments.filter filters all the comments in that specific blog where an user commented
    comments = Comment.objects.filter(blog=blogs)
    
    # comments = Comment.objects.all()-> this line is wrong because it displays comments in the each and every one of the blog
    
    context = {'blogs': blogs, 'comments': comments}
    return render(request, 'blog_routes/yourBlogs.html', context)

# view for editing a blog
@login_required(login_url='/userLogin')
def editBlogs(request, pk):
    blogs = Blog.objects.get(id=pk)
    
    # get the new edited blogs content from the form
    if request.method == 'POST':
        edited_title = request.POST.get('title', '')
        edited_description = request.POST.get('description', '')
        
        # editing the blog
        blogs.title = edited_title
        blogs.description = edited_description
        blogs.save()
        
        messages.success(request, 'Blog updated successfully!')
        return redirect('home')
    
    context = {"blogs": blogs}
    return render(request, 'blog_routes/editBlogs.html', context)

# view for deleting a blog
@login_required(login_url='/userLogin')
def deleteBlogs(request, pk):
    try:
        blog = Blog.objects.get(id=pk) #get the id from the delete button of specific blog
        blog.delete()
        
        category = blog.category 
        
        if not Blog.objects.filter(category=category).exists(): #checking if the category of the deleted blog still exists, if it does delete it
            category.delete()
        
        messages.success(request, 'Blog deleted successfully!')    
        
    except Blog.DoesNotExist:
        # log error and notify user
        messages.error(request, 'Blog does not exists or you dont have permission to delete it')
        
    except Exception as e:
        # logging unexpected error
        messages.error(request, 'An error occured while deleting the blog!')
        
    return redirect('home')


# comments views
def addComment(request, pk):
    # the blog id is for which comment is the blog is for 
    blog = Blog.objects.get(id=pk)
    
    if request.method == 'POST':
        comment_text = request.POST.get('comments', '') #get the comment text from the form
        
        # create a new comment
        if comment_text:
            Comment.objects.create(
                user=request.user,
                blog=blog,
                comment=comment_text
            ) 
            
            messages.success(request, 'comment has been added!')
            return redirect('yourBlogs', pk=pk)
    
    return redirect('yourBlogs', pk=pk)    

def deleteComment(request, pk):
    try:
        comment_text = Comment.objects.get(id=pk)
        blog_pk = comment_text.blog.id #get the blog id of that comment to be deleted
        comment_text.delete()
        
        messages.success(request, 'comment has been deleted')
        
    except Comment.DoesNotExist:
        messages.error(request, 'The comment, you are deleting does not exists')
        
    except Exception as e:
        messages.error(request, 'An unexpected error has been occured!')
           
    
    # here when we are redirecting to the yourBlog page when comment gets deleted we should provide it with a specific blog id of that post where we are deleting the comment
    # if we dont provide an specific id it throws a The NoReverseMatch error in Django typically occurs when a URL pattern requires an argument but doesn't receive it. 
    return redirect('yourBlogs', pk=blog_pk)