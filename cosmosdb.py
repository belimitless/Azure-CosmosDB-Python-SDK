from azure.cosmos import CosmosClient, PartitionKey, exceptions

# Azure Cosmos DB credentials
ENDPOINT = "<Your-Cosmos-DB-URI>"
PRIMARY_KEY = "<Your-Cosmos-DB-Primary-Key>"

# Initialize the Cosmos client
client = CosmosClient(ENDPOINT, PRIMARY_KEY)

# Create database and container
DATABASE_NAME = "mydatabase"
CONTAINER_NAME = "myconatiner"


def create_database_and_container():
    # Create a database if it doesn't exist
    database = client.create_database_if_not_exists(id=DATABASE_NAME)

    # Create a container if it doesn't exist
    container = database.create_container_if_not_exists(
        id=CONTAINER_NAME,
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
    )

    print(
        f"Database '{DATABASE_NAME}' and container '{CONTAINER_NAME}' created/verified.")
    return container


def insert_data(container):
    # Sample data to insert
    items_to_create = [
        {"id": "1", "name": "Alice", "age": 29, "city": "New York"},
        {"id": "2", "name": "Bob", "age": 34, "city": "Los Angeles"},
        {"id": "3", "name": "Charlie", "age": 25, "city": "Chicago"}
    ]

    # Insert items into the container
    for item in items_to_create:
        container.create_item(body=item)

    print("Data inserted into the container.")


def query_data(container):
    query = input(
        "Enter your query (e.g., SELECT * FROM c WHERE c.city='New York'): ")

    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    print(f"Query results ({len(items)} items):")
    for item in items:
        print(item)


def read_item(container):
    item_id = input("Enter the ID of the item to read: ")
    partition_key = item_id

    try:
        item = container.read_item(item=item_id, partition_key=partition_key)
        print(f"Read item: {item}")
    except exceptions.CosmosResourceNotFoundError:
        print(f"Item with id {item_id} not found.")


def update_item(container):
    item_id = input("Enter the ID of the item to update: ")
    partition_key = item_id

    try:
        item_to_update = container.read_item(
            item=item_id, partition_key=partition_key)
        print(f"Current item: {item_to_update}")
        item_to_update["age"] = int(input("Enter new age: "))
        container.replace_item(item=item_to_update, body=item_to_update)
        print(f"Updated item: {item_to_update}")
    except exceptions.CosmosResourceNotFoundError:
        print(f"Item with id {item_id} not found.")


def delete_item(container):
    item_id = input("Enter the ID of the item to delete: ")
    partition_key = item_id

    try:
        container.delete_item(item=item_id, partition_key=partition_key)
        print(f"Item with id '{item_id}' deleted.")
    except exceptions.CosmosResourceNotFoundError:
        print(f"Item with id {item_id} not found.")


def show_menu():
    print("\nMenu:")
    print("1. Insert data")
    print("2. Query data")
    print("3. Read an item")
    print("4. Update an item")
    print("5. Delete an item")
    print("0. Exit")


def main():
    # Create the database and container
    container = create_database_and_container()

    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            insert_data(container)
        elif choice == '2':
            query_data(container)
        elif choice == '3':
            read_item(container)
        elif choice == '4':
            update_item(container)
        elif choice == '5':
            delete_item(container)
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
