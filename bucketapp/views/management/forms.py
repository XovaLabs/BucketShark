from django import forms
from ...models import RepeatedPayment, OneTimePayment, Category


class RepeatedPaymentForm(forms.ModelForm):
    class Meta:
        model = RepeatedPayment
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RepeatedPaymentForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(category_user=user)
            # Add an option to create a new category
            self.fields['category'].choices += [('new', 'Create new category...')]


class OneTimePaymentForm(forms.ModelForm):
    class Meta:
        model = OneTimePayment
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OneTimePaymentForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(category_user=user)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['user']

    def __init__(self,  *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(category_user=user)
