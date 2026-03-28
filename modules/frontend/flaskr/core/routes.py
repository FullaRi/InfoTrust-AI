from flask import render_template, flash, redirect, request, url_for, abort
from flaskr.core import bp
from setup import settings
from . import forms
from utils import mailer


@bp.route('/')
def home():
    return render_template('index.html')


@bp.route('/report')
def report():
    return render_template('report.html')


@bp.route('/product')
def product():
    return render_template('product.html')


@bp.route('/contact-request', methods=['POST'])
def contact_request():
    form = forms.ContactForm(request.form)

    if form.validate():
        flash('Thanks for registering')

        mailer.send_contact_request_mail(form)

        return redirect(url_for('core.notif', category='contact'))

    print(form.errors)

    flash('Erreur ! Veuillez remplir correctement tous les champs.', 'error')

    return redirect(url_for('core.contact'))
