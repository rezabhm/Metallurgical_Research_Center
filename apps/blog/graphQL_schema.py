import graphene
from graphene_mongo import MongoengineObjectType
from apps.blog.document import Blog, BlogContent


class BlogType(MongoengineObjectType):
    class Meta:
        model = Blog


class BlogContentType(MongoengineObjectType):
    class Meta:
        model = BlogContent


class Query(graphene.ObjectType):
    blogs = graphene.List(
        BlogType,
        title=graphene.String(),
        slug=graphene.String(),
        category_list=graphene.List(graphene.String),
        tags=graphene.List(graphene.String),
    )

    blogs_content = graphene.List(BlogContentType, id=graphene.String(), parent=graphene.String())

    def resolve_blogs(self, info, title=None, slug=None, category_list=None, tags=None):
        query = Blog.objects  # دریافت تمام مقادیر

        if title:
            query = query.filter(title=title)
        if slug:
            query = query.filter(slug=slug)
        if category_list:
            query = query.filter(category_list__in=category_list)
        if tags:
            query = query.filter(tags__in=tags)

        return list(query)  # تبدیل به لیست و بازگرداندن نتیجه

    def resolve_blogs_content(self, info, id=None, parent=None):

        query = BlogContent.objects

        if id:
            query = query.filter(id=id)

        if parent:
            query = query.filter(blog=parent)

        return list(query)


schema = graphene.Schema(query=Query)
