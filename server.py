from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.environ.get('AWS_REGION')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

s3_client = boto3.client('s3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

@app.route('/generate-upload-url', methods=['POST'])
def generate_upload_url():
    data = request.get_json()
    file_name = data.get('filename')
    content_type = data.get('contentType', 'application/octet-stream')
    folder = data.get('folder', 'uganda')  # optional folder
    print(folder)

    if not file_name:
        return jsonify({'error': 'filename is required'}), 400

    key = f"{folder.strip('/')}/{file_name}" if folder else file_name

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': key,
                'ContentType': content_type
            },
            ExpiresIn=86400  # 24 hours
        )
        return jsonify({'uploadUrl': url, 'key': key})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-download-url', methods=['POST'])
def generate_download_url():
    data = request.get_json()
    key = data.get('key')

    if not key:
        return jsonify({'error': 'S3 key is required'}), 400

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': key
            },
            ExpiresIn=86400
        )
        return jsonify({'downloadUrl': url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)

