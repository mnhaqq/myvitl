from django.forms.widgets import FileInput

class CustomImageWidget(FileInput):
    template_name = 'accounts/custom_image_widget.html'
    
    