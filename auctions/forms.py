from django.forms import ModelForm

from .models import Listing

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "category", "starting_bid", "image_url"]
        labels = {
            "title": "Product Name",
            "description": "Detailed Description",
            "category": "Category",
            "starting_bid": "Starting Price (USD)",
            "image_url": "Image URL",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-kyore'
