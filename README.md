(# HexaShop — Django E‑commerce Demo)

This repository contains HexaShop, a small Django-based e-commerce demo app used for learning and experimentation. It includes a product catalogue (unified Product model), per-user carts backed by `Cart`/`CartItem` models, basic product listing with pagination, and classic Django templates + static assets adapted from a TemplateMo theme.

## Key features

- Django project (project root: `Hexashop/`) with a single app: `myapp`
- Product listing with pagination (9 items per page)
- Product detail pages and an Add-to-Cart flow
- Per-user persisted `Cart` and `CartItem` models (server-side storage)
- Admin site registration for managing products
- Static assets and templates under `static/` and `templates/` respectively

## Prerequisites

- Python 3.10+ installed
- A virtual environment (recommended) — this repo includes a sample `env/` folder in the workspace
- MySQL or other DB configured in `Hexashop/settings.py` (the project currently used MySQL in development)

Note on MySQL authentication: If your MySQL user uses the `caching_sha2_password` or `sha256_password` plugin you will need the `cryptography` package installed in the project's virtualenv. If you see an error like:

"RuntimeError: cryptography is required for sha256_password or caching_sha2_password authentication"

Install it with:

```powershell
& .\env\Scripts\Activate.ps1
python -m pip install cryptography
```

Alternatively change the MySQL user's authentication plugin to `mysql_native_password` on the server.

## Quickstart — run locally

1. Open a terminal in the project root (where `manage.py` lives):

```powershell
cd C:\Users\Victus\OneDrive\Desktop\HexaShop_project\Hexashop
& .\env\Scripts\Activate.ps1
```

2. Install Python dependencies (if you don't already have them installed in the virtualenv):

```powershell
python -m pip install -r requirement.txt
# If MySQL auth requires it:
python -m pip install cryptography
```

3. Create and apply migrations:

```powershell
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser to access Django admin (optional but useful):

```powershell
python manage.py createsuperuser
```

5. Run the development server:

```powershell
python manage.py runserver
```

6. Open the site in your browser (default): http://127.0.0.1:8000/

## Project structure (important files)

- `manage.py` — Django manage entrypoint
- `Hexashop/settings.py` — Django settings (DB, static files, installed apps)
- `myapp/models.py` — domain models (Product, Cart, CartItem, etc.)
- `myapp/views.py` — product listing, details, add-to-cart and cart views
- `myapp/urls.py` — app URL routes
- `templates/myapp/` — HTML templates (product listing, product detail, cart, etc.)
- `static/myapp/` — CSS, JS and images used by templates

## Notes about the data model & migrations

During development the codebase consolidated multiple category-specific product tables into a single `Product` model. If you are migrating an earlier database (with `MensProduct`, `WomensProduct`, `KidsProduct` tables), consider writing a data migration or a small management command to copy existing rows into the new `Product` table before applying destructive migrations.

If you don't need to preserve previous product data, you can run `makemigrations`/`migrate` directly.

## Admin

Open `/admin/` after creating a superuser to add or edit products. The `Product` model fields include name, price, image path/url and category.

## Styling and templates

Templates are in `templates/myapp/`. Static assets (CSS/JS/images) live under `static/myapp/`.

I applied a small inline CSS fix in `templates/myapp/products.html` to prevent rating stars from overlapping the price; for production you should move these rules into `static/myapp/css/templatemo-hexashop.css`.

## Running tests

If the project contains tests, you can run them with:

```powershell
python manage.py test
```

## Troubleshooting

- DB connection errors: check `Hexashop/settings.py` DATABASES block and ensure credentials and host are correct.
- MySQL auth error about `cryptography`: install `cryptography` in the virtualenv or change the MySQL user's auth plugin.
- Template issues (missing static files): ensure `STATICFILES_DIRS` and `STATIC_ROOT` are configured correctly and that `python manage.py collectstatic` has been run when serving static files in production.

## Next steps & suggestions

- Move inline styles in templates to the main stylesheet for maintainability.
- Make product cards fully responsive (use percentage widths / responsive image aspect ratios instead of fixed pixel heights).
- Add AJAX endpoints for cart quantity updates for a smoother UX.
- If you need to preserve existing product/cart data from older schema, I can prepare a data migration script to port rows from the old tables into the new `Product` table and update `CartItem` references.

---

If you want, I can now:

- Move the inline CSS into the project's CSS file.
- Create a small data-migration script to help migrate old product tables into the new `Product` model.
- Add a short CONTRIBUTING.md with developer flow and commit guidelines.

Tell me which of those you'd like me to do next.

