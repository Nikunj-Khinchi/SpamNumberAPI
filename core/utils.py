from .models import SpamReport

def calculate_spam_likelihood(phone_number):
    spam_count = SpamReport.objects.filter(phone_number=phone_number).count()
    return spam_count  # Simplistic spam likelihood, you can enhance this.
