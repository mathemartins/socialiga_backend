from .signals import object_viewed_signal


class ObjectViewedMixin(object):
    def get_serializer_context(self, *args, **kwargs):
        context = super(ObjectViewedMixin, self).get_serializer_context(*args, **kwargs)
        request = self.request
        instance = context.get('object')
        if instance:
            object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return context
