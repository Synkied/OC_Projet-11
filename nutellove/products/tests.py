import datetime
import json

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Product, Category, Brand, Store, Favorite


class DetailPageTestCase(TestCase):
    # test that detail page returns a 200 if the item exists.

    def setUp(self):
        # create a category
        biscuit_category = Category.objects.create(name="Biscuits")

        # create a product
        biscuit = Product.objects.create(
            code="39047011496",
            url="http://world-fr.openfoodfacts.org/produit/0039047011496/pure-butter-chocolate-chip-shortbread-walkers",
            name="Pure Butter Chocolate Chip Shortbread",
            nutri_grade="e",
            cat=Category.objects.get(
                name="Biscuits"
            ),
            last_modified_t=timezone.make_aware(
                datetime.datetime.fromtimestamp(1446034301)
            ),
        )

        # get the product base on its url (because it is unique)
        self.product = Product.objects.get(
            url="http://world-fr.openfoodfacts.org/produit/0039047011496/pure-butter-chocolate-chip-shortbread-walkers"
        )

    # test that detail page returns a 200 if the item exists
    def test_detail_page_returns_200(self):
        product_id = self.product.id
        response = self.client.get(
            reverse('products:product_detail', args=(product_id,))
        )
        self.assertEqual(response.status_code, 200)

    # test that detail page returns a 404 if the items does not exist
    def test_detail_page_returns_404(self):
        product_id = self.product.id + 1
        response = self.client.get(
            reverse('products:product_detail', args=(product_id,))
        )
        self.assertEqual(response.status_code, 404)


class SearchProductPageTestCase(TestCase):
    # test that detail page returns a 200 if the item exists.

    def setUp(self):
        # create a category
        biscuit_category = Category.objects.create(name="Biscuits")
        soupe_category = Category.objects.create(name="Soupes")
        chips_category = Category.objects.create(name="Chips et frites")

        # create a product
        biscuit = Product.objects.create(
            code="39047011496",
            url="http://world-fr.openfoodfacts.org/produit/0039047011496/pure-butter-chocolate-chip-shortbread-walkers",
            name="Gateau au chocolat trop sucré",
            nutri_grade="e",
            cat=Category.objects.get(
                name="Biscuits"
            ),
            last_modified_t=timezone.make_aware(
                datetime.datetime.fromtimestamp(1498134406)
            ),
        )

        soupe = Product.objects.create(
            code="454587",
            url="http://world-fr.openfoodfacts.org/produit/00454587/soupe-nulle",
            name="Soupe nulle",
            nutri_grade="a",
            cat=Category.objects.get(
                name="Soupes"
            ),
            img="https://static.openfoodfacts.org/images/products/003/904/701/1496/front_fr.9.400.jpg",
            last_modified_t=timezone.make_aware(
                datetime.datetime.fromtimestamp(1498134406)
            ),
        )

        gateau = Product.objects.create(
            code="454588",
            url="http://world-fr.openfoodfacts.org/produit/00454588/gateau",
            name="gateau cool au chocolat",
            nutri_grade="b",
            cat=Category.objects.get(
                name="Biscuits"
            ),
            last_modified_t=timezone.make_aware(
                datetime.datetime.fromtimestamp(1498134406)
            ),
        )

        chips = Product.objects.create(
            code="976015",
            url="http://world-fr.openfoodfacts.org/produit/00976015/chips-de-legumes-marks-spencer",
            name="Chips de légumes",
            nutri_grade="c",
            cat=Category.objects.get(
                name="Chips et frites"
            ),
            last_modified_t=timezone.make_aware(
                datetime.datetime.fromtimestamp(1498134406)
            ),
        )

        # get the product base on its url (because it is unique)
        self.product = Product.objects.get(
            url="http://world-fr.openfoodfacts.org/produit/0039047011496/pure-butter-chocolate-chip-shortbread-walkers"
        )

    def test_search_page_returns_products(self):
        """
        test that the search returns the searched product
        """
        response = self.client.get(
            reverse('products:search'), {"query": "chocolat"}
        )

        self.assertIn(b'gateau cool au chocolat', response.content)

    def test_random_list_of_products_if_query_not_found(self):
        """
        Test that a query with products not found
        returns to a page displaying a certain message
        """
        response = self.client.get(
            reverse('products:search'), {"query": "query_not_in_products"}
        )

        line = bytearray(
            "Mince, aucun produit ne correspond à cette recherche. Cherchez à nouveau !".encode('utf8')
        )

        # test that the Soupe Nulle product is displayed in the favorites,
        # as it was set up in the setUp() method.
        self.assertIn(line, response.content)

    def test_random_list_of_products_if_no_query(self):
        """
        Test that an empty query
        returns to a page displaying a certain message
        and suggestes products
        """
        response = self.client.get(
            reverse('products:search')
        )

        # test that the Soupe Nulle product is displayed in the favorites,
        # as it was set up in the setUp() method.
        self.assertIn(b'Suggestion de produits', response.content)


