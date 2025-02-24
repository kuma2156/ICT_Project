from pymongo import MongoClient
from bson.son import SON

# MongoDB Atlas 클러스터 정보
atlas_username = 'haneum'
atlas_password = 'gksdldma001'
atlas_cluster = 'cluster0.qiemnkw.mongodb.net'
database_name = 'market_tracker'
collection_name = 'product_trends'
average_collection_name = 'category_capacity_averages'

# MongoDB Atlas 연결 URI 생성
uri = f"mongodb+srv://{atlas_username}:{atlas_password}@{atlas_cluster}/{database_name}?retryWrites=true&w=majority"

# MongoDB 클라이언트 생성
client = MongoClient(uri)

try:
    # 데이터베이스와 컬렉션 선택
    db = client[database_name]
    collection = db[collection_name]
    average_collection = db[average_collection_name]

    # 기존 데이터 삭제
    average_collection.delete_many({})

    # Aggregation pipeline to calculate average price per category_small and total_capacity
    pipeline = [
        {
            '$match': {
                'price': {'$ne': None}  # 가격이 None이 아닌 데이터만 선택
            }
        },
        {
            '$project': {
                'category_small': 1,
                'total_capacity': 1,
                'total_capacity_unit': 1,
                'price': {
                    '$cond': {
                        'if': {'$regexMatch': {'input': {'$toString': '$price'}, 'regex': r'^\d+$'}},
                        'then': {'$toDouble': '$price'},
                        'else': None
                    }
                }
            }
        },
        {
            '$group': {
                '_id': {
                    'category_small': '$category_small',
                    'total_capacity': '$total_capacity',
                    'total_capacity_unit': '$total_capacity_unit'
                },
                'average_price': {'$avg': '$price'}
            }
        },
        {
            '$sort': SON([('average_price', -1)])  # 평균 가격을 기준으로 내림차순 정렬
        }
    ]

    # Aggregation 실행
    result = collection.aggregate(pipeline)

    # 결과를 새로운 컬렉션에 삽입
    average_data = [{
        'category_small': item['_id']['category_small'],
        'total_capacity': item['_id']['total_capacity'],
        'total_capacity_unit': item['_id']['total_capacity_unit'],
        'average_price': item['average_price']
    } for item in result]

    if average_data:
        average_collection.insert_many(average_data)
        print(f"{len(average_data)} 개의 카테고리 및 용량별 평균 가격 데이터를 '{average_collection_name}' 컬렉션에 삽입했습니다.")
    else:
        print(f"삽입할 평균 가격 데이터가 없습니다.")

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    # MongoDB 클라이언트 종료
    client.close()
