import pymongo

# 1. Connect to Local MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["voice_advisor_db"]
collection = db["orders"]

# 2. Define Sample Data (Phonetically Distinct IDs)
sample_orders = [
    {
        "order_id": "4120",  # "Four One Two Zero" - Very clear
        "status": "shipped",
        "eta": "tomorrow by 5 PM",
        "items": "Wireless Headphones"
    },
    {
        "order_id": "7850",  # "Seven Eight Five Zero"
        "status": "processing",
        "eta": "in 3 days",
        "items": "Gaming Monitor"
    },
    {
        "order_id": "3090",  # "Three Zero Nine Zero"
        "status": "delivered",
        "eta": "yesterday",
        "items": "USB-C Cable"
    }
]

# 3. Insert into DB (Clear old data first to avoid duplicates)
collection.delete_many({})
collection.insert_many(sample_orders)

print("✅ MongoDB re-seeded successfully!")
print(f"   Database: voice_advisor_db")
print("   New IDs available: 4120, 7850, 3090")