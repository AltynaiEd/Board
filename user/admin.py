from django.contrib import admin

from .actions import export_as_csv_action
from .models import CustomUser

import csv
import datetime
from django.http import HttpResponse

#
#
# def export_to_csv(modeladmin, request, queryset):
#     opts = modeladmin.model._meta
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment;' \
#                                       'filename={}.csv'.format(opts.verbose_name)
#     writer = csv.writer(response)
#     fields = [field for field in opts.get_fields() if not field.many_to_many \
#               and not field.one_to_many]
#     for obj in queryset:
#         data_row = []
#         for field in fields:
#             value = getattr(obj, field.name)
#             if isinstance(value, datetime.datetime):
#                 value = value.strftime('%d/%m/%Y')
#             data_row.append(value)
#         writer.writerow(data_row)
#     return response
#
class UserAdmin(admin.ModelAdmin):
    actions = [export_as_csv_action("CSV Export", fields=['field1', 'field2'])]

#     # export_to_csv.short_description = 'Export to CSV'

admin.site.register(CustomUser, UserAdmin)
