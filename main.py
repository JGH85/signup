#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

#make regex checks
user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_user (username):
    return user_re.match(username)

password_re = re.compile(r"^.{3,20}$")
def valid_password (password):
    return password_re.match(password)

email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email (email):
    return email_re.match(email)


#create html header boilerplate
html_header = """
<!DOCTYPE html>
    <html>
    <head>
        <style>
            .error {
                color:red;
                font-style:italic;
            }
        </style>

        <title>

        </title>
    </head>
    <body>

"""
#create html footer boilerplate
html_footer = """
</body>
</html>
"""



#create signup form. this will use post later but use get for now.
signup_form = """
<form method = "post" >
<label>
    User Name:
    <input type = "text" name = "username" value = "%(username)s"/>
</label>
<span class = "error"> %(userError)s </span>
<br>
<br>
<label>
    Password:
    <input type = "password" name = "password" value =''/>
</label>
<span class = "error"> %(invPass)s  </span>
<br>
<br>
<label>
    Verify Password:
    <input type = "password" name = "verifypassword" value = ''/>
</label>
<span class = "error">  %(verError)s   </span>
<br>
<br>
<label>
    Email (optional):
    <input type = "text" name = "email" value = "%(email)s"/>
</label>
<span class = "error"> %(email_err)s </span>
<br>
<br>
<input type = "submit">
</form>
"""



class MainHandler(webapp2.RequestHandler):
    def write_form(self, pagetitle='', username='', userError='', invPass='', verError='', email='', email_err=''):
        self.response.write(html_header + pagetitle +
                    signup_form %{
                    "username": username,
                    "userError": userError,
                    "invPass":invPass,
                    "verError":verError,
                    "email":email,
                    "email_err":email_err }
                    + html_footer)

    def get(self):
        title = "<h1> User Signup</h1>"
        self.write_form(title)

    def post(self):
        #initiate errors variable as False
        errors = False

        #initiate all variables
        title = "<h1> User Signup</h1>"
        user = self.request.get("username")
        passwordEntered = self.request.get("password")
        verify = self.request.get("verifypassword")
        emailaddress = self.request.get("email")

        #initiate error variables
        usernameError = ''
        invalidPasswordError = ''
        verifyError = ''
        emailError = ''

        #check on validity of username
        if valid_user(user) == None:
            errors = True
            usernameError = "Invalid username."

        #to do verify valid password
        if valid_password(passwordEntered) == None:
            errors = True
            invalidPasswordError = "Invalid password."

        #TO DO check if password and verify password match each other
        if passwordEntered != verify:
            errors = True
            verifyError = "Passwords do not match."

        #TO DO check if the user email is valid.
        #if email not valid, return error and leave email in box
        if emailaddress != '' and valid_email(emailaddress)==None:
            errors = True
            emailError = "Invalid email address."

        # if any errors, rewrite form with error messages.
        if errors == True:
            self.write_form(title, user, usernameError, invalidPasswordError, verifyError, emailaddress, emailError)
        #TO DO if no errors go to welcome page. SUCCESS AT LAST!!!!!!!
        if errors == False:
            self.redirect("/welcome?username="+user)

class validNameHandler(webapp2.RequestHandler):
    """handles requests coming into \welcome
    """
    def get(self):
        welcome_user = self.request.get("username")
        welcome_text = "<h1> Welcome, " + welcome_user + "!</h1>"
        self.response.write(html_header + welcome_text + html_footer)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', validNameHandler)
], debug=True)
