from import_export import resources

from recipe_house_backend.apps.post.models import Tag, Cuisine, Category, PostType


class TagResource(resources.ModelResource):
    class Meta:
        model = Tag


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class CuisineResource(resources.ModelResource):
    class Meta:
        model = Cuisine



class PostTypeResource(resources.ModelResource):
    class Meta:
        model = PostType

