from django import forms
from django.conf import settings


class ReputationForm(forms.Form):
    """
    A form for submitting a reputation rating (positive or negative).

    Fields:
        badge: Must be one of the allowed positive or negative badges.
        is_negative: Hidden field to indicate the nature of the reputation.
            - True → negative reputation (e.g., report)
            - False → positive reputation (e.g., thanks, trust)

    Behavior:
        - Validates that the selected badge exists in settings:
            - settings.REPUTATION_BADGES_POSITIVE if not is_negative
            - settings.REPUTATION_BADGES_NEGATIVE if is_negative
    """

    badge = forms.CharField(max_length=100)
    is_negative = forms.BooleanField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, is_negative=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_negative = is_negative
        self.fields['is_negative'].initial = is_negative

    def clean_badge(self):
        badge = self.cleaned_data['badge']
        if self.is_negative:
            valid_badges = getattr(settings, 'REPUTATION_BADGES_NEGATIVE', [])
        else:
            valid_badges = getattr(settings, 'REPUTATION_BADGES_POSITIVE', [])

        if badge not in valid_badges:
            raise forms.ValidationError("Invalid badge selected.")
        return badge
