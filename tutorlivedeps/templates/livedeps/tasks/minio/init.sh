mc config host add minio http://minio:9000 {{ OPENEDX_AWS_ACCESS_KEY }} {{ OPENEDX_AWS_SECRET_ACCESS_KEY }} --api s3v4

# Ensure the target bucket exists
mc mb --ignore-existing minio/{{ MINIO_BUCKET_NAME }}

# Check if livedeps/archive.zip already exists
if mc stat minio/{{ MINIO_BUCKET_NAME }}/livedeps/archive.zip >/dev/null 2>&1; then
    echo "✅ livedeps/archive.zip already exists in {{ MINIO_BUCKET_NAME }}"
else
    echo "⚠️  livedeps/archive.zip not found. Creating empty archive..."

    # Create an empty ZIP file manually
    # See https://en.wikipedia.org/wiki/ZIP_(file_format)#Limits
    printf '\x50\x4b\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' > /tmp/archive.zip

    # Upload it to MinIO
    mc cp /tmp/archive.zip minio/{{ MINIO_BUCKET_NAME }}/livedeps/archive.zip

    echo "✅ Created and uploaded empty livedeps/archive.zip to {{ MINIO_BUCKET_NAME }}"
fi
