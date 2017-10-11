from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.related import ForeignObjectRel
from rest_framework.filters import OrderingFilter, DjangoObjectPermissionsFilter


class RelatedOrderingFilter(OrderingFilter):
    """
    Extends OrderingFilter to support ordering by fields in related models
    using the Django ORM __ notation
    """
    def is_valid_field(self, model, field):
        """
        Return true if the field exists within the model (or in the related
        model specified using the Django ORM __ notation)
        """
        components = field.split('__', 1)
        try:
            field, parent_model, direct, m2m = \
                model._meta.get_field_by_name(components[0])

            # reverse relation
            if isinstance(field, ForeignObjectRel):
                return self.is_valid_field(field.model, components[1])

            # foreign key
            if field.rel and len(components) == 2:
                return self.is_valid_field(field.rel.to, components[1])
            return True
        except FieldDoesNotExist:
            return False

    def remove_invalid_fields(self, queryset, ordering, view):
        return [term for term in ordering
                if self.is_valid_field(queryset.model, term.lstrip('-'))]
    
class DjangoModelObjectPermissionsFilter(DjangoObjectPermissionsFilter):
    
    def filter_queryset(self, request, queryset, view):
        # We want to defer this import until run-time, rather than import-time.
        # See https://github.com/encode/django-rest-framework/issues/4608
        # (Also see #1624 for why we need to make this import explicitly)
        from guardian.shortcuts import get_objects_for_user

        user = request.user
        model_cls = queryset.model
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name
        }
        # self.perm_format comes from DjangoObjectPermissionsFilter
        permission = self.perm_format % kwargs
        extra = {
            # we need it True here to take model level control into account
            'accept_global_perms': True,  
        }
        return get_objects_for_user(user, permission, queryset, **extra)