from dataclasses import dataclass

import strawberry_django
from strawberry_django import FilterLookup

from netbox.graphql.filter_mixins import NetBoxModelFilterMixin

from netbox_cesnet_services_plugin.models import (
    BGPConnection,
    LLDPNeighbor,
    LLDPNeighborLeaf,
)


@strawberry_django.filter_type(LLDPNeighbor, lookups=True)
@dataclass
class LLDPNeighborFilter(NetBoxModelFilterMixin):
    status: FilterLookup[str] | None = strawberry_django.filter_field()
    status_detail: FilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter_type(LLDPNeighborLeaf, lookups=True)
@dataclass
class LLDPNeighborLeafFilter(NetBoxModelFilterMixin):
    status: FilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter_type(BGPConnection, lookups=True)
@dataclass
class BGPConnectionFilter(NetBoxModelFilterMixin):
    role: FilterLookup[str] | None = strawberry_django.filter_field()
