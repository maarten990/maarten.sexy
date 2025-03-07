import glob

from jinja2 import Environment, BaseLoader
from PIL import Image

template = """
<html>
  <head>
    <meta charset="utf-8">
    <link rel="stylesheet" type="text/css" href="sexy.css"/>
    <title>The sexiest place on the internet</title>
  </head>

  <body>
    <div class="sexy_header">
    </div>

    <section id="sexy_photos">
      {% for col in columns -%}
      <div class="grid_col">
        {% for img in col -%}
        <a href="{{ img }}">
          <img src="{{ img }}" alt="Sexy? Yes.">
        </a>
        {% endfor -%}
      </div>
      {% endfor -%}
    </section>

    <div class="sexy_popup">
      <img src="assets/popup.png" alt="Hello!">
    </div>
  </body>
</html>
"""


def make_col(sizes, goal) -> list[str]:
    out = []

    while goal > 0 and len(sizes) > 0:
        distances = {img: goal - size for img, size in sizes.items()}
        next = sorted(distances, key=lambda img: sizes[img], reverse=True)[0]
        out.append(next)
        goal -= sizes[next]
        sizes.pop(next)

    return out


def pack_columns() -> list[list[str]]:
    images = list(glob.glob("images/*.jpg"))

    # normalize the image sizes to a width of 1, since they'll all have the same width
    sizes = {img: Image.open(img).size for img in images}
    sizes = {img: height/width for img, (width, height) in sizes.items()}
    goal = sum(sizes.values()) / 5

    packed = []
    while len(sizes) > 0:
        packed.append(make_col(sizes, goal))

    return packed


def generate():
    columns = pack_columns()
    env = Environment(loader=BaseLoader).from_string(template)
    output = env.render(columns=columns)

    with open("index.html", "w") as f:
        f.write(output)


if __name__ == "__main__":
    generate()
