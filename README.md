
# API Documentation

This document provides an overview of the endpoints available in the Hair Services API, including request and response body details for each view.
**Base URL:** `https://example.com/api/v1`
**API Versioning:** `v1`

## RegistrationView

### Register a new user

#### Request Body
- Method: POST
- URL: `users/register/`
- Content-Type: application/json

The request body should include the following fields:

- `email` (string, required): The user's email address.
- `password` (string, required): The user's password.
- `additional_field` (type, required): Description of the additional field.

Example Request Body:
```json
{
    "email": "user@example.com",
    "password": "password123",
    "additional_field": "Additional data"
}
```

#### Response Body

- Status Code: 201 Created
- Content-Type: application/json

The response body will contain a JSON object with the following fields:

- `status` (string): Indicates the status of the request, e.g., "success" or "error."
- `message` (string): A message describing the result of the registration request.
- `data` (object): An object containing user-related data.

Example Response Body:
```json
{
    "status": "success",
    "message": "Account created successfully",
    "data": {
        "id": 1,
        "email": "user@example.com"
    }
}
```

## VerifyTwoFactorAuthTokenView

### Verify user account

#### Request Body
- Method: PATCH
- URL: `users/verify-account/`
- Content-Type: application/json

The request body should include the following fields:

- `email` (string, query parameter, required): The user's email address.
- `two_factor_auth_token` (string, required): The two-factor authentication token.

Example Request URL: `users/verify-account/?email=user@example.com`

Example Request Body:
```json
{
    "two_factor_auth_token": "123456"
}
```

#### Response Body

- Status Code: 200 OK
- Content-Type: application/json

The response body will contain a JSON object with the following fields:

- `status` (string): Indicates the status of the request, e.g., "success" or "error."
- `message` (string): A message describing the result of the verification request.

Example Response Body:
```json
{
    "status": "success",
    "message": "Account verified successfully"
}
```

## LoginView

### Login an existing user
- Method: POST
- URL: `users/login/`
- Content-Type: application/json

The request body should include the following fields:

- `email` (string, required): The user's email address.
- `password` (string, required): The user's password.

Example Request Body:
```json
{
    "email": "user@example.com",
    "password": "password123"

}
```

#### Response Body

- Status Code: 200 Ok
- Content-Type: application/json

The response body will contain a JSON object with the following fields:

- `status` (string): Indicates the status of the request, e.g., "success" or "error."
- `message` (string): A message describing the result of the login request.
- `data` (object): An object containing user-related data.

Example Response Body:
```json
{
    
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5ODcxMjQ5MiwiaWF0IjoxNjk4NjI2MDkyLCJqdGkiOiI2ZGU4Mjc5ODVlNzE0ZjljOWI0MTI0OWE3MTBmYmU5ZiIsInVzZXJfaWQiOiJiZWIzYTA5Zi1hMjUzLTQ0NjAtYTZmNy00Njc2OWJmM2Y4OTQifQ.DaCxzGkHW_wMF-Vaoa-XOW01KaElqm6B-7fDY26vp-A",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk4NjMzMjkyLCJpYXQiOjE2OTg2MjYwOTIsImp0aSI6ImIxNmU2MDg1NmNjODRhMjlhNDFjYWJiMDJhNjk3OTFlIiwidXNlcl9pZCI6ImJlYjNhMDlmLWEyNTMtNDQ2MC1hNmY3LTQ2NzY5YmYzZjg5NCJ9.QbAuamt3VZY4F6YElk13TKSCobrcKTmEWtvD65WrLWQ",
    "user_profile": {
        "status": "success",
        "message": "Login successful",
        "user_id": "beb3a09f-a253-4460-a6f7-46769bf3f894",
        "first_name": "john",
        "last_name": "doe",
        "email": "example@gmail.com",
        "username": "test123",
        "phone_number": 100000
    }

}
```

## CreateUserProfileView

### Create user profile

#### Request Body
- Method: POST
- URL: `users/register-profile/`
- Content-Type: application/json

The request body should include the following fields:

- `user` (integer, required): The user ID.
- `profile_picture` (string, optional): URL of the user's profile picture.
- `gender` (string, required): User's gender (e.g., "male" or "female").
- `date_of_birth` (string, required): User's date of birth (in the format "YYYY-MM-DD").
- `residential_address` (string, required): User's residential address.
- `city` (string, required): City where the user resides.
- `state` (string, required): State where the user resides.
- `postal_code` (string, required): Postal code of the user's location.
- `country` (string, required): Country where the user resides.

