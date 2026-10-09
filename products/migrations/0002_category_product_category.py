from django.db import migrations, models
import django.db.models.deletion


def assign_uncategorized_products(apps, schema_editor):
    Category = apps.get_model("products", "Category")
    Product = apps.get_model("products", "Product")

    category, _ = Category.objects.get_or_create(name="Sin categoría")
    Product.objects.filter(category__isnull=True).update(category_id=category.pk)


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Nombre")),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="get_products",
                to="products.category",
                verbose_name="Categoria",
            ),
        ),
        migrations.RunPython(
            assign_uncategorized_products,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="get_products",
                to="products.category",
                verbose_name="Categoria",
            ),
        ),
    ]
