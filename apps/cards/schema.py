from django.db.models import fields
from graphene_django import DjangoObjectType
from django.utils import timezone

import graphene
from graphql import GraphQLError

from .models import Card 
from apps.decks.models import Deck

buckets = (
        (1, 1),
        (2, 3),
        (3, 7),
        (4, 16),
        (5, 30),
 )

def return_date_time(days):
    now = timezone.now()
    return now + timezone.timedelta(days=days)

class CardType(DjangoObjectType):
    class Meta:
        model = Card

class CreateCard(graphene.Mutation):
    # The class attributes define the response of the mutation
    card = graphene.Field(CardType)
    class Arguments:
        # The input arguments for this mutation
        question = graphene.String()
        answer = graphene.String() 
        deck_id = graphene.Int()

    
    def mutate(self,info,question, answer, deck_id):
        c = Card(question=question, answer=answer)
        d=Deck.objects.get(id=deck_id)
        c.deck = d
        c.save()
        # Notice we return an instance of this mutation
        return CreateCard(card=c)

    
class UpdateCard(graphene.Mutation):
    card = graphene.Field(CardType)
    class Arguments:
        id = graphene.ID()
        question = graphene.String()
        answer = graphene.String()
        # easy, average or hard -> 1,2,3 (determines if they move up a bucket)
        status = graphene.Int(description="easy, average or hard -> 1,2,3 (determines if you move up a bucket)")

    def mutate(self,info, id,question, answer, status):
        if status not in [1,2,3]:
            raise GraphQLError("status out of bounds, must be 1, 2 or 3")
        c = Card.objects.get(id=id)
        bucket = c.bucket
        if status == 1 and bucket >1:
             bucket -= 1
        elif status == 3 and bucket <= 4:
            bucket  += 1

        # calculate next review date
        days = buckets[bucket-1][1]
        next_review = return_date_time(days)
 
        c.question=question
        c.answer=answer 
        c.bucket=bucket
        c.next_review_at=next_review
        c.last_review_at=timezone.now() 
        c.save()
        return UpdateCard(card=c)