from django.db import migrations
from apps.authentication.services import create_dev_user


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0002_auto_20220801_1647"),
    ]

    operations = [migrations.RunPython(create_dev_user)]
