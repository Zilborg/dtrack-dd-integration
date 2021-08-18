# dtrack-dd-integration

For custom integration Dependency track with Defec Dojo.

## Why not native implementation

The default integration isn't flexible. In version [v4.3.2 of Dependency Track](https://github.com/DependencyTrack/dependency-track/releases/tag/4.3.2) you can manipulate only with cadence (time to synchronization).

## Features

This integration for manipulate with DB of Dependency Track. So, script collect all data, that should be send and prepare it for import in Defect Dojo.

By default, when you run script:
 - Collect all analysed with state `EXPLOITABLE` (more about [State in DTrack](https://docs.dependencytrack.org/triage/analysis-states/)) 
 - Create engagements in Defect Dojo products
 - Import results with DependencyTrack parser([docs](https://defectdojo.github.io/django-DefectDojo/integrations/import/#dependency-track), [github](https://github.com/DefectDojo/django-DefectDojo/blob/master/dojo/tools/dependency_track/parser.py))
 - Change State in Dependency Track from `EXPLOITABLE` to `IN_TRIAGE`([State in DTrack](https://docs.dependencytrack.org/triage/analysis-states/))
 - Add comment in `Audit Trails` ([docs](https://docs.dependencytrack.org/triage/auditing-basics/))

## Usage

**IMPORTANT! It works only with Postgre DB of Dependency Track.**

```bash
echo DD_TOKEN=<Your token> >> .env
echo POSTGRES_PASSWORD=<DB Password> >> .env
```

I'm using with `docker-compose` integration. 

### Example 1. 

Build docker container from source.
```bash
docker build -t dtrack-dd-integration .
```

Run it in `docker-compose`.
```bash
  sync:
    image: dtrack-dd-integration
    environment:
    # Database Properties
      - DB_HOST=db
      - POSTGRES_USER=dtrack
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    # Configuration
      - LOGLEVEL=INFO
      - DD_TOKEN=${DD_TOKEN}
      - DD_HOST=https://<DefectDojo Host>/api/v2
    command: "python3 main.py"
```

### Example 2. (Less secure)

Just mount volume with sources
```bash
  sync:
    build:
      context: ./dtrack-dd-integration
      dockerfile: Dockerfile
    environment:
    # Database Properties
      - DB_HOST=db
      - POSTGRES_USER=dtrack
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - LOGLEVEL=DEBUG
      - DD_TOKEN=${DD_TOKEN}
      - DD_HOST=https://<DefectDojo Host>/api/v2
    volumes:
      - ./dtrack-dd-integration/:/service/server/
    command: "python3 main.py"
```

## How about `autorun`?

So, this case is up to you. For example, you can use cron task for scheduler run.

```bash
*/15 * * * * cd /path/to/docker-compose.yml && docker-compose (up -d / restart) sync 
```

In future, the autorun module will be appeare.
