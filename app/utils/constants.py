INVALID_SCHEMA = "INVALID_SCHEMA"
MASTER_SCHEMA = "public"
DB_NOT_UPTODATE = "DB_NOT_UPTODATE"
HEAD = "HEAD"
AUTHORIZATION = "Authorization"
USER_NOT_FOUND = "USER_NOT_FOUND"

# User related constants:
INCORRECT_PASSWORD = "INCORRECT_PASSWORD"
USER_CREATED_SUCCESSFULLY = "USER_CREATED_SUCCESSFULLY"
USER_WITH_THIS_EMAIL_ALREADY_EXISTS = "A_USER_WITH_THIS_EMAIL_ALREADY_EXISTS"
A_USER_WITH_THIS_CONTACT_ALREADY_EXISTS = "A_USER_WITH_THIS_CONTACT_ALREADY_EXISTS"

# Branch related constants
BRANCH_NOT_FOUND = "BRANCH_NOT_FOUND"
BRANCH_CREATED_SUCCESSFULLY = "BRANCH_CREATED_SUCCESSFULLY"
BRANCH_UPDATED_SUCCESSFULLY = "BRANCH_UPDATED_SUCCESSFULLY"
CITY_NAME_ALREADY_EXISTS = "CITY_NAME_ALREADY_EXISTS"
DOMAIN_NAME_ALREADY_EXISTS = "DOMAIN_NAME_ALREADY_EXISTS"

# Company related constants:
COMPANY_CREATED_SUCCESSFULLY = "COMPANY_CREATED_SUCCESSFULLY"
COMPANY_UPDATED_SUCCESSFULLY = "COMPANY_UPDATED_SUCCESSFULLY"
COMPANY_DELETED_SUCCESSFULLY = "COMPANY_DELETED_SUCCESSFULLY"
COMPANY_NOT_FOUND = "COMPANY_NOT_FOUND"
A_COMPANY_WITH_THIS_NAME_ALREADY_EXISTS = "A_COMPANY_WITH_THIS_NAME_ALREADY_EXISTS"
A_COMPANY_WITH_THIS_EMAIL_ALREADY_EXISTS = "A_COMPANY_WITH_THIS_EMAIL_ALREADY_EXISTS"

# Bus related constants:
BUS_CREATED_SUCCESSFULLY = "BUS_CREATED_SUCCESSFULLY"
BUS_UPDATED_SUCCESSFULLY = "BUS_UPDATED_SUCCESSFULLY"
BUS_DELETED_SUCCESSFULLY = "BUS_DELETED_SUCCESSFULLY"
BUS_NOT_FOUND = "BUS_NOT_FOUND"
A_BUS_WITH_THIS_NUMBER_ALREADY_EXISTS = "A_BUS_WITH_THIS_NUMBER_ALREADY_EXISTS"
A_BUS_WITH_THIS_ROUTE_ALREADY_EXISTS = "A_BUS_WITH_THIS_ROUTE_ALREADY_EXISTS"
BUS_SCHEDULE_CREATED_SUCCESSFULLY = "BUS_SCHEDULE_CREATED_SUCCESSFULLY"
BUS_SCHEDULE_UPDATED_SUCCESSFULLY = "BUS_SCHEDULE_UPDATED_SUCCESSFULLY"
BUS_SCHEDULE_DELETED_SUCCESSFULLY = "BUS_SCHEDULE_DELETED_SUCCESSFULLY"
SCHEDULE_NOT_FOUND = "SCHEDULE_NOT_FOUND"

# Ticket related constants:
TICKET_CREATED_SUCCESSFULLY = "TICKET_CREATED_SUCCESSFULLY"
TICKET_UPDATED_SUCCESSFULLY = "TICKET_UPDATED_SUCCESSFULLY"
TICKET_DELETED_SUCCESSFULLY = "TICKET_DELETED_SUCCESSFULLY"
TICKET_NOT_FOUND = "TICKET_NOT_FOUND"

#┌────────────────────────────── FIELD VALIDATION ERROR MESSAGES ────────────────────────────────────┐
ATLEAST_ONE_UPPER_CASE = "must contain at least one uppercase letter."
ATLEAST_ONE_LOWER_CASE = "must contain at least one lowercase letter."
ATLEAST_ONE_DIGIT = "must contain at least one digit."
ATLEAST_ONE_SPECIAL_CHARACTER = "must contain at least one special character."
SHOULD_NOT_CONTAIN_SPACES = "must not contain spaces."
ATLEAST_36_CHARACTERS = "must be at least 36 characters long."
GREATER_THAN_ZERO = "must be greater than zero"
ATLEAST_8_CHARACTERS = "must be at least 8 characters long."
SHOULD_CONTAIN_10_DIGITS = "Phone number must be valid, with an optional '+' prefix and 10-15 digits."
MUST_BE_ALPHANUMERIC = "must be alphanumeric and can include underscores."
MUST_BE_BETWEEN_2_AND_20_CHARACTERS = "must be between 2 and 20 characters."
MUST_BE_ALPHABETIC = "must be alphabetic"
MUST_CONTAIN_ATLEAST_ONE_DIGIT = "must contain at least one digit."
MUST_CONTAIN_ATLEAST_ONE_LETTER = "must contain at least one letter."
INVALID_PAGE_NUMBER = "Invalid page number. Page must be between 1 and 100000."
INVALID_PAGE_SIZE = "Invalid page size. Page size must be between 1 and 1000."