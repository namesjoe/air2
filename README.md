# air2
docker run -d --name some-clickhouse-server -p 8123:8123 -p 9000:9000 --ulimit nofile=262144:262144 -v /home/sedov/repos/airflow2/ch_config/config.xml:/etc/clickhouse-server/config.d/config.xml yandex/clickhouse-server

connect dbeaver to CH --user=default --host=localhost --port=8123
then execute

CREATE TABLE default.songs
(
    ts DateTime('Europe/Moscow'),
    userId String,
    sessionId UInt8,
    page String,
    auth String,
    method String,
    status UInt8,
    level String,
    itemInSession UInt8,
    location String,
    userAgent String,
    lastName String,
    firstName String,
    registration DateTime('Europe/Moscow'),,
    gender FixedString(1),
    artist String,
    song String,
    length Float32
    
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(ts)
ORDER BY ts;

docker build -t namesjoe/air2:v{%d} .
docker push namesjoe/air2:v{%d}
docker-compose up -d 
