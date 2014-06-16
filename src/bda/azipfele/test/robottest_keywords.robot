*** Keywords ***

# -----------------------------------------------------------------------------
# Login
# -----------------------------------------------------------------------------

I'm logged in as admin
    Debug
    Go to  ${PLONE_URL}/login_form
    Page should contain element  __ac_name
    Page should contain element  __ac_password
    Page should contain button  Log in
    Input text  __ac_name  admin
    Input text  __ac_password  secret
    Click Link  Log in
    Wait Until Page Contains  Contents

