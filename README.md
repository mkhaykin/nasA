# nasA

## Сборка образа

```bash
docker build --build-arg APP_VERSION=0.0.1 -t pyso/nasa:0.0.1dev1 .
docker tag pyso/nasa:0.0.1dev1 pyso/nasa:latest
docker push pyso/nasa:0.0.1dev1
docker push pyso/nasa:latest
```
Или через `make`.
