import requests
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .forms import FormEntryForm

def form_view(request):
    if request.method == 'POST':
        form = FormEntryForm(request.POST)
        if form.is_valid():
            form_entry = form.save(commit=False)

            # Calculate start date and expiration date
            start_date = form_entry.start_date
            expiration_days = form_entry.expiration_days
            expiration_date = start_date + timedelta(days=expiration_days)

            # Send welcome email to the user
            subject = 'SWEBS POF DISBURSED SUCCESSFULLY'
            from_email = 'info@swebslimited.com'
            to_email = form_entry.email

            # Create EmailMultiAlternatives object
            email = EmailMultiAlternatives(subject, '', from_email, [to_email])

            # Attach HTML message
            html_message = f"""
             <img src="https://swebslimited.com/assets/img/logoo.jpg" alt="Logo">
                <p>Hello {form_entry.name},</p>
                <p>Thank you for using Swebs Limited. Your POF has been disbursed.</p>
                <p>Please note that the funds will be in your account for {form_entry.expiration_days} days.</p>
                <h3>POF DETAILS</h3>
                <p>Amount: {form_entry.amount}</p>
                <p>Start Date: {start_date}</p>
                <p>Stop Date: {expiration_date}</p>
                <p>If you have any questions, please send us an email at ugochi@swebslimited.com or call 09039525017 or 09017394719</p>
             
            """
            email.attach_alternative(html_message, "text/html")

            # Send email
            email.send()

            # Calculate reminder dates
            reminder_dates = [
                expiration_date - timedelta(days=3),
                expiration_date - timedelta(days=2),
                expiration_date - timedelta(days=1),
                expiration_date - timedelta(days=0),
            ]

            # Send reminder emails
            for reminder_date in reminder_dates:
                reminder_subject = 'SWEBS POF REMINDER'
                reminder_message = f"""
                     <img src="https://swebslimited.com/assets/img/logoo.jpg" alt="Logo">
                    <p>Hello {form_entry.name},</p>
                    <p>This is a reminder that your POF will be due on {expiration_date}.</p>
                    <p>Kindly go to the bank and print your bank statement before the expiry date.</p>
                    <h3>POF DETAILS</h3>
                    <p>Amount: {form_entry.amount}</p>
                    <p>Start Date: {start_date}</p>
                    <p>Stop Date: {expiration_date}</p>
                    <p>You also have the option to extend the loan. If you wish to extend, kindly contact us before the expiry date.</p>
                    <p>Note: If you have paid for an extension, kindly disregard this email as it is automated.</p>
                    
                    <p>If you have any questions, please send us an email at ugochi@swebslimited.com or call 09039525017 or 09017394719</p>
                 
                """

                # Create EmailMultiAlternatives object for reminder email
                reminder_email = EmailMultiAlternatives(reminder_subject, '', from_email, [to_email])
                reminder_email.attach_alternative(reminder_message, "text/html")

                # Send reminder email
                reminder_email.send()

            form_entry.save()
            return render(request, 'success.html')  # Render a success template

    else:
        form = FormEntryForm()

    return render(request, 'form.html', {'form': form})  # Render the form template
