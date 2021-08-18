from django.db import models


class BaseManager(models.Manager):

    # Base function to create an object in database
    def create(self, **kwargs):
        return super(BaseManager, self).create(**kwargs)

    # Function to get all the values from the table
    def get_all(self):
        return super(BaseManager, self).all()

    # function to get the objects by passing their id
    def get_by_id(self, pk):
        return super(BaseManager, self).get(pk=pk)

    # Function to filter the objects list passing the parameters
    def get_by_filter(self, **filter_args):
        return self.get_all_active().filter(**filter_args)

    # Function to get all the active object from the table
    def get_all_active(self):
        return self.get_all().filter(is_deleted=False)

    # Function to filter the objects list passing the parameters
    def does_exist(self, **filter_args):
        return self.get_by_filter(**filter_args).exists()
