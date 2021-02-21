import datetime
from user.actions import export_as_csv_action

from django.contrib import admin

from user.models import CustomUser
from .models import Post, Vote, Comments


import csv
import datetime
from django.http import HttpResponse

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = 'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not\
              field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'



class PostAdmin(admin.ModelAdmin):
    model = Post
    actions = [export_to_csv]

    # export_to_csv.short_description = 'Export to CSV'


admin.site.register(Post, PostAdmin)
admin.site.register(Vote)
admin.site.register(Comments)

