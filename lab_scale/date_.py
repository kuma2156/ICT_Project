import pandas as pd
from pymongo import MongoClient

# MongoDB Atlas 클러스터 정보
atlas_username = 'haneum'
atlas_password = 'gksdldma001'
atlas_cluster = 'cluster0.qiemnkw.mongodb.net'
database_name = 'market_tracker'
collection_name = 'product_trends'
new_collection_name = 'datewise_product_prices'

# MongoDB Atlas 연결 URI 생성
uri = f"mongodb+srv://{atlas_username}:{atlas_password}@{atlas_cluster}/{database_name}?retryWrites=true&w=majority"

# MongoDB 클라이언트 생성
client = MongoClient(uri)

try:
    # 데이터베이스와 컬렉션 선택
    db = client[database_name]
    product_trends_collection = db[collection_name]
    datewise_product_prices_collection = db[new_collection_name]

    # 기존 데이터 삭제
    delete_result = datewise_product_prices_collection.delete_many({})
    print(f"기존 데이터 {delete_result.deleted_count} 개를 삭제했습니다.")

    # 날짜별로 묶어서 상품 이름과 가격을 추출
    pipeline = [
        {
            "$group": {
                "_id": "$date",
                "products": {
                    "$push": {
                        "product_name": "$product_name",
                        "price": "$price"
                    }
                }
            }
        }
    ]
    
    result = list(product_trends_collection.aggregate(pipeline))

    # 새로운 컬렉션에 데이터 삽입
    documents_to_insert = []
    for record in result:
        date = record["_id"]
        for product in record["products"]:
            document = {
                "date": date,
                "product_name": product["product_name"],
                "price": float(product["price"]) if product["price"].isdigit() else None  # 가격을 float로 변환하고 숫자가 아닌 경우 None으로 설정
            }
            documents_to_insert.append(document)

    if documents_to_insert:
        insert_result = datewise_product_prices_collection.insert_many(documents_to_insert)
        print(f"새로운 컬렉션에 {len(insert_result.inserted_ids)} 개의 문서를 삽입했습니다.")
    else:
        print("삽입할 데이터가 없습니다.")

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    # MongoDB 클라이언트 종료
    client.close()
