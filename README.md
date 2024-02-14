# Splitwise

## Architecture Overview

### Architecture Diagram

The expense-sharing system follows a three-tier architecture with the presentation layer, business logic layer, and data access layer.

```sql
+---------------------+        +-----------------------+        +------------------------+
|      Controller     |  <---  |      Service Layer    |  <---  |       Data Access      |
+---------------------+        +-----------------------+        +------------------------+
|   API Endpoints     |        |    Business Logic     |        |   Database Queries     |
+---------------------+        +-----------------------+        +------------------------+
            |                             |                                 |
            |                             |                                 |
            +-------------------------------------------------------------+
                                          |
                                          v
                                   +--------------+
                                   |    Models    |
                                   +--------------+
                                   | User         |
                                   | Expense      |
                                   | Transaction  |
                                   +--------------+


```

## Database Schema

### User Table

- `user_name` (Primary Key)
- `name`
- `email`
- `mobileNumber`

### Expense Table

- `description` 
- `expense_type`
- `total_amount`
- `participants` 

### Transaction Table

- `user` 
- `description` 
- `amount`
- `timestamp`

### Participant Table

- `user`
- `expense` 
- `share`



## API Endpoints

### User Management

- `POST /Splitwise/createUser/` - Create a user
- `POST /Splitwise/createExpense/` - Create Expense
- `GET /Splitwise/getBalances/` - Get balances of all users
- `GET /Splitwise/getUserExpense/{userId}/` - Get user balance in expense
- `GET /Splitwise/calculateBalances` - Calculate Balances



## Class Structure


### User Class

```python
class User:
    name
    user_name
    email
    mobileNumber
```
### Expense Class

```python
class Expense:
    amount
    description
    expense_type
    participants
```
### Transaction Class

```python
class Transaction:
    user
    description
    amount
    timestamp
  
```

