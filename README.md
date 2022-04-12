## Автодеплой через GitHub Webhooks

### Настройка

1. Установить зависимости

`pipenv install`

2. Сделать исполняемыми bash-скрипты

`chmod +x update.sh`

`chmod +x service.sh`

3. Создать и заполнить `.env` файл из `.env.example`

4. Положить шаблон systemd юнита в папку с сервисами
```shell
cp deployer.service.template /etc/systemd/system/deployer.service
```

6. В скопированном файле с конфигом сервиса `deployer.service` указать полный 
путь до скрипта `service.sh`

7. Активировать сервис
```shell
sudo systemctl daemon-reload
sudo systemctl enable deployer.service
sudo systemctl start deployer.service
```