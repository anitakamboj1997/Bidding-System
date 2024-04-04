from django.apps import apps
from django.contrib import admin


apps_to_register = ["authentication", "bidding"]
models = [model for app in apps_to_register for model in apps.all_models[app].values()]
for model in models:
    try:
        admclass = type(
            model._meta.model.__name__ + "Admin",
            (admin.ModelAdmin,),
            {"list_display": tuple(map(lambda obj: obj.name, model._meta.fields))},
        )
        admin.site.register(model, admclass)

    except admin.sites.AlreadyRegistered:
        pass
    except Exception as msg:
        print(msg)
