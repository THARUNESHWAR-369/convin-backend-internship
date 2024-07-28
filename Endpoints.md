# Endpoints
### Auth
<ul>
  <li>Login</li>
  <ul>
    <li><code>POST /api/v1/auth/token</code></li>
    <li>Request Body (application/x-www-form-urlencoded)</li>
    <pre>
    {
      "username": "test@example.com",
      "password": "testpassword"
    }
    </pre>
    <li>Response</li>
    <pre>
    {
      "access_token": "string",
      "token_type": "bearer"
    }
    </pre>
  </ul>
</ul>

### Users

<ul>
  <li>Create a new user</li>
  <ul>
    <li><code>POST /api/v1/users/</code></li>
    <li>Request Body</li>
    <pre>
    {
      "email": "newuser@example.com",
      "name": "New User",
      "mobile": "0987654321",
      "password": "newpassword"
    }
    </pre>
  </ul>
  <li>Get current authenticated user</li>
  <ul>
    <li><code>GET /api/v1/users/current_user</code></li>
    <li>Request Header</li>
    <pre>
    {
      "Authorization": "Bearer access_token"
    }
    </pre>
    <li>Response</li>
    <pre>
    {
      "id": 1,
      "email": "test@example.com",
      "name": "Test User",
      "mobile": "1234567890"
    }
    </pre>
  </ul>
  <li>Get all users</li>
  <ul>
    <li><code>GET /api/v1/users/all</code></li>
    <li>Response</li>
    <pre>
    [
      {
        "id": 1,
        "email": "test@example.com",
        "name": "Test User",
        "mobile": "1234567890"
      },
      ...
    ]
    </pre>
  </ul>
  <li>Get a user by ID</li>
  <ul>
    <li><code>GET /api/v1/users/{user_id}</code></li>
    <li>Response</li>
    <pre>
    {
      "id": 1,
      "email": "test@example.com",
      "name": "Test User",
      "mobile": "1234567890"
    }
    </pre>
  </ul>
</ul>

### Expenses

<ul>
  <li>Create a new expense</li>
  <ul>
    <li><code>POST /api/v1/expenses/create_expense</code></li>
    <li>Request Header</li>
    <pre>
    {
      "Authorization": "Bearer access_token"
    }
    </pre>
    <li>Request Body</li>
    <pre>
    {
      "amount": 100.0,
      "description": "Test Expense",
      "split_method": "equal",
      "splits": [{"user_id": 1}]
    }
    </pre>
    <li>Response</li>
    <pre>
    {
      "id": 1,
      "amount": 100.0,
      "description": "Test Expense",
      "split_method": "equal",
      "owner_id": 1
    }
    </pre>
  </ul>
  <li>Get current user's expenses</li>
  <ul>
    <li><code>GET /api/v1/expenses/current_user_expenses</code></li>
    <li>Request Header</li>
    <pre>
    {
      "Authorization": "Bearer access_token"
    }
    </pre>
    <li>Response</li>
    <pre>
    [
      {
        "id": 1,
        "amount": 100.0,
        "description": "Test Expense",
        "split_method": "equal",
        "owner_id": 1
      }
    ]
    </pre>
  </ul>
  <li>Get balance sheet of current user</li>
  <ul>
    <li><code>GET /api/v1/expenses/balance_sheet/current_user</code></li>
    <li>Request Header</li>
    <pre>
    {
      "Authorization": "Bearer access_token"
    }
    </pre>
    <li>Response</li>
    <pre>
    {
      "balance": 50.0,
      "owed_to": [{"user_id": 2, "amount": 25.0}],
      "owed_by": [{"user_id": 3, "amount": 75.0}]
    }
    </pre>
  </ul>
  <li>Get overall balance sheet</li>
  <ul>
    <li><code>GET /api/v1/expenses/balance_sheet/overall</code></li>
    <li>Request Header</li>
    <pre>
    {
      "Authorization": "Bearer access_token"
    }
    </pre>
    <li>Response</li>
    <pre>
    [
      {
        "user_id": 1,
        "balance": 50.0
      },
      {
        "user_id": 2,
        "balance": -25.0
      },
      {
        "user_id": 3,
        "balance": -75.0
      }
    ]
    </pre>
  </ul>
  <li>Download current user's balance sheet</li>
  <ul>
    <li><code>GET /api/v1/expenses/download/balance_sheet/current_user</code></li>
    <li>Request Header</li>
    <pre>
    {
      "Authorization": "Bearer access_token"
    }
    </pre>
  </ul>
  <li>Download overall balance sheet</li>
  <ul>
    <li><code>GET /api/v1/expenses/download/balance_sheet/overall</code></li>
    <li>Request Header</li>
    <pre>
    {
      "Authorization": "Bearer access_token"
    }
    </pre>
  </ul>
</ul>