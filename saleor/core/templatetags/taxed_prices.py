from django import template
from prices import MoneyRange, TaxedMoney, TaxedMoneyRange

from ...core.utils.taxes import DEFAULT_TAX_RATE_NAME, apply_tax_to_price

register = template.Library()


@register.inclusion_tag('product/_price_range.html', takes_context=True)
def price_range(context, price_range):
    display_gross_prices = context['site'].settings.display_gross_prices
    return {
        'price_range': price_range,
        'display_gross_prices': display_gross_prices}


@register.simple_tag
def tax_rate(taxes, rate_name):
    """Return tax rate value for given tax rate type in current country."""
    if not taxes:
        return 0

    tax = taxes.get(rate_name) or taxes.get(DEFAULT_TAX_RATE_NAME)
    return tax['value']


@register.inclusion_tag('price.html', takes_context=True)
def price(context, base, display_gross=None, html=True):
    if isinstance(base, (TaxedMoney, TaxedMoneyRange)):
        if display_gross is None:
            display_gross = context['site'].settings.display_gross_prices

        if isinstance(base, TaxedMoneyRange):
            if display_gross:
                base = MoneyRange(start=base.start.gross, stop=base.stop.gross)
            else:
                base = MoneyRange(start=base.start.net, stop=base.stop.net)

        if isinstance(base, TaxedMoney):
            base = base.gross if display_gross else base.net

    is_range = isinstance(base, MoneyRange)
    return {'price': base, 'is_range': is_range, 'html': html}


@register.inclusion_tag('start_price.html', takes_context=True)
def product_start_price(context, product):
    taxes = context['request'].taxes
    display_gross_prices = context['site'].settings.display_gross_prices

    tax_rate_ = product.tax_rate or product.product_type.tax_rate
    taxed_price = apply_tax_to_price(taxes, tax_rate_, product.price)

    result = taxed_price.gross if display_gross_prices else taxed_price.net

    return {'price': result}
