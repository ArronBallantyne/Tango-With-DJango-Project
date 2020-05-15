from django.template.defaultfilters import slugify

def add_category(name, views=0, likes=0):
    category = Category(name)
    category.views = views
    category.likes = likes
    category.save()
    return category


def delete():
    Category.objects.clear()


class Category():

    objects = []

    def __init__(self, name):
        self.name = name
        self.views = 0
        self.likes = 0
        self.slug = slugify(name)

    def save(self):
        self.objects.append(self)

