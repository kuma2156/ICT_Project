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
    # 데이터베이스와 컬렉션 선택
    db = client[database_name]
    collection = db[collection_name]

    # 모든 문서 조회
    all_documents = collection.find()

    # 결과 출력
    total_documents = all_documents.count_documents({})
    print(f'컬렉션 내 전체 문서 수: {total_documents}')

    for doc in all_documents:
        print(doc)

except Exception as e:
    print(f'오류 발생: {e}')
finally:
    # MongoDB 클라이언트 종료
    client.close()
