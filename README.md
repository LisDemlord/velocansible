- **install-velociraptor-host.yml**: Пока только устанавливает velociraptor и формирует конфиг для сервера.

Запуск сервера:
  Находясь в дирекстории '/opt/velociraptor' ввести команду в терминал: 'sudo ./velociraptor-bin -v -c server.config.yaml frontend'
   '-v' - отвечает за вывод логов в терминал

Работоспособность проверена последующим ручным запуском сервера и командой 'curl -L -k -u LisDem:2369180ho https://192.168.124.67:8889/'
