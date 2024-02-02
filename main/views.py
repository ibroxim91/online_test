from django.shortcuts import get_object_or_404, render ,redirect
from django.urls import reverse
from django.views import View
from .models import Category,Result,History,Question, Variant
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        data = {"categories": categories}
        return render(request,"home.html" , data)

class TestView(LoginRequiredMixin, View):

    def page_control(self,request,id):
        history_id = request.GET.get("question")
        history = get_object_or_404(History , id=int(history_id))
        result = history.result
        if result.end == False and result.user == request.user:
            if history.is_marked == False:
                data = {"history": history ,  "category":result.category, "test_status":result, "all_questions":result.history.all() }
                return render(request,"test.html" , data)
        return redirect(f"/test/{self.category_id}")
    

    def get(self, request, id):
        user = request.user
        self.category_id = id
        category = get_object_or_404(Category,id=id)
       
        page_number = request.GET.get("question")
        if page_number:
            return self.page_control(request,id)
        

        if Result.objects.filter(user=user, category=category,end=False).exists():
            result = Result.objects.get(user=user, category=category,end=False)
            history = result.history.filter(is_marked=False).order_by('number')

        else:
            result = Result.objects.create(user=user, category=category)
            questions = Question.objects.filter(category=category).order_by("?")[:15]
            n = 1
            history = []
            for q in questions:
                h = History.objects.create( result=result, question=q, number=n)
                n += 1
                history.append(h)
            
        data = {"history": history[0] ,  "category":category, "test_status":result, "all_questions":result.history.all() }
        return render(request,"test.html" , data)




class TestSaveView(LoginRequiredMixin, View):
    def post(self, request):
        history_id = request.POST.get('history_id')
        user_answer = request.POST.get('user_answer')
        history = get_object_or_404(History , id=int(history_id))
        variant = get_object_or_404(Variant , id=int(user_answer))                                                                                               

        result = history.result
        if  history.is_marked == False:
            history.user_variant = variant                                                                                                                                                          
            history.is_marked = True
            history.save()
            if variant.is_true:
                history.result.score += 1
                history.result.success += 1
            else:    
                history.result.fail += 1
            history.result.save()
        if result.history.filter(is_marked=False).count() == 0:
           result.end = True
           result.end_date = datetime.datetime.now()
           result.save()
           return render(request, "results.html", {"result":result})

        category_id = history.result.category.id

        return redirect(  reverse("test" , args = (category_id ,) )  )


