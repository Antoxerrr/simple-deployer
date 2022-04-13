## Автодеплой через GitHub Webhooks для Neti 1C Academy

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


6. В скопированном файле с конфигом сервиса `deployer.service` в строке 
`ExecStart=/bin/bash /full/path/to/service.sh` заменить `/full/path/to/project/service.sh` на полный 
путь до скрипта `service.sh` (`/bin/bash` не удалять)


7. В скопированном файле с конфигом сервиса `deployer.service` в строке 
`WorkingDirectory=/full/path/to/project` заменить `/full/path/to/project` на полный 
путь до корня проекта


8. В скопированном файле с конфигом сервиса `deployer.service` в строке 
`Environment="PATH=/root/full/path/to/project/virtualenv/bin"` заменить 
`/root/full/path/to/project/virtualenv/bin` на полный путь до папки `bin` виртуального окружения, 
созданного pipenv (`PATH=` не удалять). По умолчанию pipenv создает окружения в папке `~/.local/share/virtualenvs`


9. В скрипте `update.sh` в команде `cd` указать полный путь до обновляемого проекта


10. Активировать сервис
```shell
sudo systemctl daemon-reload
sudo systemctl enable deployer.service
sudo systemctl start deployer.service
```

В `update.sh` выполняется `git pull`, поэтому, если репозиторий приватный,
нужно чтобы явки/пароли хранились, допустим, через `git-credential-store`

Также, при необходимости, нужно вручную открыть порт 9000