# Favorite page

class FavoritesTestCase(TestCase):
    """
    Testing the favorites page
    """

    def setUp(self):
        biscuit_category = Category.objects.create(name="Biscuits")
        soupe_category = Category.objects.create(name="Soupes")

        # create a product
        biscuit = Product.objects.create(
            code="39047011496",
            url="http://world-fr.openfoodfacts.org/produit/0039047011496/pure-butter-chocolate-chip-shortbread-walkers",
            name="Pure Butter Chocolate Chip Shortbread",
            nutri_grade="e",
            cat=Category.objects.get(
                name="Biscuits"
            ),
            last_modified_t=timezone.make_aware(
                datetime.datetime.fromtimestamp(1446034301)
            ),
        )

        soupe = Product.objects.create(
            code="454587",
            url="http://world-fr.openfoodfacts.org/produit/00454587/soupe-nulle",
            name="Soupe nulle",
            nutri_grade="a",
            cat=Category.objects.get(
                name="Soupes"
            ),
            last_modified_t=timezone.make_aware(
                datetime.datetime.fromtimestamp(1498134406)
            ),
        )

        # get the product base on its url (because it is unique)
        self.biscuit_product = Product.objects.get(
            url="http://world-fr.openfoodfacts.org/produit/0039047011496/pure-butter-chocolate-chip-shortbread-walkers"
        )

        self.soupe_product = Product.objects.get(
            url="http://world-fr.openfoodfacts.org/produit/00454587/soupe-nulle",
        )

        # define a user to add and remove favorites
        User.objects.create_user(username="testuser", email="test@test.fr", password="mdptest1234")
        self.user = User.objects.get(username="testuser")

        # connect our user
        response = self.client.post(reverse('users:login'), {
            'username': "testuser",
            'password': "mdptest1234",
        })

        a_favorite = Favorite.objects.create(
            substitute=self.soupe_product, user=self.user
        )

    def test_add_product_to_favorite(self):
        """
        Test if a product can be add to the favorite list of a user
        """
        old_favorites = Favorite.objects.count()

        product_id = self.biscuit_product.id

        self.client.post(
            reverse('products:bookmark', args=(product_id,))
        )

        new_favorites = Favorite.objects.count()

        self.assertEqual(new_favorites, old_favorites + 1)

    def test_remove_product_from_favorite(self):
        """
        Test if a product can be removed from the favorite list of a user
        """
        old_favorites = Favorite.objects.count()

        product_id = self.soupe_product.id

        response = self.client.post(
            reverse('products:bookmark', args=(product_id,))
        )

        new_favorites = Favorite.objects.count()

        self.assertEqual(new_favorites, old_favorites - 1)

    def test_get_favorites_list(self):
        """
        Test if the favorites of a user are displayed on the favorites page
        """
        response = self.client.get(
            reverse('products:favorites')
        )

        # test that the Soupe Nulle product is displayed in the favorites,
        # as it was set up in the setUp() method.
        self.assertIn(b'Soupe nulle', response.content)
