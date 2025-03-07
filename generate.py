import glob

from jinja2 import Environment, BaseLoader

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
      {% for img in images -%}
      <a href="{{ img }}">
        <img src="{{ img }}" alt="Sexy? Yes.">
      </a>
      {% endfor %}
    </section>

    <div class="sexy_popup">
      <img src="assets/popup.png" alt="Hello!">
    </div>
  </body>
</html>
"""

def generate():
    images = sorted(glob.glob("images/*.jpg"))
    env = Environment(loader=BaseLoader).from_string(template)
    output = env.render(images=images)

    with open("index.html", "w") as f:
        f.write(output)


if __name__ == "__main__":
    generate()
