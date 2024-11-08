from django.forms import CheckboxInput, FileInput
from django.utils.translation import gettext_lazy as _


FILE_INPUT_CONTRADICTION = object()


class MyImageField(FileInput):
    clear_checkbox_label = _("Clear")
    initial_text = _("Currently")
    input_text = _("Change")
    help_text = _("SVG, PNG, JPG or GIF (MAX. 800x400px).")
    template_name = "partials/widgets/clearable_file_input.html"
    checked = False

    def clear_checkbox_name(self, name):
        """
        Given the name of the file input, return the name of the clear checkbox
        input.
        """
        return name + "-clear"

    def clear_checkbox_id(self, name):
        """
        Given the name of the clear checkbox input, return the HTML id for it.
        """
        return name + "_id"

    def is_initial(self, value):
        """
        Return whether value is considered to be initial value.
        """
        return bool(value and getattr(value, "url", False))

    def format_value(self, value):
        """
        Return the file object if it has a defined url attribute.
        """
        if self.is_initial(value):
            return value

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        checkbox_name = self.clear_checkbox_name(name)
        checkbox_id = self.clear_checkbox_id(checkbox_name)
        context["widget"].update(
            {
                "aria-describedby": "file_input_help",
                "class": "custom_file_input",
                "checkbox_name": checkbox_name,
                "checkbox_id": checkbox_id,
                "is_initial": self.is_initial(value),
                "help_text": self.help_text,
                "input_text": self.input_text,
                "initial_text": self.initial_text,
                "clear_checkbox_label": self.clear_checkbox_label,
            }
        )
        context["widget"]["attrs"].setdefault("disabled", False)
        context["widget"]["attrs"]["checked"] = self.checked
        return context

    def value_from_datadict(self, data, files, name):
        upload = super().value_from_datadict(data, files, name)
        self.checked = self.clear_checkbox_name(name) in data
        if not self.is_required and CheckboxInput().value_from_datadict(
            data, files, self.clear_checkbox_name(name)
        ):
            if upload:
                # If the user contradicts themselves (uploads a new file AND
                # checks the "clear" checkbox), we return a unique marker
                # object that FileField will turn into a ValidationError.
                return FILE_INPUT_CONTRADICTION
            # False signals to clear any existing value, as opposed to just None
            return False
        return upload

    def value_omitted_from_data(self, data, files, name):
        return (
            super().value_omitted_from_data(data, files, name)
            and self.clear_checkbox_name(name) not in data
        )
