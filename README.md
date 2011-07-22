# Page Objects in Robot Framework #
## Well, Page Objects-ish ##

### Background ###

There are a number of frameworks out there that land into the broad bucket of Acceptance Test Driven Develpment (ATDD) and/or Behaviour Driven Development (BDD). These tools allow for the encoding of product desirables in a human readable Domain Specific Language (DSL) and then automated in some other programming language.

One popular one is the [Robot Framework](http://code.google.com/p/robotframework/) which has an add-on library to extend its DSL to include Selenium commands (keywords in RF terminology) through its [SeleniumLibrary](http://code.google.com/p/robotframework-seleniumlibrary/). But convenience comes at a removal of fine grained control that you get from using the Page Object Pattern directly.

This experiment shows how you can get the best of both worlds with the product ownership team still being able to see their readable DSL but the people implementing the code can use OO principles for driving the interaction with the code.

### Its all about the keywords ###

Much like if you were using SeleniumLibrary, this whole thing revolves around creating custom keywords. Only instead of using the keywords in SeleniumLibrary you use the raw Se API calls in your implementation.

Let's look at a script.

    *** Settings ***

    Documentation  A test suite with a single test for valid login. This test has
    ...            a workflow that is created using keywords from the resource file.
    Resource       common_resource.txt
    Test Setup    Open Browser To English Home Page
    Test Teardown  Close Browser After Run

    *** Test Cases ***

    Invalid Login
        Navigate To Sign In Page
        Set Sign In Email As    demo
        Set Sign In Password As    demo
        Submit Sign In Credentials
        Sign In Error Message Should Be  Sorry, we don't recognize that email address, username or password. Please try again.
        
Nothing unusual there. Now let's look at the keywords associated with the Sign In page.

    from SeleniumWrapper import SeleniumWrapper as wrapper

    locators = {
        "email": "id=Email",
        "password": "id=Password",
        "sign in": "id=submit",
        "error messages": "css=.validation-summary-errors li"
    }

    class SignInPage(object):
        # needed for robot framework
        def get_keyword_names(self):
            return ['set_sign_in_email_as',
                    'set_sign_in_password_as',
                    'submit_sign_in_credentials',
                    'sign_in_error_message_should_be']

        def set_sign_in_email_as(self, email):
            se = wrapper().connection
            se.type(locators["email"], email)

        def set_sign_in_password_as(self, password):
            se = wrapper().connection
            se.type(locators["password"], password)

        def submit_sign_in_credentials(self, success=False):
            se = wrapper().connection
            se.click(locators["sign in"])
            se.wait_for_page_to_load("20000")
        
        def sign_in_error_message_should_be(self, message):
            se = wrapper().connection
            assert se.get_text(locators['error messages']) == message

A few things of note.

* the _wrapper_ that gets imported is a singleton connection to the Se server
* in a 'normal' PO, self.se would be set in the constructor, but the way RF creates objects means that it tries to make the connection before things are connected leading to non-good things happening.
* locators are isolated to the PO that they are used in. And they should not cross.
* element interaction is done in the keyword via API calls rather than through an Element instance
* the name of the page is in each keyword since there are not variables flying around in RF