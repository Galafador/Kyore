from django import forms
from django.forms import ModelForm

from .models import Listing, Bid, Comment

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_url", "category"]
        labels = {
            "title": "Product Name",
            "description": "Detailed Description",
            "starting_bid": "Starting Price (USD)",
            "image_url": "Image URL (optional)",
        }
        widgets = {
            "description": forms.Textarea(attrs={
                "placeholder": "write a description for your product...",
            }),
            "image_url": forms.URLInput(attrs={
                "placeholder": "http://..."
            }),
            "category": forms.HiddenInput(attrs={
                "id": "selectedCategoryForm"
            })
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


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        widgets = {
                    "amount": forms.NumberInput(attrs={
                        "placeholder": "Enter your bid amount...",
                        "class":  "form-control form-control-kyore py-4"
                    }),
        }
    def add_is_invalid_class(self):
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                existing = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing} is-invalid".strip()

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
                    "comment": forms.Textarea(attrs={
                        "placeholder": "Add a comment...",
                        "class":  "form-control comment-textarea flex-grow-1",
                        "rows": 3

                    }),
        }
        def add_is_invalid_class(self):
            for field_name, field in self.fields.items():
                if self.errors.get(field_name):
                    existing = field.widget.attrs.get('class', '')
                    field.widget.attrs['class'] = f"{existing} is-invalid".strip()
