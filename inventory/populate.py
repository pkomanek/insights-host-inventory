import random

import uuid
import os
import django
from django.db.transaction import atomic

products = (["Red Hat Enterprise Linux"] * 75) + ["Openstack", "Red Hat Virtualization"]
versions = ["7.0", "7.1", "7.2", "7.3", "7.4", "7.5"]
accts = ["%07d" % n for n in range(1, 99)]


@atomic
def populate(count=100):
    from inventory.models import Entity, Tag

    def make_facts():
        return {
            "default": {
                "hostname": e.display_name.replace("ent", "host"),
                "product": random.choice(products),
                "version": random.choice(versions),
            }
        }

    def make_tags(namespace):
        t = Tag.objects.create(namespace=namespace, name="fun", value="times")
        t.save()
        return t

    def make_ids():
        return {"pmaas_id": str(uuid.uuid4()), "hccm_id": str(uuid.uuid4())}

    for x in range(count):
        acct = random.choice(accts)
        e = Entity.objects.create(account=acct, display_name="ent_%d" % x)
        e.facts = make_facts()
        e.tags.add(make_tags(namespace=acct))
        e.canonical_facts = make_ids()
        print(e.canonical_facts["pmaas"])
        e.save()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insights.settings")
    django.setup()
    populate()
