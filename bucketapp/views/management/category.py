from django.shortcuts import render, redirect  # Import functions to render templates and handle redirects
from django.contrib.auth.mixins import LoginRequiredMixin  # Import mixin to ensure user is logged in
from django.views.generic import View  # Import generic class-based view
from ...models import Category  # Import the Category model from the current app's models
from django.http import HttpResponseForbidden  # Import HttpResponseForbidden to handle forbidden responses


class CategoryView(View, LoginRequiredMixin):
    # This class inherits from Django's generic View and
    # LoginRequiredMixin to ensure only logged-in users can access it.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = 'bucketapp/category.html'  # Define the template to be used for rendering

        # Function mapping dictionary to map form actions to methods
        self.function_mapping = {
            "save": self.save_category,
            "add_new": self.add_new_category,
            "delete": self.delete_category,
        }

    def save_category(self, request):
        '''
        Save an existing category
        '''
        print("saved")
        # Retrieve the category record to be updated based on the primary key from POST data
        record = Category.objects.get(category_id=request.POST['id'])
        # Update the category name and budgeted fields from POST data
        record.category_name = request.POST['name']
        record.budgeted = request.POST['budgeted']
        # Save the updated record to the database
        record.save()

    def add_new_category(self, request):
        '''
        Add a new category
        '''
        # Create a new category with the current user, default name 'empty', and default privacy as True
        new_category = Category(category_user=request.user, category_name='empty', category_privacy=True)
        # Save the new category to the database
        new_category.save()

    def delete_category(self, request):
        '''
        Delete an existing category
        '''
        print("deleted")
        # Retrieve the category record to be deleted based on the primary key from POST data
        record = Category.objects.get(category_id=request.POST['id'])
        # Delete the record from the database
        record.delete()

    def get(self, request):
        '''
        Handle GET requests
        '''
        # Retrieve all category records for the current user
        category_records = Category.objects.filter(category_user=request.user)
        # Render the template with the retrieved category records
        return render(request, self.template_name, {
            'category_records': category_records,
        })

    def post(self, request):
        '''
        Handle POST requests
        '''
        print(request.POST)
        # Call the appropriate method based on the submit value in the POST data
        self.function_mapping[request.POST['submit']](request)
        # Redirect to the summary view after handling the POST request
        return redirect('summary')
