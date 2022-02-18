from django.contrib.humanize.templatetags.humanize import intcomma


def make_display_price(price):
    naira = round(price, 9)
    return "$%s%s" % (intcomma(int(naira)), ("%0.9f" % naira)[-3:])