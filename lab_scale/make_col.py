from pymongo import MongoClient

# MongoDB Atlas 클러스터 정보
atlas_username = 'haneum'
atlas_password = 'gksdldma001'
atlas_cluster = 'cluster0.qiemnkw.mongodb.net'
database_name = 'market_tracker'
collection_name = 'products'

# MongoDB Atlas 연결 URI 생성
uri = f"mongodb+srv://{atlas_username}:{atlas_password}@{atlas_cluster}/{database_name}?retryWrites=true&w=majority"

# MongoDB 클라이언트 생성
client = MongoClient(uri)

try:
    # 데이터베이스 선택 (없으면 자동으로 생성됨)
    db = client[database_name]

    # 컬렉션 확인 및 생성
    if collection_name in db.list_collection_names():
        print(f'컬렉션 "{collection_name}" 이미 존재합니다.')
    else:
        db.create_collection(collection_name)
        print(f'컬렉션 "{collection_name}"을(를) 생성하였습니다.')

    # 생성된 컬렉션에 데이터 삽입 등의 작업 수행

finally:
    # MongoDB 클라이언트 종료
    client.close()