Example Request Body:
```json
{
  
    "profile_picture": "profile_pictures/user1.jpg",
    "gender": "Male",
    "date_of_birth": "1990-01-01",
    "residential_address": "123 Main St",
    "city": "City",
    "state": "State",
    "postal_code": "12345",
    "country": "Country"

}
```

#### Response Body

- Status Code: 201 Created
- Content-Type: application/json

The response body will contain a JSON object with the following fields:

- `status` (string): Indicates the status of the request, e.g., "success" or "error."
- `message` (string): A message describing the result of the user profile creation request.
- `data` (object): An object containing user profile data.

Example Response Body:
```json
{
    "status": "success",
    "message": "User Profile created successfully",
    "data": {
        "id": 1,
        "user": {
            "id": 1,
            "gender": "Male",
            "date_of birth": "1990-01-01",
            "residential_address": "123 Main St",
            "city": "City",
            "state": "State",
            "postal_code": "12345",
            "country": "Country"
        }
    }
}
```
## RetrieveUpdateUserProfileView

### Retrieve user profile

#### Request Body
- Method: GET
- URL: `users/profile/`
- Content-Type: application/json

This view retrieves the user's profile. No request body is required.

#### Response Body

- Status Code: 200 OK
- Content-Type: application/json

The response body will contain a JSON object with the following fields:

- `status` (string): Indicates the status of the request, e.g., "success" or "error."
- `message` (string): A message describing the result of the user profile retrieval request.
- `data` (object): An object containing user profile data.

Example Response Body:
```json
{
    "status": "success",
    "message": "User Profile retrieved successfully",
    "data": {
        "id": 1,
        "user": 1,
        "profile_picture": "profile_pictures/user1.jpg",
        "gender": "Male",
        "date_of birth": "1990-01-01",
        "residential_address": "123 Main St",
        "city": "City",
        "state": "State",
        "postal_code": "12345",
        "country": "Country"
    }
}
```

### Update user profile

#### Request Body
- Method: PATCH
- URL: `users/profile/`
- Content-Type: application/json

The request body should include the following fields, and it allows partial updates:

- `profile_picture` (string, optional): URL of the user's profile picture.
- `gender` (string, required): User's gender (e.g., "male" or "female").
- `date_of_birth` (string, required): User's date of birth (in the format "YYYY-MM-DD").
- `residential_address` (string, required): User's residential address.
- `city` (string, required): City where the user resides.
- `state` (string, required): State where the user resides.
- `postal_code` (string, required): Postal code of the user's location.
- `country` (string, required): Country where the user resides.

Example Request Body:
```json
{
    "profile_picture": "updated_profile_pictures/user1.jpg",
    "gender": "Female",
    "date_of_birth": "1990-01-02",
    "residential_address": "456 New St",
    "city": "New City",
    "state": "New State",
    "postal_code": "54321",
    "country": "New Country"
}
```

#### Response Body

- Status Code: 200 OK
- Content-Type: application/json

The response body will contain a JSON object with the following fields:

- `status` (string): Indicates the status of the request, e.g., "success" or "error."
- `message` (string): A message describing the result of the user profile update request.
- `data` (object): An object containing updated user profile data.

Example Response Body:
```json
{
    "status": "success",
    "message": "User Profile updated successfully",
    "data": {
        "id": 1,
        "user": 1,
        "profile_picture": "updated_profile_pictures/user1.jpg",
        "gender": "Female",
        "date_of birth": "1990-01-02",
        "residential_address": "456 New St",
        "city": "New City",
        "state": "New State",
        "postal_code": "54321",
        "country": "New Country"
    }
}
```



## UpdateUserAccountView

### Update user account

#### Request Body
- Method: PATCH
- URL: `users/update-account/`
- Content-Type: application/json

The request body should include the following fields, and it allows partial updates:

- `email` (string, optional): The user's email address.
- `first_name` (string, optional): User's first name.
- `username` (string, optional): User's username.
- `phone_number` (string, optional): User's phone number.

Example Request Body:
```json
{
    "email": "newemail@example.com",
    "full_name": "John New Doe",
    "username": "newjohndoe",
    "phone_number": "987-654-3210",
}
```

#### Response Body

