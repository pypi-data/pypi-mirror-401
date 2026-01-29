from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EmbeddingCache",
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
                ("model_label", models.CharField(max_length=200)),
                ("object_id", models.CharField(max_length=255)),
                ("embedding_vector", models.TextField()),
                ("content_hash", models.CharField(max_length=64)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("model_label", "object_id"),
                        name="embeddingcache_unique_object",
                    )
                ],
            },
        )
    ]
