from pathlib import Path

PROJECT_NAME = "bb-s3-copy"

directories = [
    "src/bb_s3_copy/domain",
    "src/bb_s3_copy/services",
    "src/bb_s3_copy/adapters",
    "tests",
]

files = [
    "src/bb_s3_copy/__init__.py",
    "src/bb_s3_copy/bb.py",

    "src/bb_s3_copy/domain/__init__.py",
    "src/bb_s3_copy/domain/request.py",
    "src/bb_s3_copy/domain/result.py",
    "src/bb_s3_copy/domain/models.py",
    "src/bb_s3_copy/domain/exceptions.py",

    "src/bb_s3_copy/services/__init__.py",
    "src/bb_s3_copy/services/validator.py",
    "src/bb_s3_copy/services/path_resolver.py",
    "src/bb_s3_copy/services/object_discovery.py",
    "src/bb_s3_copy/services/copy_service.py",

    "src/bb_s3_copy/adapters/__init__.py",
    "src/bb_s3_copy/adapters/s3_client.py",

    "tests/__init__.py",
    "tests/test_copy_service.py",
    "tests/test_path_resolver.py",
    "tests/test_validator.py",

    "pyproject.toml",
    "README.md",
    ".gitignore",
    "LICENSE",
]

root = Path(PROJECT_NAME)

for directory in directories:
    (root / directory).mkdir(parents=True, exist_ok=True)

for file in files:
    path = root / file
    path.touch(exist_ok=True)

print(f"Proyecto '{PROJECT_NAME}' creado correctamente.")