- Status Code: 200 OK
- Content-Type: application/json

The response body will contain a JSON object with the following fields:

- `status` (string): Indicates the status of the request, e.g., "success" or "error."
- `message` (string): A message describing the result of the user account update request.
- `data` (object): An object containing updated user account data.

Example Response Body:
```json
{
    "status": "success",
    "message": "User Account updated successfully",
    "data": {
        "id": 1,
        "email": "newemail@example.com",
        "full_name": "John New Doe",
        "username": "newjohndoe",
        "phone_number": "987-654-3210",
    }
}
```

## ChangeUserPasswordView

### Change user password

#### Request Body
- Method: PATCH
- URL: `users/change-password/`
- Content-Type: application/json

The request body should include the following fields:

- `old_password` (string, required): The user's old password.
- `new_password` (string, required): The new password to set.

Example Request Body:
```json
{
    "old_password": "old_password123",
    "new_password": "new_password456"
}
```

#### Response Body

- Status Code: 200 OK
- Content-Type: application/json

The response body will contain a JSON object with the following fields:

- `status` (string): Indicates the status of the request, e.g., "success" or "error."
- `message` (string): A message describing the result of the password change request.

Example Response Body:
```json
{
    "status": "success",
    "message": "User password updated successfully"
}
```

## ForgetPasswordView

### Forget user password

#### Request Body
- Method: PATCH
- URL: `users/forget-password/`
- Content-Type: application/json

This view sends a reset password token to the user's email address. The request body should include the following field:

- `email` (string, required, query parameter): The user's email address to send the reset password token.

Example Request Body:
```json
{
    "email": "user@example.com"
}
```

#### Response Body

- Status Code: 200 OK
- Content-Type: application/json

The response body will contain a JSON object with the following fields:

- `status` (string): Indicates the status of the request, e.g., "success" or "error."
- `message` (string): A message describing the result of the reset password token request.

Example Response Body:
```json
{
    "status": "success",
    "message": "Reset password token sent successfully to your email"
}
```

## ResetPasswordView

### Reset user password

#### Request Body
- Method: PATCH
- URL: `users/reset-password/`
- Content-Type: application/json

The request body should include the following fields:

- `email` (string, required, query parameter): The user's email address.
- `reset_password_token` (string, required): The reset password token received via email.
- `password` (string, required): The new password to set.

Example Request Body:
```json
{
    "email": "user@example.com",
    "reset_password_token": "123456",
    "password": "new_password123"
}
```

#### Response Body

- Status Code: 200 OK
- Content-Type: application/json

The response body will contain a JSON object with the following fields:

- `status` (string): Indicates the status of the request, e.g., "success" or "error."
- `message` (string): A message describing the result of the password reset request.

Example Response Body:
```json
{
    "status": "success",
    "message": "Password reset successfully"
}
```

## DeleteUserAccountView

### Delete user account

#### Request Body
- Method: DELETE
- URL: `users/delete-account/`
- Content-Type: application/json

This view deletes the user's account. No request body is required.

#### Response Body

- Status Code: 204 No Content
- Content-Type: application/json

The response body will contain a JSON object with the following fields:

- `status` (string): Indicates the status of the request, e.g., "success" or "error."
- `message` (string): A message describing the result of the user account deletion request.

Example Response Body:
```json
{
    "status": "success",
    "message": "User Account deleted successfully"
}
```

## Service Category Views

### Create and List Service Categories (`CreateListServiceCategoryView`)

- **Endpoint:** `/service-categories/`
- **HTTP Methods:** GET (List Service Categories), POST (Create a Service Category)
- **Authentication:** Admin User (IsAdminUser permission)
- **Request (POST):**
  ```json
  {
      "category_name": "Category Name"
  }
  ```
- **Response (Success - POST):**
  - HTTP Status Code: 201 Created
  ```json
  {
      "status": "success",
      "message": "Service Category Created Successfully",
      "data": {
          "id": 1,
          "category_name": "Category Name",
          "created_at": "2023-10-28T14:30:00Z",
          "updated_at": "2023-10-28T14:30:00Z"
      }
  }
  ```
- **Response (Success - GET):**
  - HTTP Status Code: 200 OK
  ```json
  {
      "status": "success",
      "message": "Service Categories Retrieved Successfully",
      "data": [
          {
              "id": 1,
              "category_name": "Category Name",
              "created_at": "2023-10-28T14:30:00Z",
              "updated_at": "2023-10-28T14:30:00Z"
          },
          ...
      ]
  }
  ```
