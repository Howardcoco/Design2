from django.http import request
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

# from django.contrib import messages


# from .models import UserProfile

# from .forms import ProfileForm


@login_required
def profile(request):
    user = request.user
    #go to the home page
    return render(request, 'users/profile2.html')
#    return render(request, 'login.html')

#if request.user.is_authenticated():
#    ...
#else:
#   return render(request, 'login.html')

#from utils import LoginRequiredMixin
#class CourseCommentView(LoginRequiredMixin, View):
#    """
#    课程评论
#    """
#    def get(self, request):
#        pass
