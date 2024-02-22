@echo off
@REM for /F %%A in ('git rev-parse HEAD --short=7 HEAD') do set LATEST_COMMIT=%%A

@REM set HASH=%LATEST_COMMIT:~0,7%
@REM echo %HASH%

docker buildx bake -f docker-compose.build.yml
@REM echo build complete with TAG : %HASH%

@REM echo pushing clocksession/test:%HASH%
docker image push clocksession/test:latest
@REM docker image push clocksession/test:%HASH%

