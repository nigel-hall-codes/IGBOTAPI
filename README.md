# APIS

## accounts/login/
### type: POST
### params:
#### username: String
#### password: String

## accounts/create/
### type: POST
### params:
#### username: String
#### password: String
#### email: String

## accounts/<int:id>/settings/
### type: GET
### params:
#### None

## accounts/<int:id>/settings/ig
### type: POST
### params:
#### igusername: String
#### igpassword: String

## accounts/<int:id>/settings/wm
### type: POST
### params:
#### url: String

## accounts/<int:userID>/bot/run
### type: GET
### params:
#### None.  This will start the bot

## accounts/<int:userID>/bot/testpost
### type: GET
### params:
#### None.  This will test the bot by posting a meme

## accounts/<int:userID>/bot/stop
### type: GET
### params:
#### None.  THis will destroy the bot

