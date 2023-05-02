import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from . import models as hospital_models


class AdminTable(tables.Table):
    # cnic = tables.Column(empty_values=())
    action = tables.Column(empty_values=(), verbose_name="Action")
    first_name = tables.Column(empty_values=())
    last_name = tables.Column(empty_values=())
    email = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = hospital_models.UserProfile
        fields = ('first_name', 'last_name', 'email', 'cnic', 'role')

    def render_first_name(self, record):
        return record.user.first_name

    def render_last_name(self, record):
        return record.user.last_name

    def render_email(self, record):
        return record.user.email

    def render_action(self, record):
        return format_html("""
            <a href = "{}" class='btn btn-sm bg-dark' text-white><i  class = "fa fa-trash" style="color:white"></i> </a>
            <a href = "{}" class='btn btn-sm bg-dark text-white'><i  class = "fas fa-edit" style="color:white"></i></a>
        """, reverse('delete-admin', kwargs={"pk": record.user.pk}),
                           reverse('edit-admin', kwargs={"pk": record.user.pk}))

    # def render_cnic(self, record):
    #     try:
    #         idno = record.userprofile.cnic
    #         return idno
    #     except (hospital_models.UserProfile.DoesNotExist, AttributeError):
    #         return ''


class PatientTable(tables.Table):
    action = tables.Column(empty_values=(), verbose_name="Action")
    first_name = tables.Column(empty_values=())
    last_name = tables.Column(empty_values=())
    email = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = hospital_models.UserProfile
        fields = ('first_name', 'last_name', 'email', 'cnic', 'role')

    def render_first_name(self, record):
        return record.user.first_name

    def render_last_name(self, record):
        return record.user.last_name

    def render_email(self, record):
        return record.user.email

    def render_action(self, record):
        return format_html("""
            <a href = "{}" class='btn btn-sm bg-dark' text-white><i  class = "fa fa-trash" style="color:white"></i> </a>
            <a href = "{}" class='btn btn-sm bg-dark text-white'><i  class = "fas fa-edit" style="color:white"></i></a>
        """, reverse('delete-patient', kwargs={"pk": record.user.pk}),
                           reverse('edit-patient', kwargs={"pk": record.user.pk}))


class DoctorTable(tables.Table):
    action = tables.Column(empty_values=(), verbose_name="Action")
    first_name = tables.Column(empty_values=())
    last_name = tables.Column(empty_values=())
    email = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = hospital_models.UserProfile
        fields = ('first_name', 'last_name', 'email', 'cnic', 'role')

    def render_first_name(self, record):
        return record.user.first_name

    def render_last_name(self, record):
        return record.user.last_name

    def render_email(self, record):
        return record.user.email

    def render_action(self, record):
        return format_html("""
            <a href = "{}" class='btn btn-sm bg-dark' text-white><i  class = "fa fa-trash" style="color:white"></i> </a>
            <a href = "{}" class='btn btn-sm bg-dark text-white'><i  class = "fas fa-edit" style="color:white"></i></a>
        """, reverse('delete-doctor', kwargs={"pk": record.user.pk}),
                           reverse('edit-doctor', kwargs={"pk": record.user.pk}))


class AvailibilityTable(tables.Table):
    action = tables.Column(empty_values=(), verbose_name="Action")

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = hospital_models.DoctorsAvailibility
        fields = ('doctor', 'days', 'starting_time', 'ending_time', 'active')

    def render_action(self, record):
        return format_html("""
            <a href = "{}" class='btn btn-sm bg-dark' text-white><i  class = "fa fa-trash" style="color:white"></i> </a>
            <a href = "{}" class='btn btn-sm bg-dark text-white'><i  class = "fas fa-edit" style="color:white"></i></a>
        """, reverse('delete-availibility', kwargs={"pk": record.pk}),
                           reverse('edit-availibility', kwargs={"pk": record.pk}))


class SlotTable(tables.Table):
    action = tables.Column(empty_values=(), verbose_name="Action")

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = hospital_models.Slots
        fields = ('doctor', 'slot_date', 'slot_start_time', 'slot_end_time', 'is_available')

    def render_action(self, record):
        return format_html("""
            <a href = "{}" class='btn btn-sm bg-dark' text-white><i  class = "fa fa-trash" style="color:white"></i> </a>
            <a href = "{}" class='btn btn-sm bg-dark text-white'><i  class = "fas fa-edit" style="color:white"></i></a>
        """, reverse('delete-slot', kwargs={"pk": record.pk}),
                           reverse('edit-slot', kwargs={"pk": record.pk}))
