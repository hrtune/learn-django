# Static files

* Web applications generally need to serve additional files.
    * such as images, JavaScript, or CSS


For polls,
```
polls/static/polls
```

Make `polls/static/polls/style.css`

Then apply the css
`polls/templates/polls/index.html`
```html
{% load static %}

<link rel="stylesheet" href="{% static 'polls/style.css' %}">
```
* The `{% static %}` template tag generates the absolute URL of static files.

## For images

* Create a directory `polls/static/polls/images/` and put images in it.

Apply to a css
```css
body {
    background: white url("images/background.png") no-repeat;
}
```
* The `{% static %}` template tag is not available here.
