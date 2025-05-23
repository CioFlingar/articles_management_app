from typing import Any


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from app_dj.models import Articles

# from django.shortcuts import  redirect, render
# from .forms import CreateArticleForm

# def home(request):
#     articles = Articles.objects.all()
#     return render(request, "app_dj/home.html", {"articles": articles})


# def create_article(request):  # type:ignore
#     if request.method == "POST":
#         form = CreateArticleForm(request.POST)
#         if form.is_valid():
#             form_data = form.cleaned_data
#             new_article = Articles(
#                 title=form_data["title"],
#                 status=form_data["status"],
#                 content=form_data["content"],
#                 word_count=form_data["word_count"],
#                 twitter_post=form_data["twitter_post"],
#             )
#             new_article.save()

#             return redirect("home")
#     else:
#         form = CreateArticleForm()
#         return render(request, "app_dj/article_create.html", {"form": form})


class ArticleListView(LoginRequiredMixin, ListView):
    template_name = "app_dj/home.html"
    model = Articles
    context_object_name = "articles"
    paginate_by = 4

    def get_queryset(self) -> QuerySet[Any]:
        search = self.request.GET.get("search")
        queryset = super().get_queryset().filter(creator=self.request.user)
        if search:
            queryset = queryset.filter(title__search=search)
        return queryset.order_by("-created_at")


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = "app_dj/article_create.html"
    model = Articles
    fields = ["title", "status", "content", "twitter_post"]
    success_url = reverse_lazy("home")
    context_object_name = "article"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class AritcleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "app_dj/article_update.html"
    model = Articles
    fields = ["title", "status", "content", "twitter_post"]
    success_url = reverse_lazy("home")
    context_object_name = "article"

    def test_func(self) -> bool | None:
        return self.request.user == self.get_object().creator


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "app_dj/article_delete.html"
    model = Articles
    success_url = reverse_lazy("home")
    context_object_name = "article"

    def test_func(self) -> bool | None:
        return self.request.user == self.get_object().creator

    def post(self, request, *args, **kwargs):
        messages.success(request, "Article deleted successfully.", extra_tags="destructive")
        return super().post(request, *args, **kwargs)
