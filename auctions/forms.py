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
            "image_url": "Image URL (optional)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control form-control-kyore"

    def add_is_invalid_class(self):
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                existing = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing} is-invalid".strip()
