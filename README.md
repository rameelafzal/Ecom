# Ecom
# ECommerce API

## Overview

This is an API for managing an e-commerce platform. It provides endpoints to manage products, sales, categories, user roles, inventory, and more.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the API](#running-the-api)
- [Endpoints](#endpoints)
  - [Products](#products)
  - [Sales](#sales)
  - [Categories](#categories)
  - [Users](#users)
  - [Inventory](#inventory)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- pip package manager
- MySQL or another relational database

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/rameelafzal/Ecomm.git

2. Install the required Python packages:
    ```bash
     pip install -r requirements.txt

Running the API
To run the API, use the following command:

    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

The API will be available at http://localhost:8000.

Endpoints
Sales
GET /sales/: Get a list of all sales records.
GET /sales/{sale_id}: Get details of a specific sale record.
GET /categories/{category_id}/sales: Get sales records for a specific category.
GET /products/{product_id}/sales/: Get sales records for a specific product.
Inventory
GET /inventory/: Get a list of all inventory items.
GET /inventory/low-stock-alerts Get a list of all low-stock inventory items.
PUT /inventory/{inventory_id}/update: Update inventory levels for a specific item.
GET /inventory/{inventory_id}/history: Get historical changes to inventory levels.
Revenue
GET /revenue/daily: Get daily revenue.
GET /revenue/weekly: Get weekly revenue.
GET /revenue/monthly: Get monthly revenue.
GET /revenue/annual: Get annual revenue.
GET /revenue: Get revenue by category within a date range.
