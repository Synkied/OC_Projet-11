from random import randint

from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import Brand, Category, Product, Favorite
from django.utils.translation import gettext
from django.views import View

# Create your views here.


def listing(request):  # pragma: no cover
    """
    List all available products on a page
    """
    products = Product.objects.filter()[:9]

    title = gettext("Tous nos produits")

    context = {
        'products': products,
        'title': title,
        'paginate': True
    }

    return render(request, 'products/listing.html', context)


class ProductDetail(View):
    template_name = 'products/product_details.html'

    def get(self, request, product_id):
        """
        Used to display the details of a product
        """
        product = get_object_or_404(Product, pk=product_id)
        category = get_object_or_404(Category, pk=product.cat.id)
        brands = [brand.name for brand in product.brands.all()]
        stores = [store.name for store in product.stores.all()]

        context = {
            'product': product,
            'brands': brands,
            'stores': stores,
            'category': category,
        }

        return render(request, self.template_name, context)


class BrandCategoryDetail(View):  # pragma: no cover
    """
    Abstract class to display categories and details
    """
    obj = None
    model = None
    template_name = 'products/category_or_brand_details.html'

    def get(self, request, **kwargs):
        """
        Used to give details of a brand
        """
        user = auth.get_user(request)
        obj_id = kwargs.get('obj_id')

        if obj_id is None:
            objs = self.model.objects.all().order_by('name')

            if self.model == Brand:
                title = "Toutes les marques"
            elif self.model == Category:
                title = "Toutes les catégories"

            context = {
                'objs': objs,
                'title': title,
                'model': self.model.__name__,
            }

            return render(request, self.template_name, context)

        else:
            # get the object with the obj_id passed in the url
            obj = get_object_or_404(self.model, pk=obj_id)

            # conditionnals for text, can be updated I guess
            if self.model == Brand:
                products = Product.objects.filter(brands=obj.id)[:9]
                title = "Produits de la marque {}".format(obj.name)
            elif self.model == Category:
                products = Product.objects.filter(cat=obj.id)[:9]
                title = "Produits de la catégorie {}".format(obj.name)

            # check if user is not anonymous
            if user.username != "":
                for product in products:
                    if Favorite.objects.filter(substitute=product, user=user).exists():
                        product.is_favorite = True
                    else:
                        product.is_favorite = False

            context = {
                'obj': obj,
                'title': title,
                'products': products,
            }

            return render(request, self.template_name, context)


class Search(View):
    """
    Handles the search of products in the app.
    Also contains the algorithm that show better products compared to
    the queried product.
    """

    template_name = 'products/search.html'

    def get(self, request):
        """
        Used to handle queries from user and perform a search
        """
        query = request.GET.get('query')

        user = auth.get_user(request)

        if not query:

            # display random products with imgs
            products = (Product.objects.filter(
                nutri_grade="a").exclude(
                    img__isnull=True).exclude(
                    name__icontains="frite").exclude(
                    name__icontains="frie").order_by('?')
            )[:9]

            title = gettext("Suggestion de produits")

            chosen_product = None

        else:
            # title contains the query and query is not sensitive to case.
            products = Product.objects.filter(name__icontains=query)

            if len(products) > 0:
                chosen_product = products[0]

                if chosen_product.nutri_grade == "a":
                    better_products = [
                        product for product in products
                        if product.nutri_grade == chosen_product.nutri_grade
                    ]
                else:
                    better_products = [
                        product for product in products
                        if product.nutri_grade < chosen_product.nutri_grade
                    ]

                products = better_products[:6]

            else:
                chosen_product = None

            # title = gettext(
            #     "Résultats pour la requête {}".format(
            #         query.capitalize()
            #     )
            # )

            title = ""

        # check if user is not anonymous
        if user.username != "":  # pragma: no cover
            for product in products:
                if Favorite.objects.filter(substitute=product, user=user).exists():
                    product.is_favorite = True
                else:
                    product.is_favorite = False

        context = {
            'chosen_product': chosen_product,
            'products': products,
            'title': title,
            'query': query,
        }

        return render(request, self.template_name, context)


class FavoriteView(LoginRequiredMixin, View):
    """
    Handles two things:
    - get: The showing of a user's favorites
    - post: The add/remove products to favorites, via a specific url (bookmark)
    """

    # pass the model in path args in urls.py
    # e.g: FavoriteView.as_view(model=Favorite)

    model = None
    template_name = 'products/favorites.html'

    def get(self, request, product_id=None):
        """
        Get all the favorites of a user
        """

        user = auth.get_user(request)
        favorites = self.model.objects.filter(user=user)

        context = {
            'favorites': favorites
        }

        # get next url
        next_url = request.GET.get('next')

        # redirect to next url
        if next_url:  # pragma: no cover
            return HttpResponseRedirect(next_url)
        else:
            return render(request, self.template_name, context)

    def post(self, request, product_id):
        """
        Adds or remove a product to the connected user's favorites
        """

        # Get the user if connected
        user = auth.get_user(request)

        # Trying to get a favorite from the database, or create a new one
        product = Product.objects.get(pk=product_id)
        favorite, created = self.model.objects.get_or_create(substitute=product, user=user)

        # If no new bookmark has been created,
        # Then we believe that the request was to delete the bookmark
        if not created:
            favorite.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
