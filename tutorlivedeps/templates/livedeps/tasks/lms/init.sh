python3 << 'EOF'
import io
import zipfile
from django.core.files.base import File
from django.core.files.storage import storages

DEPS_KEY = "livedeps/archive.zip"
STORAGE = storages["default"]

def main():
    if STORAGE.exists(DEPS_KEY):
        print(f"✅ {DEPS_KEY} already exists in default storage.")
        return

    print(f"⚠️  {DEPS_KEY} not found. Creating an empty archive...")
    
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        pass
    buf.seek(0)

    STORAGE.save(DEPS_KEY, File(buf))
    print(f"✅ Created and uploaded empty {DEPS_KEY} to storage.")

if __name__ == "__main__":
    main()
EOF
