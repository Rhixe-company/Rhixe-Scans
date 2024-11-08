import django_tables2 as tables
from django.contrib.auth import get_user_model
from django.utils.html import escape, format_html
from django_tables2.utils import AttributeDict
from django.utils.safestring import mark_safe

User = get_user_model()


class MaterializeCssCheckboxColumn(tables.CheckBoxColumn):
    def render(self, value, bound_column, record):
        default = {"type": "checkbox", "name": bound_column.name, "value": value}
        if self.is_checked(value, record):
            default.update({"checked": "checked"})
        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")
        attrs = tables.utils.AttributeDict(default, **(specific or general or {}))
        return mark_safe(
            '<label class="flex cursor-pointer items-center text-neutral-600 dark:text-neutral-300"><div class="relative flex items-center"><input %s class="custom_checkbox_input":checked="checkAll" /><svg xmlns="http://www.w3.org/2000/svg"viewBox="0 0 24 24"aria-hidden="true"stroke="currentColor"fill="none"stroke-width="4"class="invisible pointer-events-none absolute left-1/2 top-1/2 size-3 -translate-x-1/2 -translate-y-1/2 text-neutral-100 peer-checked:visible dark:text-black"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" /></svg></div></label>'
            % attrs.as_html()
        )


class StatusColumn(tables.BooleanColumn):

    def render(self, value, record, bound_column):
        value = self._get_bool_value(record, value, bound_column)
        text = self.yesno[int(not value)]
        attrs = {"class": str(value).lower()}
        attrs.update(self.attrs.get("span", {}))

        return format_html(
            "<span {}>{}</span>", AttributeDict(attrs).as_html(), escape(text)
        )


class UserTable(tables.Table):

    check = MaterializeCssCheckboxColumn(orderable=False)
    activestatus = StatusColumn(accessor="is_active", orderable=False)
    superstatus = StatusColumn(accessor="is_superuser", orderable=False)

    user = tables.TemplateColumn(
        template_name="partials/user/user.html", orderable=False
    )
    actions = tables.TemplateColumn(
        template_name="partials/user/actions.html", orderable=False
    )

    class Meta:
        model = User

        sequence = (
            "check",
            "user",
            "id",
            "date_joined",
            "activestatus",
            "superstatus",
        )
        fields = (
            "check",
            "user",
            "id",
            "date_joined",
            "activestatus",
            "superstatus",
        )
        attrs = {
            "th": {
                "_ordering": {
                    "orderable": "sortable",  # Instead of `orderable`
                    "ascending": "ascend",  # Instead of `asc`
                    "descending": "descend",  # Instead of `desc`
                }
            },
        }
        row_attrs = {"data-id": lambda record: record.pk}
