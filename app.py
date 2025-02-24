from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

# MongoDB Atlas 클러스터 정보
atlas_username = 'haneum'
atlas_password = 'gksdldma001'
atlas_cluster = 'cluster0.qiemnkw.mongodb.net'
database_name = 'market_tracker'
collection_name = 'index_products'

# MongoDB Atlas 연결 URI 생성
uri = f"mongodb+srv://{atlas_username}:{atlas_password}@{atlas_cluster}/{database_name}?retryWrites=true&w=majority"

# MongoDB 클라이언트 생성
client = MongoClient(uri)

@app.route('/documents', methods=['GET'])
def get_documents():
    try:
        # 데이터베이스와 컬렉션 선택
        db = client[database_name]
        collection = db[collection_name]

        # 모든 문서 조회
        all_documents = collection.find()

        # 결과를 JSON으로 변환
        result = dumps(all_documents)

        # 결과 출력
        total_documents = collection.count_documents({})
        print(f'컬렉션 내 전체 문서 수: {total_documents}')

        return jsonify({
            'total_documents': total_documents,
            'documents': result
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/document/<id>', methods=['GET'])
def get_document_by_id(id):
    try:
        # 데이터베이스와 컬렉션 선택
        db = client[database_name]
        collection = db[collection_name]

        # 특정 문서 조회
        document = collection.find_one({'_id': id})

        if document:
            # 결과를 JSON으로 변환
            result = dumps(document)
            return jsonify(result)
        else:
            return jsonify({'error': 'Document not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
