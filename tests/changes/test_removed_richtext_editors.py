# PR #3

from django.forms import model_to_dict

from saleor.dashboard.page.forms import PageForm
from saleor.dashboard.product.forms import ProductForm
from saleor.product.models import Product


def test_page_content(page, default_category):
    data = model_to_dict(page)
    data['content'] = (
        '<b>bold</b><p><i>italic</i></p><h2>Header</h2><h3>subheader</h3>'
        '<blockquote>quote</blockquote>'
        '<p><a href="www.mirumee.com">link</a></p>'
        '<p>an <script>evil()</script>example</p>')
    form = PageForm(data, instance=page)
    assert form.is_valid()
    form.save()

    assert page.content == data['content']
    assert page.seo_description == (
        'bolditalicHeadersubheaderquotelinkan evil()example')


def test_product_description(product_type, default_category):
    product = Product.objects.create(
        name='Test Product', price=10, description='', pk=10,
        product_type=product_type, category=default_category)
    data = model_to_dict(product)
    data['description'] = (
        '<b>bold</b><p><i>italic</i></p><h2>Header</h2><h3>subheader</h3>'
        '<blockquote>quote</blockquote>'
        '<p><a href="www.mirumee.com">link</a></p>'
        '<p>an <script>evil()</script>example</p>')
    data['price'] = 20

    form = ProductForm(data, instance=product)
    assert form.is_valid()

    form.save()
    assert product.description == data['description']
    assert product.seo_description == (
        'bolditalicHeadersubheaderquotelinkan evil()example')
