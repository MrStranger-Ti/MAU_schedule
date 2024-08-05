from django.forms import Form, ModelForm


def add_error_class(form: Form | ModelForm, all_fields: bool = False) -> None:
    if all_fields:
        for field in form.fields.values():
            field_class = field.widget.attrs.get('class')
            if field_class:
                field.widget.attrs['class'] += ' error-input'
            else:
                field.widget.attrs['class'] = 'error-input'
    else:
        for field_name in form.errors:
            field_obj = form.fields.get(field_name)
            field_class = field_obj.widget.attrs.get('class')
            if field_class:
                field_obj.widget.attrs['class'] += ' error-input'
            else:
                field_obj.widget.attrs['class'] = 'error-input'
