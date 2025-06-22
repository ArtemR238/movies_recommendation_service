set -e
DATA_DIR="/app/data"
ML_URL="https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
ZIP_FILE="$DATA_DIR/ml-latest-small.zip"

mkdir -p "$DATA_DIR"

if [ ! -f "$ZIP_FILE" ]; then
  echo "Downloading MovieLens dataset"
  curl -L "$ML_URL" -o "$ZIP_FILE"
else
  echo "Archive already present, skipping download"
fi

if [ ! -d "$DATA_DIR/ml-latest-small" ]; then
  echo "Extracting MovieLens dataset"
  unzip -q "$ZIP_FILE" -d "$DATA_DIR"
else
  echo "Already extracted, skipping"
fi

echo "Waiting for Postgres to be ready"
until pg_isready -h db -p 5432 -U postgres >/dev/null 2>&1; do
  sleep 1
done

echo "Ingesting MovieLens data…"
python -m app.ingest

echo "Data loaded, starting API"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000