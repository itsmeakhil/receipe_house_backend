from import_export import resources

from app.post.models import Tag, Cuisine, Category


class TagResource(resources.ModelResource):
    class Meta:
        model = Tag


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class CuisineResource(resources.ModelResource):
    class Meta:
        model = Cuisine

