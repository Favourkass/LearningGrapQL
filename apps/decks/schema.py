from django.db.models import fields
from graphene_django import DjangoObjectType
from django.utils import timezone

import graphene

from .models import Deck 


class DeckType(DjangoObjectType):
    class Meta:
        model = Deck

class CreateDeck(graphene.Mutation):
    # The class attributes define the response of the mutation
    deck = graphene.Field(DeckType)
    class Arguments:
        # The input arguments for this mutation
        title = graphene.String()
        description = graphene.String() 

    
    def mutate(self,info,title, description):
        d = Deck(title=title, description=description)
        d.save()
        # Notice we return an instance of this mutation
        return CreateDeck(deck=d)