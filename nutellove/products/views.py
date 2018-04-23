import functools
import operator

from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import Brand, Category, Product, Favorite
from django.utils.translation import gettext
from django.views import View
from django.db.models import Q

from .controllers import *

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
                products = Product.objects.filter(brands=obj.id)
                title = "Produits de la marque {}".format(obj.name)
            elif self.model == Category:
                products = Product.objects.filter(cat=obj.id)
                title = "Produits de la catégorie {}".format(obj.name)

            products = view_pagination(request, 6, products)
            page_range = page_indexing(products, 6)

            # check if user is not anonymous
            if user.username != "":
                for product in products:
                    if Favorite.objects.filter(
                        substitute=product, user=user
                    ).exists():
                        product.is_favorite = True
                    else:
                        product.is_favorite = False

            context = {
                'obj': obj,
                'title': title,
                'products': products,
                'paginate': True,
                'page_range': page_range,
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
            page_range = None

        else:
            # title contains the query and query is not sensitive to case.
            products = Product.objects.filter(name__icontains=query)

            # split the query in multiple parts (list)
            q = query.split(" ")

            if products:
                chosen_product = products[0]

                # https://stackoverflow.com/questions/4824759/
                # django-query-using-contains-each-value-in-a-list
                # https://docs.python.org/2/library/operator.html
                new_query = functools.reduce(
                    operator.or_, (
                        Q(
                            name__icontains=item
                        ) for item in q)
                )

                # returns a list of products excluding the chosen product
                # order products by nutri_grade,
                # after a product has been chosen
                products = Product.objects.filter(
                    new_query,
                    cat=chosen_product.cat,
                ).exclude(
                    name=chosen_product.name
                ).order_by(
                    "nutri_grade"
                )

                better_products = select_better_product(
                    chosen_product, products
                )

                products = view_pagination(request, 6, better_products)
                page_range = page_indexing(products, 6)

            else:
                chosen_product = None
                page_range = None

            title = ""

        # check if user is not anonymous
        if user.username != "":  # pragma: no cover
            for product in products:
                if Favorite.objects.filter(
                    substitute=product, user=user
                ).exists():
                    product.is_favorite = True
                else:
                    product.is_favorite = False

        context = {
            'chosen_product': chosen_product,
            'products': products,
            'title': title,
            'query': query,
            'paginate': True,
            'page_range': page_range,
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
        favorite, created = self.model.objects.get_or_create(
            substitute=product, user=user
        )

        # If no new bookmark has been created,
        # Then we believe that the request was to delete the bookmark
        if not created:
            favorite.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