- **Response (Error - Invalid Data):**
  - HTTP Status Code: 400 Bad Request
  ```json
  {
      "status": "failed",
      "message": "Invalid Data",
      "data": {
          "category_name": [
              "This field is required."
          ]
      }
  }
  ```
- **Response (Error - User Does Not Exist):**
  - HTTP Status Code: 404 Not Found
  ```json
  {
      "status": "failed",
      "message": "User Does Not Exist",
      "data": []
  }
  ```

### Retrieve Service Category (`RetrieveServiceCategoryView`)

- **Endpoint:** `/service-categories/<int:id>/`
- **HTTP Method:** GET (Retrieve a Service Category)
- **Authentication:** Admin User (IsAdminUser permission)
- **Response (Success - GET):**
  - HTTP Status Code: 200 OK
  ```json
  {
      "status": "success",
      "message": "Service Category Retrieved Successfully",
      "data": [
          {
              "id": 1,
              "category_name": "Category Name",
              "created_at": "2023-10-28T14:30:00Z",
              "updated_at": "2023-10-28T14:30:00Z"
          }
      ]
  }
  ```
- **Response (Error - Service Category Does Not Exist):**
  - HTTP Status Code: 404 Not Found
  ```json
  {
      "status": "failed",
      "message": "Service Category Does Not Exist",
      "data": []
  }
  ```

## Service Views

### Create and List Services (`CreateListServiceView`)

- **Endpoint:** `/services/`
- **HTTP Methods:** GET (List Services), POST (Create a Service)
- **Authentication:** Authenticated User (IsAuthenticated permission)
- **Request (POST):**
  ```json
  {
      "service_name": "Service Name",
      "description": "Service Description",
      "price": 100.00,
      "duration_minutes": 60,
      "service_category": 1
      "start_time": "08:00",
      "end_time": "17:00"
  }
  ```
- **Response (Success - POST):**
  - HTTP Status Code: 201 Created
  ```json
  {
      "status": "success",
      "message": "Service Created Successfully",
      "data": {
          "id": 1,
          "service_name": "Service Name",
          "description": "Service Description",
          "price": 100.00,
          "duration_minutes": 60,
          "service_category": 1,
          "start_time": "08:00",
          "end_time": "17:00",
          "created_at": "2023-10-28T14:30:00Z",
          "updated_at": "2023-10-28T14:30:00Z"
      }
  }
  ```
- **Response (Success - GET):**
  - HTTP Status Code: 200 OK
  ```json
  {
      "status": "success",
      "message": "All Services Retrieved Successfully",
      "data": [
          {
              "id": 1,
              "service_name": "Service Name",
              "description": "Service Description",
              "price": 100.00,
              "duration_minutes": 60,
              "service_category": 1,
              "start_time": "08:00",
              "end_time": "17:00",
              "created_at": "2023-10-28T14:30:00Z",
              "updated_at": "2023-10-28T14:30:00Z"
          },
          ...
      ]
  }
  ```
- **Response (Error - Invalid Data):**
  - HTTP Status Code: 400 Bad Request
  ```json
  {
      "status": "failed",
      "message": "Invalid Data",
      "data": {
          "service_name": [
              "This field is required."
          ]
      }
  }
  ```
- **Response (Error - User Does Not Exist):**
  - HTTP Status Code: 404 Not Found
  ```json
  {
      "status": "failed",
      "message": "User Does Not Exist",
      "data": []
  }
  ```

### Retrieve and Update Service (`RetrieveUpdateServiceView`)

- **Endpoint:** `/services/<int:id>/`
- **HTTP Methods:** GET (Retrieve a Service), PATCH (Update a Service)
- **Authentication:**  Authenticated User (IsAuthenticated permission)
- **Response (Success - GET):**
  - HTTP Status Code: 200 OK
  ```json
  {
      "status": "success",
      "message": "Service Retrieved Successfully",
      "data": [
          {
              "id": 1,
              "service_name": "Service Name",
              "description": "Service Description",
              "price": 100.00,
              "duration_minutes": 60,
              "service_category": 1,
              "start_time": "08:00",
              "end_time": "17:00",
              "created_at": "2023-10-28T14:30:00Z",
              "updated_at": "2023-10-28T14:30:00Z"
          }
      ]
  }
  ```
