import mongoengine as mongo
from django.utils.text import slugify


# mongo documents
class Category(mongo.Document):

    category_name = mongo.StringField(required=True)
    slug = mongo.StringField(unique=True)

    meta = {'collection': 'Categories'}

    def save(
        self,
        *args,
        **kwargs,
    ):

        if not self.slug:
            self.slug = slugify(self.category_name)

        super().save(*args, **kwargs)


class Blog(mongo.Document):

    title = mongo.StringField(required=True)
    cover_image = mongo.StringField(required=True)
    category_list = mongo.ListField(mongo.ReferenceField(Category, reverse_delete_rule=mongo.CASCADE), default=[])
    tags = mongo.ListField(mongo.StringField(), default=[])
    slug = mongo.StringField(unique=True)

    meta = {'collection': 'Blogs'}

    def save(
        self,
        *args,
        **kwargs,
    ):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


class BlogContent(mongo.Document):

    index = mongo.IntField(required=True)
    content = mongo.StringField(required=True)
    class_name = mongo.StringField()
    is_multiline = mongo.BooleanField(default=True)
    blog = mongo.ReferenceField(Blog, reverse_delete_rule=mongo.CASCADE)

    meta = {'collection': 'BlogContent'}


class BlogImage(mongo.Document):

    image = mongo.StringField()
    blog = mongo.ReferenceField(Blog, reverse_delete_rule=mongo.CASCADE)

    meta = {'collection': 'BlogImage'}
