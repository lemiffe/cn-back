# CN-BACK

Backend Flask-based API for CN-APP

## Running locally

**Docker:**
- Run start-docker.sh (will stop, remove, build, and start a new container)
- Should be accessible via port 1338 (e.g. http://localhost:1338)

## Setting up the server (for automated CI/CD deploys using CircleCI and Dokku)

**Install Dokku:**
- wget https://raw.githubusercontent.com/dokku/dokku/v0.11.3/bootstrap.sh
- sudo DOKKU_TAG=v0.11.3 bash bootstrap.sh
- Browse to your server's IP address and follow the installer

**Set up the app (on the server):**
- dokku apps:create cn-back

**Set up the domain (on the server):**
- dokku domains:report cn-back
- dokku domains:add cn-back api.yourdomain.com
- dokku config:set cn-back DOKKU_NGINX_PORT=80

**Mount configuration (on the server):**
- Create config.ini file (/home/config-cn-back.ini)
- dokku storage:mount cn-back /home/config-cn-back.ini:/cn-back/config.ini

**Set up the ports (on the server):**
- dokku proxy:ports cn-back (see list of ports, see the port of your container)
- dokku proxy:ports-add cn-back http:1338:8080 (host 1338 will map to your container now)
- dokku proxy:ports-add cn-back https:1338:8080 (host 1338 will map to your container now)
- If adding https fails, first set up SSL (see below)
- If you messed up the ports, run dokku proxy:ports-clear cn-back

**Troubleshooting:**
- Read this for more info: http://dokku.viewdocs.io/dokku~v0.11.3/deployment/application-deployment/

## Setting up SSL on the server (letsencrypt)

**Set up letsencrypt (after first deploy!):**
- sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
- dokku config:set --no-restart cn-back DOKKU_LETSENCRYPT_EMAIL=your@email.com
- dokku letsencrypt cn-back
- dokku letsencrypt:cron-job --add

**Troubleshooting:**
- Infinite redirects?
    - Might be that you have 2 nginx services running somehow
    - service nginx stop
    - ps aux | grep nginx
    - kill -9 any remaining processes
    - service nginx start
- 502s?
    - Might be the docker 1.12 issue where sometimes it fails to start a container if on the same IP
    - dokku ps:rebuild cn-back
    - You can add a check to CHECKS and automate this if necessary
- After deploy do infinite redirects come back?
    - If you set DOKKU_NGINX_PORT in your dokku config, unset it on the server
    - Reboot the server? Then:
    - dokku config:set cn-back DOKKU_NGINX_SSL_PORT=443 [see this bug](https://github.com/dokku/dokku/issues/2535)
    - dokku ps:rebuildall
- Still having issues with infinite redirects?
    - Are you using Cloudflare? Do you have SSL set to "flexible"?
    - Turn it off, it is the cause of the loop if you are also using letsencrypt!