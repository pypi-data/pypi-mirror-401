# Javis Agent

## Build local
pip install -e .

## Publish package without code
### 1. Cài đặt PyArmor
```bash
cd /home/worker/src/codefun/deepl/javis_agent
source venv/bin/activate
pip install pyarmor
```

### 2. Obfuscate source code
```bash
# Tạo thư mục output cho code đã obfuscate
pyarmor gen -O dist_obfuscated javis/

# Kết quả: thư mục dist_obfuscated/ sẽ chứa code đã mã hóa
```

### 3. Cấu trúc thư mục sau khi obfuscate
```
javis_agent/
├── pyproject.toml
├── dist_obfuscated/
│   └── javis/          # Code đã obfuscate
│       ├── __init__.py
│       ├── server.py
│       └── ...
```

### 4. Sửa pyproject.toml để build từ code obfuscated
Thêm vào pyproject.toml:

```toml
[tool.hatch.build.targets.wheel]
packages = ["dist_obfuscated/javis"]
```

### 5. Build package
```bash
# Xóa dist cũ
rm -rf dist

# Build package với code đã obfuscate
pip install build twine
python -m build

# Kết quả: dist/ sẽ có .whl và .tar.gz với code đã mã hóa
```

### 6. Kiểm tra package trước khi upload
```bash
# Tạo môi trường test
python3 -m venv test_venv
source test_venv/bin/activate

# Cài đặt từ .whl local
pip install dist/Javis_agent-1.1.0-py3-none-any.whl

# Test xem có chạy được không
javis --help
```

### 7. Upload lên PyPI
```bash
twine upload dist/*
```


## User installation
python3 -m venv venv
source venv/bin/activate
pip install javis-agent
