


# def generate_slug(text, model_class: Model, instance=None):
#     base_slug = slugify(text)
#     slug = base_slug
#     counter = 1
#     kwargs = {'slug': slug}
#     if instance and hasattr(instance, 'pk') and instance.pk:
#         kwargs['pk__ne'] = instance.pk
#     while model_class.objects.filter(**kwargs).exists():
#         slug = f"{base_slug}-{counter}"
#         kwargs['slug'] = slug
#         if instance and hasattr(instance, 'pk') and instance.pk:
#             kwargs['pk__ne'] = instance.pk
#         counter += 1
#     return slug