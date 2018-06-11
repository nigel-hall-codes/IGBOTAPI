# APIS

## account/login/
### type: POST
### params:
username: String
password: String

## account/create/
### type: POST
### params:
username: String
password: String
email: String

## account/<int:id>/settings/
### type: GET
### params:
None

## account/<int:id>/settings/ig
### type: POST
### params:
igusername: String
igpassword: String

## account/<int:id>/settings/wm
### type: POST
### params:
url: String