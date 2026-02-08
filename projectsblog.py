from flask import Flask, render_template, flash, redirect, request, url_for
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from forms import ContactForm

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = '435d8c13a645888b823fb65642ac84bf'

posts = [
    {
        'title': '3D model',
        'content': 'Data science',
        'date_posted': 'April 20, 2025'
    }
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects/whian-whian')
def whian_whian_project():
    return render_template('projects/whian_whian.html')

@app.route('/projects/confluencer')
def confluencer_project():
    return render_template('projects/confluencer.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        sender_email = form.email.data
        message_body = form.message.data

        msg = MIMEMultipart()
        msg['From'] = sender_email # type: ignore
        msg['To'] = os.getenv('MAIL_USERNAME') # type: ignore
        msg['Subject'] = "New Contact Form Message"
        body = f"From: {sender_email}\n\nMessage:\n{message_body}"
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD')) # type: ignore
                server.sendmail(sender_email, os.getenv('MAIL_USERNAME'), msg.as_string()) # type: ignore
            flash("Message sent! I'll get back to you soon.", 'success')
        except Exception as e:
            print(f"Email error: {e}")
            flash("Sorry, something went wrong. Please try again later.", 'danger')

    return render_template('contact.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)