- **Request (PATCH):**
  ```json
  {
      "price": 120.00
  }
  ```
- **Response (Success - PATCH):**
  - HTTP Status Code: 200 OK
  ```json
  {
      "status": "success",
      "message": "Service Updated Successfully",
      "data": {
         

 "id": 1,
          "service_name": "Service Name",
          "description": "Service Description",
          "price": 120.00,
          "duration_minutes": 60,
          "service_category": 1,
          "start_time": "08:00",
          "end_time": "17:00",
          "created_at": "2023-10-28T14:30:00Z",
          "updated_at": "2023-10-28T15:00:00Z"
      }
  }
  ```
- **Response (Error - Service Does Not Exist):**
  - HTTP Status Code: 404 Not Found
  ```json
  {
      "status": "failed",
      "message": "Service Does Not Exist",
      "data": []
  }
  ```

### Search Services by Category and Location 

(`SearchListServiceByCategoryAndLocationView`)
- **Endpoint:** `/services/search-category-location/`

- **HTTP Method:** GET
- **Authentication:** Authenticated User (IsAuthenticated permission)
- **Query Parameters:**
  - `category` (Service Category Name)
  - `location` (Service Location)
- **Response (Success):**
  - HTTP Status Code: 200 OK
  ```json
  {
      "status": "success",
      "message": "All Services Retrieved Successfully",
      "data": [
          {
              "id": 1,
              "service_name": "Service Name",
              "description": "Service Description",
              "price": 100.00,
              "duration_minutes": 60,
              "service_category": 1,
              "start_time": "08:00",
              "end_time": "17:00",
              "created_at": "2023-10-28T14:30:00Z",
              "updated_at": "2023-10-28T14:30:00Z"
          },
          ...
      ]
  }
  ```
- **Response (Error - Service Category Does Not Exist):**
  - HTTP Status Code: 404 Not Found
  ```json
  {
      "status": "failed",
      "message": "Service Category Does Not Exist",
      "data": []
  }
  ```

### Search Services by Date, Time, and Location (`SearchListServiceByDateTimeAndLocationView`)

- **Endpoint:** `/services/search-location-date-time/`
- **HTTP Method:** GET
- **Authentication:** Authenticated User (IsAuthenticated permission)
- **Query Parameters:**
  - `date` (Service Date, format: 'yyyy-mm-dd')
  - `time` (Service Time, format: 'HH:MM')
  - `location` (Service Location)
- **Response (Success):**
  - HTTP Status Code: 200 OK
  ```json
  {
      "status": "success",
      "message": "All Services Retrieved Successfully",
      "data": [
          {
              "id": 1,
              "service_name": "Service Name",
              "description": "Service Description",
              "price": 100.00,
              "duration_minutes": 60,
              "service_category": 1,
              "start_time": "08:00",
              "end_time": "17:00",
              "created_at": "2023-10-28T14:30:00Z",
              "updated_at": "2023-10-28T14:30:00Z"
          },
          ...
      ]
  }
  ```
- **Response (Error - Invalid Date Format):**
  - HTTP Status Code: 400 Bad Request
  ```json
  {
      "status": "failed",
      "message": "Invalid date format. Use 'yyyy-mm-dd'."
  }
  ```

## Service Provider Views

### List All Service Providers (`ListAllServiceProvidersView`)

