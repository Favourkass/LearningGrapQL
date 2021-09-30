# LearningGrapQL
i am trying my hands out with graphQL by building a project

list of calls that can be made to the API

 query{
   decks{
    id
     description
     title
   }
 } 

query {
   deckCards(deck:1) {
     id
     question
     answer
   }
  
 }
 mutation {
   updateCard(id:1, question:"Hello", answer:"hi", status:3){
     card{
       id
       question
       bucket
       nextReviewAt
     }
   }
 }

 mutation {
   createCard(question:"what is your name?", answer:"...", deckId:1){
   	card {
     	id
   }
 }
 }

 mutation {
   createDeck(description:"hello world 2", title:"second deck 2"){
     deck{
       id
     }
   }
 }
