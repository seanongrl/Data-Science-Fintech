from app import app, admin, db
from app.models import News, Category
from flask_admin.contrib.sqla import ModelView
from flask import Markup


class NewsModelView(ModelView):

    def _image_formatter(view, context, News, image):
        if News.image:
            return Markup(
                '<br/><img src="%s" style="width:400px;height:110px">' % News.image)
        else:
            return ""

    def _desc_formatter(view, context, News, description):
        if News.description:
            return Markup("<h4>%s</h4>" % News.title) \
                   + Markup("<br/> <p>%s</p>" % News.description[:250]) \
                   + Markup("<a href='%s'>Read More</a>" % News.link) \
                   + Markup("<br/><br/> <p>%s, %s</p>" % (News.source, News.dt))
        else:
            return ""

    column_list = ['image', 'description', 'category']

    column_formatters = {
        'image': _image_formatter,
        'description': _desc_formatter
    }

    can_create = False
    can_edit = False
    can_delete = False
    page_size = 10
    column_searchable_list = ['title', 'description', 'source', 'dt']
    column_filters = ['title', 'description', 'source', 'dt', 'category']
    column_default_sort = ('dt', True)  # sort by dt desc


admin.add_view(NewsModelView(News, db.session))