- **Endpoint:** `/services/all-providers/`
- **HTTP Method:** GET
- **Authentication:** Authenticated User (IsAuthenticated permission)
- **Response (Success - GET):**
  - HTTP Status Code: 200 OK
  ```json
    {
        "status": "success",
        "message": "All service providers Retrieved Successfully",
        "data": [
            {
                "id": 1,
                "first_name": "john",
                "last_name": "doe",
                "email": "johndoe@gmail.com",
                "username": "johndoe",
                "phone_number": 100000,
                "serviced_offered": [
                    "Service A",
                    "Service B",
                    "Service C"
                ]
            },
            {
                "id": 2,
                "first_name": "jane",
                "last_name": "doe",
                "email": "james@gmail.com",
                "username": "james",
                "phone_number": 200000,
                "serviced_offered": [
                    "Service X",
                    "Service Y"
                ]
            },
            {
                "id": 3,
                "first_name": "john",
                "last_name": "doe",
                "email": "test@gmail.com",
                "username": "test",
                "phone_number": 300000,
                "serviced_offered": [
                    "Service M",
                    "Service N",
                    "Service O"
                ]
            }
        ]
    }

  ```

  ```

### Retrieve Service Provider (`RetrieveServiceProviderView`)

- **Endpoint:** `/services/providers/<str:id>/`
- **HTTP Method:** GET (Retrieve a Service Provider)
- **Authentication:** None
- **Response (Success - GET):**
  - HTTP Status Code: 200 OK
  ```json
  {
      "status": "success",
      "message": "Service Provider Retrieved Successfully",
      "data": 
          {
            id": 3,
            "first_name": "john",
            "last_name": "doe",
            "email": "johndoe@gmail.com",
            "username": "johndoe",
            "phone_number": 100000,
            "serviced_offered": [
                "Service M",
                "Service N",
                "Service O"
            ]
         }
      
  }
  ```
- **Response (Error - Service Provider Does Not Exist):**
  - HTTP Status Code: 404 Not Found
  ```json
  {
      "status": "failed",
      "message": "Service Provider Does Not Exist",
      "data": []
  }
  ```

### List All Service Provider Shops (`ListAllServiceProviderShopView`)

- **Endpoint:** `/services/shops/`
- **HTTP Method:** GET
- **Authentication:** Authenticated User (IsAuthenticated permission)
- **Response (Success - GET):**
  - HTTP Status Code: 200 OK
  ```json
  {
    "status": "success",
    "message": "All service provider shops Retrieved Successfully",
    "data": [
        {
            "id": 1,
            "business_name": "ABC Services",
            "business_address": "123 Main Street",
            "state": "California",
            "services_offered": [
                "Service A",
                "Service B",
                "Service C"
            ]
        },
        {
            "id": 2,
            "business_name": "XYZ Solutions",
            "business_address": "456 Elm Avenue",
            "state": "New York",
            "services_offered": [
                "Service X",
                "Service Y"
            ]
        },
        {
            "id": 3,
            "business_name": "123 Enterprises",
            "business_address": "789 Oak Road",
            "state": "Texas",
            "services_offered": [
                "Service M",
                "Service N",
                "Service O"
            ]
        }
    ]
}


### Retrieve Service Provider Shop (`RetrieveServiceProviderShopView`)

- **Endpoint:** `/services/shop/`
- **HTTP Method:** GET
- **Authentication:** None
- **Query Parameters:**
  - `business_name` (Service Provider Business Name)
- **Response (Success - GET):**
  - HTTP Status Code: 200 OK
  ```json
  {
      "status": "success",
      "message": "Service Provider Shop Retrieved Successfully",
      "data": {
          "id": 1,
          "business_name": "123 Enterprises",
            "business_address": "789 Oak Road",
            "state": "Texas",
            "services_offered": [
                "Service M",
                "Service N",
                "Service O"
            ]
      }
  }
  ```
- **Response (Error - Service Provider Shop Does Not Exist):**
  - HTTP Status Code: 404 Not Found
  ```json
  {
      "status": "failed",
      "message": "Service Provider Shop Does Not Exist",
      "data": []
  }
  ```

### `UserBookedAppointmentView`

**Request:**
- HTTP Method: POST
- URL: /book-appointments/
- Headers: 
    - Authorization: Token [your_token_here]
- Request Body:
    ```json
    {
        "service_provider": "Service Provider Name",
        "service": "Service Name",
        "date": "2023-11-30",
        "time": "14:30",
        "notes": "Additional notes (optional)"
    }
    ```

**Response (Success):**
- HTTP Status Code: 201 Created
- Response Body:
    ```json
    {
        "status": "success",
        "message": "Appointment booked Successfully",
        "data": {
            "id": 1,
            "user": 1,
            "service_provider": 1,
            "service": 1,
            "date": "2023-11-30",
            "time": "14:30",
            "status": "pending",
            "notes": "Additional notes (optional)",
            "created_at": "2023-10-28T14:30:00Z",
            "updated_at": "2023-10-28T14:30:00Z"
        }
    }
    ```

**Response (Error - Service Provider Does Not Exist):**
- HTTP Status Code: 400 Bad Request
- Response Body:
    ```json
    {
        "status": "error",
        "message": "Service provider does not exist"
    }
    ```

**Response (Error - Service Does Not Exist):**
- HTTP Status Code: 400 Bad Request
- Response Body:
    ```json
    {
        "status": "error",
        "message": "Service does not exist"
    }
    ```

