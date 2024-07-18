from django.shortcuts import redirect
from django.views import View


class LandingPageView(View):
    def get(self, request):
        return redirect('tasks:task_list')