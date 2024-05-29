from django import forms
from ...models import RepeatedPayment, OneTimePayment, Category


# Form for creating and updating RepeatedPayment instances
class RepeatedPaymentForm(forms.ModelForm):
    class Meta:
        model = RepeatedPayment  # Model to be used for the form
        fields = ['budget_id', 'source', 'spent', 'category', 'date_received', 'frequency', 'next_payment_date']
        # Fields to include in the form

        exclude = ['user']  # Exclude the 'user' field from the form

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pop the 'user' keyword argument if present
        super(RepeatedPaymentForm, self).__init__(*args, **kwargs)
        if user:
            # Filter the 'category' field's queryset to include only categories belonging to the user
            self.fields['category'].queryset = Category.objects.filter(category_user=user)
            # Add an option to create a new category
            self.fields['category'].choices += [('new', 'Create new category...')]


# Form for creating and updating OneTimePayment instances
class OneTimePaymentForm(forms.ModelForm):
    class Meta:
        model = OneTimePayment  # Model to be used for the form
        fields = '__all__'  # Include all fields from the model in the form
        exclude = ['user']  # Exclude the 'user' field from the form

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pop the 'user' keyword argument if present
        super(OneTimePaymentForm, self).__init__(*args, **kwargs)
        if user:
            # Filter the 'category' field's queryset to include only categories belonging to the user
            self.fields['category'].queryset = Category.objects.filter(category_user=user)


# Form for creating and updating Category instances
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category  # Model to be used for the form
        fields = '__all__'  # Include all fields from the model in the form
        exclude = ['user']  # Exclude the 'user' field from the form

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pop the 'user' keyword argument if present
        super(CategoryForm, self).__init__(*args, **kwargs)
        if user:
            # Filter the 'category' field's queryset to include only categories belonging to the user
            self.fields['category'].queryset = Category.objects.filter(category_user=user)