**Response (Error - Time Not Available):**
- HTTP Status Code: 400 Bad Request
- Response Body:
    ```json
    {
        "status": "error",
        "message": "Time not available"
    }
    ```

**Response (Error - Date or Time in the Past):**
- HTTP Status Code: 400 Bad Request
- Response Body:
    ```json
    {
        "status": "error",
        "message": "Date or time provided is in the past"
    }
    ```

**Response (Error - Service Provider or Service Not Available on Selected Day):**
- HTTP Status Code: 400 Bad Request
- Response Body:
    ```json
    {
        "status": "error",
        "message": "Service provider is not available on this day"
    }
    ```

**Response (Error - Service Provider Not Available at Selected Time):**
- HTTP Status Code: 400 Bad Request
- Response Body:
    ```json
    {
        "status": "error",
        "message": "Service provider is not available at this time"
    }
    ```

**Response (Error - Service Not Available on Selected Day):**
- HTTP Status Code: 400 Bad Request
- Response Body:
    ```json
    {
        "status": "error",
        "message": "Service is not available on this day"
    }
    ```

**Response (Error - Time Already Booked):**
- HTTP Status Code: 400 Bad Request
- Response Body:
    ```json
    {
        "status": "error",
        "message": "Time is already booked, please choose another time"
    }
    ```

### `UserBookedAppointmentListView`
**Request:**
- HTTP Method: GET
- URL: /book-appointments/all-appointments/
- Headers: 
    - Authorization: Token [your_token_here]

**Response (Success):**
- HTTP Status Code: 200 OK
- Response Body:
    ```json
    {
        "status": "success",
        "message": "User booked appointments retrieved successfully",
        "data": [
            {
                "id": 1,
                "user": 1,
                "service_provider": 1,
                "service": 1,
                "date": "2023-11-30",
                "time": "14:30",
                "status": "pending",
                "notes": "Additional notes (optional)",
                "created_at": "2023-10-28T14:30:00Z",
                "updated_at": "2023-10-28T14:30:00Z"
            },
            {
                "id": 2,
                "user": 1,
                "service_provider": 2,
                "service": 2,
                "date": "2023-12-15",
                "time": "10:00",
                "status": "completed",
                "notes": "Notes for completed appointment",
                "created_at": "2023-11-15T10:00:00Z",
                "updated_at": "2023-11-15T10:00:00Z"
            }
        ]
    }
    ```

### `RetrieveUpdateDestroyUserBookedAppointmentView`
**Request:**
- HTTP Method: GET
- URL: /book-appointments/<int:appointment_id>/
- Headers: 
    - Authorization: Token [your_token_here]

**Response (Success):**
- HTTP Status Code: 200 OK
- Response Body:
    ```json
    {
        "status": "success",
        "message": "User booked appointment retrieved successfully",
        "data": {
            "id": 1,
            "user": 1,
            "service_provider": 1,
            "service": 1,
            "date": "2023-11-30",
            "time": "14:30",
            "status": "pending",
            "notes": "Additional notes (optional)",
            "created_at": "2023-10-28T14:30:00Z",
            "updated_at": "2023-10-28T14:30:00Z"
        }
    }
    ```

**Request:**
- HTTP Method: PATCH
- URL:/book-appointments/<int:appointment_id>/
- Headers: 
    - Authorization: Token [your_token_here]
- Request Body (Update Notes):
    ```json
    {
        "notes": "Updated notes for the appointment"
    }
    ```

**Response (Success):**
- HTTP Status Code: 200 OK
- Response Body:
    ```json
    {
        "status": "success",
        "message": "User booked appointment updated

 successfully",
        "data": {
            "id": 1,
            "user": 1,
            "service_provider": 1,
            "service": 1,
            "date": "2023-11-30",
            "time": "14:30",
            "status": "pending",
            "notes": "Updated notes for the appointment",
            "created_at": "2023-10-28T14:30:00Z",
            "updated_at": "2023-10-28T15:00:00Z"  // Updated timestamp
        }
    }
    ```
**Request:**
- HTTP Method: DELETE
- URL: /book-appointments/<int:appointment_id>/
- Headers: 
    - Authorization: Token [your_token_here]

**Response (Success):**
- HTTP Status Code: 204 No Content
- Response Body: No content in the response.