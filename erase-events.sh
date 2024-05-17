# Ejecuta el erase_events.py en el contenedor festup-server-api-1 y escribe el resultado en un fichero
echo -n "$(date) - " >> /home/shared/FestUp-server/crontab.log
docker exec festup-server-api-1 python3 /app/erase_events.py >> /home/shared/FestUp-server/crontab.log