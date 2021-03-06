import re
from django.utils.html import escape

def convert_bb_to_html(text):
    """Converts a piece of text with bb-tags (like [b] and [img]) to
    html. Any 'real' HTML tags that were present in the original text
    are html-escaped."""

    # First escape the text to get rid of all HTML tags.
    text = escape(text)

    # Now we can safely replace the bb-tags and be sure that those will be
    # the only HTML tags in the text.
    replacements = [
        ('\[b\](.+?)\[/b\]',  '<b>\\1</b>'),
        ('\[i\](.+?)\[/i\]',  '<i>\\1</i>'),
        ('\[ul\](.+?)\[/ul\]',  '<ul>\\1<//ul>'),
        ('\[li\](.+?)\[/li\]',  '<li>\\1<//i>'),
        ('\[img\](.+?)\[/img\]', '<img src="\\1" />'),
        ('\[url\](.+?)\[/url\]', '<a href="\\1">\\1</a>'),
        ('\[url=(.+?)\](.+?)\[/url\]', '<a href="\\1">\\2</a>'),
        ("\n", '<br />'),
        ("\[br\]", '<br />'),
    ]

    for r in replacements:
        p = re.compile(r[0])
        text = p.sub(r[1], text)

    return text

def get_square_html(color, size):
    html = '<table class="blokje" border="0" cellspacing="0" cellpadding="0">'
    html += "\n"
    html += '<tr>';
    html += '<td width="%d" height="%d" ' % (size, size)
    html += 'bgcolor="#%s">' % color
    html += '<img src="http://media.carnique.nl/images/spacer.gif" '
    html += 'alt="" height="%d" width="%d">' % (size, size)
    html += "</td></tr></table>\n";
    return html

def get_square_color(age):
    if age is None or age < 0:
        return '000000';

    if age == 0:
        return 'FFFFFF';

    black_time = 28 * 86400

    if age >= black_time:
        return '000000'

    colors = [
        {
          'max_time': 0,
          'color': (255, 255, 255),
        },
        {
          'max_time': 7 * 86400,
          'color': (204, 204, 51),
        },
        {
          'max_time': 14 * 86400,
          'color': (102, 204, 0),
        },
        {
          'max_time': 21 * 86400,
          'color': (204, 51, 0),
        },
        {
          'max_time': black_time,
          'color': (0, 0, 0),
        },
    ]

    index = 0
    while age > colors[index]['max_time']:
        index += 1

    minc = colors[index - 1]['color']
    maxc = colors[index]['color']
    mint = colors[index - 1]['max_time']
    maxt = colors[index]['max_time']

    ratio = float(age - mint) / float(maxt - mint)

    red   = int(minc[0] + ratio * (maxc[0] - minc[0]))
    blue  = int(minc[1] + ratio * (maxc[1] - minc[1]))
    green = int(minc[2] + ratio * (maxc[2] - minc[2]))
    color = "%02X%02X%02X" % (red, blue, green)

    return color;
