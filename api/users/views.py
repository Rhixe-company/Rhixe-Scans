from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from api.users.forms import UserForm, AdminUserUpdateForm, AdminUserCreateForm
from api.users.models import User
from api.users.tables import UserTable
from api.users.decorators import admin_only, user_only
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django_htmx.http import trigger_client_event
from render_block import render_block_to_string
from api.apps.filters import UserFilter
from django.conf import settings
from django_tables2 import RequestConfig


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"
    form_class = UserForm
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


@user_only
@admin_only
def userAdmin(request):
    users = User.objects.all()
    myFilter = UserFilter(request.GET, queryset=users)
    table = UserTable(myFilter.qs)
    RequestConfig(request, paginate={"per_page": settings.PAGINATE_BY}).configure(table)
    context = {
        "table": table,
        "filter": myFilter,
    }
    if request.htmx:
        return render(request, "partials/user/body.html", context)
    return render(request, "users/admin.html", context)


@user_only
@admin_only
def userAdminCreate(request):
    if request.method == "POST":
        userform = AdminUserCreateForm(request.POST, request.FILES)
        if userform.is_valid():
            user = userform.save()

            context = {
                "user": user,
            }
            html = render_block_to_string(
                "partials/user/createsuccess.html", "usercreate", context
            )
            response = HttpResponse(html)
            return trigger_client_event(response, "user_added")
        else:
            context = {"form": userform}
            html = render_block_to_string(
                "partials/user/create.html", "usercreate", context
            )
            response = HttpResponse(html)
            return response
    form = AdminUserCreateForm()
    context = {
        "form": form,
    }
    if request.htmx:
        html = render_block_to_string(
            "partials/user/create.html", "usercreate", context
        )
        response = HttpResponse(html)
        return response
    return render(request, "users/admincreate.html", context)


@user_only
@admin_only
def userAdminEdit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    form = AdminUserUpdateForm(instance=user)
    if request.method == "POST":
        form = AdminUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            newuser = form.save()
            form = AdminUserUpdateForm(instance=newuser)
            context = {
                "user": newuser,
            }
            html = render_block_to_string(
                "partials/user/updatesuccess.html", "useredit", context
            )
            response = HttpResponse(html)
            return response
        else:
            context = {"form": form, "item": user}
            html = render_block_to_string(
                "partials/user/update.html", "useredit", context
            )
            response = HttpResponse(html)
            return response

    context = {"form": form, "item": user}
    html = render_block_to_string("partials/user/update.html", "useredit", context)
    return HttpResponse(html)


@user_only
@admin_only
def userAdminDelete(request, user_id):
    if User.objects.filter(pk=user_id).exists():
        if request.method == "DELETE":
            user = get_object_or_404(User, pk=user_id)
            user.delete()
            response = HttpResponse("")
            return trigger_client_event(response, "user_added")
        user = get_object_or_404(User, pk=user_id)
        context = {"record": user}
        html = render_block_to_string(
            "partials/user/delete.html", "userdelete", context
        )
        return HttpResponse(html)
