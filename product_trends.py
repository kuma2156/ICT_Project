from pymongo import MongoClient

# MongoDB Atlas 클러스터 정보
atlas_username = 'haneum'
atlas_password = 'gksdldma001'
atlas_cluster = 'cluster0.qiemnkw.mongodb.net'
database_name = 'market_tracker'
collection_name = 'product_trends'

# MongoDB Atlas 연결 URI 생성
uri = f"mongodb+srv://{atlas_username}:{atlas_password}@{atlas_cluster}/{database_name}?retryWrites=true&w=majority"

# MongoDB 클라이언트 생성
client = MongoClient(uri)

try:
    # 데이터베이스 선택
    db = client[database_name]

    # 컬렉션 선택
    collection = db[collection_name]

    # 컬렉션에서 첫 번째 문서 가져오기 (필드 구조 확인용)
    document = collection.find_one()

    if document:
        print("product_trends 컬렉션의 필드 구성:")
        for key, value in document.items():
            print(f"{key}: {type(value).__name__}")
    else:
        print(f"'{collection_name}' 컬렉션에 문서가 없습니다.")

finally:
    # MongoDB 클라이언트 종료
    client.close()
